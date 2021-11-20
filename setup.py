import pygame
from utils import *
from classes import *
from parameters import *

#pygame setup
pygame.init()
surface = pygame.display.set_mode((windowX, windowY))
background = pygame.Surface((windowX, windowY))
background.fill(pygame.Color('#FFFFFF'))
