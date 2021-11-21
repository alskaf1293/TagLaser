from setup import *
from parameters import *
from utils import *
import numpy as np

class Player:
    def __init__(self, rect, mazeDim):
        self.radius = playerRadius
        self.xPos = rect.centerx + windowX/2-mazeDim[0]/2
        self.yPos = rect.centery + windowY/2-mazeDim[1]/2
        self.angleFacing = np.random.randint(359)
        self.facingVector = getUnitCirclePointFromAngle(self.angleFacing)
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


class LaserBullet:
    def __init__(self, xPos, yPos, direction, cameFrom):
        #types float, float, np.array((2,), dtype = np.float32/64)
        # np.array([0,1]) // dimension (2,)
        self.xPos = xPos
        self.yPos = yPos
        self.direction = direction
        self.cameFrom = cameFrom
    def updateValue(self, someAmount):
        self.xPos += someAmount[0]
        self.yPos += someAmount[1]
    def get_cameFrom(self):
        return self.cameFrom