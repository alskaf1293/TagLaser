import pygame, sys
from utils import *
from setup import *

maze = generateMaze(width,height)
mazeWithRects, mazeDim = getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window_surface.blit(background, (0, 0))

    for x in mazeWithRects:
        pygame.draw.rect(window_surface, black, x.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2))
    pygame.display.update()