from setup import *
from parameters import *
from utils import *
import numpy as np

class Player:
    def __init__(self, rect, indexY, indexX):
        self.indexX = indexY
        self.indexY = indexX
        self.currentRect = rect
        self.radius = playerRadius
        self.xPos = rect.centerx
        self.yPos = rect.centery
        self.angleFacing = np.random.randint(359)
        self.facingVector = getUnitCirclePointFromAngle(self.angleFacing)
    def updateRectangle(self,rect, pos):
        self.currentRect = rect
        self.indexX = pos[0]
        self.indexY = pos[1]
    def updatePos(self, someAmount):
        self.xPos += someAmount[0]
        self.yPos += someAmount[1]
    def updateAngle(self, someAmount):
        self.angleFacing = self.angleFacing + someAmount
        self.facingVector = getUnitCirclePointFromAngle(self.angleFacing)
    def get_center(self):
        return (self.xPos, self.yPos)
    def get_radius(self):
        return self.radius
    def get_angle(self):
        return self.angleFacing
    def get_facingVector(self):
        return self.facingVector
    def get_currentRect(self):
        return self.currentRect
    def get_indexX(self):
        return self.indexX
    def get_indexY(self):
        return self.indexY


class LaserBullet:
    def __init__(self, xPos, yPos, direction, cameFrom):
        #types float, float, np.array((2,), dtype = np.float32/64)
        # np.array([0,1]) // dimension (2,)
        self.indexX = cameFrom.get_indexX()
        self.indexY = cameFrom.get_indexY()
        self.xPos = xPos
        self.yPos = yPos
        self.direction = direction
        self.cameFrom = cameFrom
    def updateRectangle(self, rect, pos):
        self.currentRect = rect
        self.indexX = pos[0]
        self.indexY = pos[1]
    def setDirection(self, val):
        self.direction = val

    def updateValue(self, someAmount):
        self.xPos += someAmount[0]
        self.yPos += someAmount[1]
    def get_cameFrom(self):
        return self.cameFrom
    def get_direction(self):
        return self.direction
    def get_center(self):
        return np.array((self.xPos, self.yPos))
    def get_radius(self):
        return bulletRadius
    def get_xPos(self):
        return self.xPos
    def get_yPos(self):
        return self.yPos
    def get_indexX(self):
        return self.indexX
    def get_indexY(self):
        return self.indexY
    