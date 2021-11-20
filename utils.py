import numpy as np

def generateMaze(width, height):
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

    