import pygame
pygame.init()
pygame.mixer.init()

def play_sound(file_path, volume=1.0):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    sound.play()
    while pygame.mixer.get_busy(): 
        pygame.time.delay(100)
