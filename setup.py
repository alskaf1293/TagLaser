import pygame

black = (0,0,0)
windowX, windowY = 800,600
width, height = 5, 5
wallwidth, wallheight = 3, 40
probMirror=0.8

pygame.init()
window_surface = pygame.display.set_mode((windowX, windowY))
background = pygame.Surface((windowX, windowY))
background.fill(pygame.Color('#FFFFFF'))