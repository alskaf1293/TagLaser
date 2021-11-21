import pygame, sys
import numpy as np
from utils import *
from setup import *
from classes import *
from parameters import *

#generate maze
maze = generateMaze(width,height)
mazeWithRects, mazeGrid, mazeDim = getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror)
mazeWithRects = [x.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2) for x in mazeWithRects]

#generate players
rectIndex1X, rectIndex1Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
while [rectIndex1X, rectIndex1Y] == [rectIndex2X, rectIndex2Y]: 
    rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
player1 = Player(mazeGrid[rectIndex1X][rectIndex1Y], mazeDim)
player2 = Player(mazeGrid[rectIndex2X][rectIndex2Y], mazeDim)

#bullets
bullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: isA = True
            if event.key == pygame.K_d: isD = True
            if event.key == pygame.K_w: isW = True
            if event.key == pygame.K_s: player1.updateAngle(180)

            #shoot bullet player 1
            if event.key == pygame.K_BACKQUOTE:
                bullet = LaserBullet(player1.get_center()[0], player1.get_center()[1], player1.get_facingVector(), player1)
                bullets.append(bullet)
            ##
            if event.key == pygame.K_LEFT: isArrowLeft = True
            if event.key == pygame.K_RIGHT: isArrowRight = True
            if event.key == pygame.K_UP: isArrowUp = True
            if event.key == pygame.K_DOWN: player2.updateAngle(180)
            #shoot bullet player 2
            if event.key == pygame.K_SLASH:
                bullet = LaserBullet(player2.get_center()[0], player2.get_center()[1], player2.get_facingVector(), player2)
                bullets.append(bullet)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                isA = False
            if event.key == pygame.K_d:
                isD = False
            if event.key == pygame.K_w:
                isW = False
            ##
            
            if event.key == pygame.K_LEFT:
                isArrowLeft = False
            if event.key == pygame.K_RIGHT:
                isArrowRight = False
            if event.key == pygame.K_UP:
                isArrowUp = False
    
    ###### update values
    #update players
    if isA: player1.updateAngle(-1* maxAngleChange)
    if isD: player1.updateAngle(maxAngleChange)

    if isArrowLeft: player2.updateAngle(-1* maxAngleChange)
    if isArrowRight:player2.updateAngle(maxAngleChange)
    
    if isW:
        willCollide = checkCollisions(player1, mazeWithRects)
        if not willCollide: player1.updatePos(player1.get_facingVector()*maxSpeed)
    if isArrowUp:
        willCollide = checkCollisions(player2, mazeWithRects)
        if not willCollide: player2.updatePos(player2.get_facingVector()*maxSpeed)

    #update bullets
    for x in bullets:
        willCollide = checkBulletCollisions(x, mazeWithRects)
        if not willCollide:
            x.updateValue(x.direction*maxBulletSpeed)
        else:
            for y in mazeWithRects:
                detectBulletCollision(x,y)

    ###### rendering
    # renders surface
    surface.blit(background, (0, 0))

    #renders bullets
    for x in bullets:
        if x.get_cameFrom() == player1:
            pygame.draw.circle(surface, red, (x.xPos, x.yPos), bulletRadius)
        else:
            pygame.draw.circle(surface, blue, (x.xPos, x.yPos), bulletRadius)

    # renders walls
    for x in mazeWithRects:
        pygame.draw.rect(surface, black, x)

    #renders players
    pygame.draw.circle(surface, red, player1.get_center(), player1.get_radius())
    pygame.draw.circle(surface, blue, player2.get_center(), player2.get_radius())

    #renders angle lines
    pygame.draw.line(surface, red, player1.get_center(),player1.get_center()+ barrelLength*player1.get_facingVector(), width = barrelWidth)
    pygame.draw.line(surface, blue, player2.get_center(),player2.get_center()+ barrelLength*player2.get_facingVector(), width = barrelWidth)

    pygame.display.update()