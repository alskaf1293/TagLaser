from setup import *
from parameters import *
import numpy as np

class Player:
    def __init__(self, rect, mazeDim):
        self.radius = playerRadius
        self.xPos = rect.centerx + windowX/2-mazeDim[0]/2
        self.yPos = rect.centery + windowY/2-mazeDim[1]/2
        self.angleFacing = np.random.randint(359)
    def updateAngle(self, someAmount):
        self.angleFacing = self.angleFacing + someAmount
    def get_center(self):
        return (self.xPos, self.yPos)
    def get_radius(self):
        return self.radius


class LaserBullet:
    def __init__(self, xPos, yPos, velocity):
        #types float, float, np.array((2,0), dtype = np.float32/64)
        self.xPos = xPos
        self.yPos = yPos
        self.velocity = velocity