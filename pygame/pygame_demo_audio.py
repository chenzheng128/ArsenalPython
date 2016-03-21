import pygame
pygame.mixer.init()
#pygame.mixer.music.load("audio/friendship.mp3")
pygame.mixer.music.load("audio/shake.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
