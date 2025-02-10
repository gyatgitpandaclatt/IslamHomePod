import pygame
import os

def play_quran(folder_path):
    pygame.mixer.init()
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            pygame.mixer.music.load(os.path.join(folder_path, filename))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
play_quran("IslamHomePod-main/apps/app_7")

