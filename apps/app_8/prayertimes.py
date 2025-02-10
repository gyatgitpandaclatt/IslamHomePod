import requests
from datetime import datetime
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class PrayerTimes:
    def __init__(self):
        self.prayer_api_url = "http://api.aladhan.com/v1/timings"
        self.geolocator = Nominatim(user_agent="my_prayer_app")
        self.location = None
        self.latitude = None
        self.longitude = None

    def get_user_location(self):
        """Get user location either by city name or coordinates"""
        try:
            choice = input("Enter '1' to input city name or '2' to use coordinates: ")
            
            if choice == '1':
                city = input("Enter city name (e.g., London, UK): ")
                location = self.geolocator.geocode(city)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    self.location = location
                    print(f"\nLocation found: {location.address}")
                    return True
                else:
                    print("Location not found. Please try again.")
                    return False
                    
            elif choice == '2':
                self.latitude = float(input("Enter latitude (e.g., 51.5074): "))
                self.longitude = float(input("Enter longitude (e.g., -0.1278): "))
                location = self.geolocator.reverse(f"{self.latitude}, {self.longitude}")
                if location:
                    self.location = location
                    print(f"\nLocation found: {location.address}")
                    return True
                return True
                
            else:
                print("Invalid choice. Please try again.")
                return False
                
        except GeocoderTimedOut:
            print("Timeout error. Please try again.")
            return False
        except ValueError:
            print("Invalid coordinates. Please try again.")
            return False

    def get_prayer_times(self):
        """Fetch prayer times from the API"""
        if not self.latitude or not self.longitude:
            print("Please set location first.")
            return None

        # Get current date
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")

        # Parameters for the API request
        params = {
            'latitude': self.latitude,
            'longitude': self.longitude,
            'method': 2,  # Islamic Society of North America (ISNA)
            'date': date
        }

        try:
            response = requests.get(self.prayer_api_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            if data['code'] == 200:
                return data['data']['timings']
            else:
                print("Error fetching prayer times.")
                return None

        except requests.RequestException as e:
            print(f"Error fetching prayer times: {e}")
            return None

    def display_prayer_times(self, times):
        """Display prayer times in a formatted way"""
        if not times:
            return

        print("\nPrayer Times:")
        print("=" * 30)
        
        # Order of prayer times to display
        prayer_order = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        
        # Get current time for highlighting current prayer
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        for prayer in prayer_order:
            time = times[prayer]
            
            # Add marker for current/next prayer
            if self.is_current_prayer(current_time, times, prayer):
                marker = "→ "  # Current prayer
            else:
                marker = "  "
                
            print(f"{marker}{prayer:<10} : {time}")

    def is_current_prayer(self, current_time, times, prayer):
        """Check if this is the current prayer time"""
        prayer_times = [(p, times[p]) for p in ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']]
        
        for i, (p, time) in enumerate(prayer_times):
            if p == prayer:
                if i == len(prayer_times) - 1:
                    # Last prayer (Isha)
                    return current_time >= time or current_time < prayer_times[0][1]
                else:
                    # Other prayers
                    return time <= current_time < prayer_times[i + 1][1]
        return False

def main():
    prayer = PrayerTimes()
    
    print("Welcome to Prayer Times App!")
    print("==========================")
    
    # Get location
    while not prayer.get_user_location():
        pass

    # Get and display prayer times
    times = prayer.get_prayer_times()
    if times:
        prayer.display_prayer_times(times)
    
    print("\nNote: '→' indicates the current prayer time")

if __name__ == "__main__":
    main()
