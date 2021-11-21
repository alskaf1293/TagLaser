#colors
black = (0,0,0)
white = (255,255,255)
red = (255, 127, 127)
blue = (100, 100, 255)
mirrorColor = (125, 249, 255)

#maze parameters
width, height = 12, 12
wallwidth, wallheight = 5, 60
probMirror=0.7

#player parameters
maxSpeed = 1
maxAngleChange = 2
playerRadius = 8
barrelLength = 16
barrelWidth = 4

#bullet parameters
shootingCooldown = 1
bulletsPerStream = 30
maxBulletSpeed = 3.5
bulletRadius = 2
maxSwitches = 20

#pygame and windows
windowX, windowY = 1200,800

#scoring
player1Score = 0
player2Score = 0

scoreFont = 'gabriola'
scoreFontSize = 70
scorePlacementBuffer = 20

#key presses
isA = False
isD = False
isW = False

isArrowUp = False
isArrowLeft = False
isArrowRight = False