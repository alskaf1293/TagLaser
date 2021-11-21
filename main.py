import pygame, sys, time
import numpy as np
from utils import *
from setup import *
from classes import *
from parameters import *

def generate():
    #generate maze
    maze = generateMaze(width,height)
    temp, mazeWithRects, temp2, mazeWalls, mazeDim = getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror)
    mazeWithRects = [x.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2) for x in mazeWithRects]

    #mazeWithRects is every rectangle you can collide with
    #every rect object in the maze
    wholeMaze = []
    for x in temp:
        thing = []
        for y in x:
            thing.append(y.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2))
        wholeMaze.append(thing)

    mazeGrid = []
    for x in temp2:
        thing = []
        for y in x:
            thing.append(y.move(windowX/2-mazeDim[0]/2, windowY/2-mazeDim[1]/2))
        mazeGrid.append(thing)
        

    #generate players
    rectIndex1X, rectIndex1Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
    rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0]))); 
    while [rectIndex1X, rectIndex1Y] == [rectIndex2X, rectIndex2Y]: 
        rectIndex2X, rectIndex2Y = np.random.randint((len(mazeGrid), len(mazeGrid[0])))
    player1 = Player(mazeGrid[rectIndex1X][rectIndex1Y], 2*rectIndex1Y+1, 2*rectIndex1X+1)
    player2 = Player(mazeGrid[rectIndex2X][rectIndex2Y], 2*rectIndex2Y+1, 2*rectIndex2X+1)

    #bullets
    bullets = []
    return player1, player2, bullets, mazeGrid, wholeMaze, maze, mazeWithRects, mazeWalls, mazeDim

player1, player2, bullets, mazeGrid, wholeMaze, maze, mazeWithRects, mazeWalls, mazeDim = generate()

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
        willCollide = checkCollisions(player1, wholeMaze, mazeWalls)
        if not willCollide: player1.updatePos(player1.get_facingVector()*maxSpeed)
    updatePlayerBox(player1, wholeMaze, mazeWalls)

    if isArrowUp:
        willCollide = checkCollisions(player2, wholeMaze, mazeWalls)
        if not willCollide: player2.updatePos(player2.get_facingVector()*maxSpeed)
    updatePlayerBox(player2, wholeMaze, mazeWalls)

    #check for bullet/player collision
    for x in bullets:
        if x.get_cameFrom() == player2:
            collided = checkCollisionBetweenCircles(x.get_center(), player1.get_center(), x.get_radius(), player1.get_radius())
            if collided:
                player2Score += 1
                time.sleep(2)
                player1, player2, bullets, mazeGrid, wholeMaze, maze, mazeWithRects, mazeWalls, mazeDim = generate()
                
        if x.get_cameFrom() == player1:
            collided = checkCollisionBetweenCircles(x.get_center(), player2.get_center(), x.get_radius(), player2.get_radius())
            if collided:
                player1Score += 1
                time.sleep(2)
                player1, player2, bullets, mazeGrid, wholeMaze, maze, mazeWithRects, mazeWalls, mazeDim = generate()
                
    #print(player1Score)
    #print(player2Score)
    #update bullets
    for x in bullets:
        willCollide, collideWall, wallIndex = checkBulletCollisions(x, wholeMaze, mazeWalls)
        if not willCollide:
            x.updateValue(x.get_direction()*maxBulletSpeed)
        else:
            if mazeWalls[wallIndex[0]][wallIndex[1]] in [2,3]:
                bullets.remove(x)
            else:
                detectBulletCollision(x,collideWall)
        updateBullet(x, wholeMaze, mazeWalls)

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
    for x in range(len(wholeMaze)):
        for y in range(len(wholeMaze[0])):
            if mazeWalls[x][y] == 1:
                pygame.draw.rect(surface, mirrorColor, wholeMaze[x][y])
            elif mazeWalls[x][y] == 3 or mazeWalls[x][y] == 2:
                pygame.draw.rect(surface, black, wholeMaze[x][y])
    #for x in mazeWithRects:
    #    pygame.draw.rect(surface, black, x)

    #renders players
    pygame.draw.circle(surface, red, player1.get_center(), player1.get_radius())
    pygame.draw.circle(surface, blue, player2.get_center(), player2.get_radius())

    #renders angle lines
    pygame.draw.line(surface, red, player1.get_center(),player1.get_center()+ barrelLength*player1.get_facingVector(), width = barrelWidth)
    pygame.draw.line(surface, blue, player2.get_center(),player2.get_center()+ barrelLength*player2.get_facingVector(), width = barrelWidth)

    #renders scores
    font = pygame.font.SysFont(scoreFont, scoreFontSize)
    player1Surface = font.render(str(player1Score), False, red)
    player2Surface = font.render(str(player2Score), False, blue)
    surface.blit(player1Surface,(scorePlacementBuffer,scorePlacementBuffer))
    surface.blit(player2Surface,(windowX-player2Surface.get_size()[0]-scorePlacementBuffer,scorePlacementBuffer))
    pygame.display.update()