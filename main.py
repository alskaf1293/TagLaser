import pygame, sys
import numpy as np
from utils import *
from setup import *
from classes import *
from parameters import *

#generate maze
maze = generateMaze(width,height)
mazeWithRects, mazeGrid, mazeDim = getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror)

#generate players
rectIndex1X, rectIndex1Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
while [rectIndex1X, rectIndex1Y] == [rectIndex2X, rectIndex2Y]: 
    rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
player1 = Player(mazeGrid[rectIndex1X][rectIndex1Y], mazeDim)
player2 = Player(mazeGrid[rectIndex2X][rectIndex2Y], mazeDim)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # renders surface
    surface.blit(background, (0, 0))

    # renders walls
    for x in mazeWithRects:
        pygame.draw.rect(surface, black, x.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2))

    #renders players
    pygame.draw.circle(surface, red, player1.get_center(), player1.get_radius())
    pygame.draw.circle(surface, blue, player2.get_center(), player2.get_radius())


    #renders bullets

    pygame.display.update()