import numpy as np
import pygame
import math
from parameters import *

def detectBulletCollision(bullet, rect):
    velocity = bullet.get_direction()
    angle = math.atan(velocity[1]/velocity[0])

    #if horizontal wall
    if rect.width > rect.height:
        bullet.setDirection(np.array((math.cos(angle),-math.sin(angle))))
    #if vertical wall
    elif rect.height > rect.width:
        bullet.setDirection(np.array((-math.cos(angle),math.sin(angle))))

def updateBullet(bullet,wholeMaze,mazeWalls):
    futurePos = np.array(bullet.get_direction())*maxBulletSpeed + bullet.get_center()
    indexX = bullet.get_indexX()
    indexY = bullet.get_indexY()

    besideVectors = np.array([[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0]])
    surrounding = []

    for x in besideVectors:
        surroundElem = mazeWalls[indexY + x[1]][indexX + x[0]]
        if surroundElem == 0:
            surrounding.append((wholeMaze[indexY + x[1]][indexX + x[0]],x))
    for x in surrounding:
        if circleWithRectangleCollision(x[0].left, x[0].top, x[0].width, x[0].height,futurePos[0], futurePos[1], bullet.get_radius()):
            bullet.updateRectangle(x[0], x[1]+np.array([indexX,indexY]))
def checkBulletCollisions(bullet, wholeMaze, mazeWalls):
    futurePos = np.array(bullet.get_direction())*maxBulletSpeed + bullet.get_center()
    collision = None
    returnIndex = None
    indexX = bullet.get_indexX()
    indexY = bullet.get_indexY()

    besideVectors = np.array([[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0]])
    surrounding = []

    for x in besideVectors:
        surroundElem = mazeWalls[indexY + x[1]][indexX + x[0]]
        if surroundElem != 0:
            surrounding.append((wholeMaze[indexY + x[1]][indexX + x[0]],(indexY + x[1],indexX + x[0])))
    willCollide = False
    for x in surrounding:
        if circleWithRectangleCollision(x[0].left, x[0].top, x[0].width, x[0].height,futurePos[0], futurePos[1], bullet.get_radius()):
            willCollide = True
            collision = x[0]
            returnIndex = x[1]
            break
    return willCollide, collision, returnIndex

def updatePlayerBox(player, wholeMaze, mazeWalls):
    futurePos = player.get_facingVector()*maxSpeed + player.get_center()
    indexX = player.get_indexX()
    indexY = player.get_indexY()
    besideVectors = np.array([[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0]])
    surrounding = []
    for x in besideVectors:
        surroundElem = mazeWalls[indexY + x[1]][indexX + x[0]]
        if surroundElem == 0:
            surrounding.append((wholeMaze[indexY + x[1]][indexX + x[0]], x))
    for x in surrounding:
        if circleWithRectangleCollision(x[0].left, x[0].top, x[0].width, x[0].height,futurePos[0], futurePos[1], player.get_radius()):
            player.updateRectangle(x[0], x[1]+np.array([indexX,indexY]))
            break

def checkCollisions(player, wholeMaze, mazeWalls):
    futurePos = player.get_facingVector()*maxSpeed + player.get_center()
    indexX = player.get_indexX()
    indexY = player.get_indexY()
    besideVectors = np.array([[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1],[1,0]])
    surrounding = []
    for x in besideVectors:
        surroundElem = mazeWalls[indexY + x[1]][indexX + x[0]]
        if surroundElem != 0:
            surrounding.append(wholeMaze[indexY + x[1]][indexX + x[0]])
    willCollide = False
    for x in surrounding:
        if circleWithRectangleCollision(x.left, x.top, x.width, x.height,futurePos[0], futurePos[1], player.get_radius()):
            willCollide = True
    return willCollide

def circleWithRectangleCollision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width, rtop + height

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


def generateMaze(width, height):
    #input type: int, int
    #output type: list

    grids = width * height
    maze = []
    visited = []
    toVisit = []

    visited.append(0)
    toVisit.append((0,1))
    toVisit.append((0, width))

    while len(toVisit) > 0:
        randomIndex = np.random.randint(len(toVisit))
        nextPath = toVisit.pop(randomIndex)

        if nextPath[1] in visited:
            continue
        if nextPath[0] > nextPath[1]:
            maze.append((nextPath[1], nextPath[0]))
        else:
            maze.append(nextPath)
        
        visited.append(nextPath[1])

        above = nextPath[1] - width
        if above > 0 and not above in visited:
            toVisit.append((nextPath[1], above))

        left = nextPath[1] - 1
        if left % width != width - 1 and not left in visited:
            toVisit.append((nextPath[1], left))

        right = nextPath[1] + 1
        if right % width != 0 and not right in visited:
            toVisit.append((nextPath[1], right))

        below = nextPath[1] + width
        if below < grids and not below in visited:
            toVisit.append((nextPath[1], below))
    return maze

def getWallsFromMaze(maze, width, height, probMirror):
    final = np.zeros((2*width+1, 2*height + 1))
    final[0,0] = 3
    for x in range(width):
        final[0,1+2*x] = randMirror(probMirror)
    for x in range(width):
        final[0,2+2*x] = 3
    for x in range(height):
        final[1+2*x,0] = randMirror(probMirror)
    for x in range(height):
        final[2+2*x,0] = 3

    for y in range(height):
        for x in range(width):
            pos = np.array([1,1])+ 2* np.array([x,y])
            current = y*width + x
            lower = ((y+1)* width) + x
            if not (current, lower) in maze:
                final[pos[0],pos[1]+1] = randMirror(probMirror)
            if not (current, current + 1) in maze:
                final[pos[0]+1,pos[1]] = randMirror(probMirror)
            final[pos[0]+1, pos[1]+1] = 3
    return final

def randMirror(probMirror):
    #1 is mirror, 2 is wall
    randNum = np.random.rand()
    if randNum <= probMirror:
        return 1
    else: 
        return 2

def getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror):
    maze = getWallsFromMaze(maze, width, height, probMirror)
    grid = []
    final = []
    wholeMaze = []
    yPos = 0
    xPos = 0
    for y in range(len(maze)):
        wholeMazeBuff = []
        gridBuff = []
        currHeight = maze[y][0]
        for x in range(len(maze[0])):
            current = maze[y][x]
            if current == 0:
                if x % 2 == 0:
                    wholeMazeBuff.append(pygame.Rect((xPos, yPos), (wallwidth, wallheight)))
                    xPos += wallwidth
                else:
                    if x % 2 == 1 and y % 2 == 1:
                        rect = pygame.Rect((xPos, yPos), (wallheight, wallheight))
                        wholeMazeBuff.append(rect)
                        gridBuff.append(rect)
                    else:
                        wholeMazeBuff.append(pygame.Rect((xPos, yPos), (wallheight, wallwidth)))
                    xPos += wallheight

            elif current == 1 or current == 2:
                if currHeight == 3:
                    
                    rect = pygame.Rect((xPos,yPos),(wallheight, wallwidth))
                    wholeMazeBuff.append(rect)
                    final.append(rect)
                    xPos += wallheight
                elif currHeight == 1 or currHeight == 2:
                    rect = pygame.Rect((xPos,yPos),(wallwidth, wallheight))
                    wholeMazeBuff.append(rect)
                    final.append(rect)
                    xPos += wallwidth
            else:
                rect = pygame.Rect((xPos,yPos),(wallwidth, wallwidth))
                wholeMazeBuff.append(rect)
                final.append(rect)
                xPos += wallwidth
        
        if currHeight == 3:
            yPos += wallwidth
        else:
            yPos += wallheight
        if y != len(maze) -1:
            xPos = 0
        wholeMaze.append(wholeMazeBuff)
        if len(gridBuff) != 0:
            grid.append(gridBuff)
        wholeMazeBuff = []
        gridBuff = []
    
    xPos += wallwidth
    return wholeMaze, final, grid, maze, (xPos, yPos)

def getUnitCirclePointFromAngle(theta):
    thetaRadians = math.radians(theta)
    return np.array((math.cos(thetaRadians), math.sin(thetaRadians)))