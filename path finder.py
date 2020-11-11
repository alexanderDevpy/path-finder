from collections import deque
import sys
import pygame as pg
import math
import time
import threading


from pygame.locals import (

    K_UP,

    K_DOWN,

    K_LEFT,

    K_RIGHT,

    K_ESCAPE,

    KEYDOWN,

    QUIT,
    K_SPACE

)


class HashableRect(pg.Rect):
    def __hash__(self):
        return hash(tuple(self))


class AStar:

    def __init__(self, name):
        self.name = name

    def distBetween(self, current, neighbor):

        if (current[2] - 1 == neighbor[2] and current[3] - 1 == neighbor[3]) or (
                current[2] - 1 == neighbor[2] and current[3] + 1 == neighbor[3]) or (
                current[2] + 1 == neighbor[2] and current[3] + 1 == neighbor[3]) or (
                current[2] + 1 == neighbor[2] and current[3] - 1 == neighbor[3]):
            cost = 14
        else:
            cost = 10

        return cost

    def heuristicEstimate(self, start, goal):

        cost = math.floor(
            (math.sqrt(math.pow(int(start[2] - goal[2]), 2) + math.pow(int(start[3] - goal[3]), 2))))

        return cost * 10

    def neighborNodes(self, current, neib):
        position = [(21, 0), (0, 21), (-21, 0), (0, -21), (21, 21), (21, -21), (-21, -21), (-21, 21)]
        neighbour = []
        close = (153, 0, 153)
        blue = (0, 153, 255)
        black = (0, 0, 0)

        for rect in rectangles:
            if rectangles[rect] == current:
                if rectangles[rect][1] == green:
                    continue
                rectangles[rect] = (rectangles[rect][0], close, rectangles[rect][2], rectangles[rect][3])
                continue

            for x, y in position:

                if rectangles[rect][0].collidepoint((current[0][0] + x, current[0][1] + y)):

                    if rectangles[rect][1] == black:
                        continue
                    if rectangles[rect][1] == green:
                        continue

                    if rectangles[rect][1] == close:
                        continue
                    else:

                        rectangles[rect] = (rectangles[rect][0], blue, rectangles[rect][2], rectangles[rect][3])
                        temp = []
                        neighbour.append(rectangles[rect])

        return neighbour

    def reconstructPath(self, cameFrom, goal):
        path = deque()
        blue = (0, 153, 255)
        gold = (255, 255, 0)
        node = goal
        node = (node[0], blue, node[2], node[3])
        path.appendleft(node)

        while node in cameFrom:
            node = cameFrom[node]
            for rect in rectangles:

                if rectangles[rect][0].collidepoint((node[0][0], node[0][1])):
                    rectangles[rect] = (rectangles[rect][0], gold)

            path.appendleft(node)

        return path

    def getLowest(self, openSet, fScore):
        lowest = float("inf")
        lowestNode = None
        for node in openSet:
            if fScore[node] < lowest:
                lowest = fScore[node]
                lowestNode = node
        return lowestNode

    def aStar(self, start, goal):
        cameFrom = {}
        openSet = set([start])
        closedSet = set()
        gScore = {}
        fScore = {}
        gScore[start] = 0
        fScore[start] = gScore[start] + self.heuristicEstimate(start, goal)
        while len(openSet) != 0:
            current = self.getLowest(openSet, fScore)
            if current[0] == goal[0]:
                return self.reconstructPath(cameFrom, goal)
            openSet.remove(current)
            closedSet.add(current)
            time.sleep(0.02)
            for neighbor in self.neighborNodes(current, closedSet):
                tentative_gScore = gScore[current] + self.distBetween(current, neighbor)
                if neighbor in closedSet and tentative_gScore >= gScore[neighbor]:
                    continue
                if neighbor not in closedSet or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor, goal)
                    if neighbor not in openSet:
                        openSet.add(neighbor)
        return 0


def draw():
    vectorx = 0
    vectory = 0
    height = 23
    width = 31
    size = 20
    color = (255, 255, 255)
    rectangles.clear()
    for y in range(height):

        for x in range(width):
            rect = HashableRect(x * (size + 1), y * (size + 1), size, size)

            rectangles[(vectorx, vectory)] = (rect, color, vectorx, vectory)

            vectorx += 1
        vectory += 1
        vectorx = 0


def main():
    global rectangles, green, red, black, greenuse, reduse, startpos
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()

    color = (255, 255, 255)
    green = (0, 255, 0)
    greenuse = False
    red = (255, 0, 0)
    reduse = False
    black = (0, 0, 0)
    startpos = None
    stoppos = None
    rectangles = {}
    reset = False

    done = False
    draw()
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not reset:

                        star = AStar("Star")
                        t = threading.Thread(target=star.aStar, args=(rectangles[startpos], rectangles[stoppos]))
                        t.start()

                        reset = True

                    else:
                        if t.is_alive():
                            continue
                        else:
                            reset = False
                            greenuse = False
                            reduse = False
                            draw()

        if pg.mouse.get_pressed()[0]:
            mouse_pos = pg.mouse.get_pos()

            for rect in rectangles:
                if rectangles[rect][0].collidepoint(mouse_pos):

                    if not greenuse:

                        rectangles[rect] = (rectangles[rect][0], green, rectangles[rect][2], rectangles[rect][3])
                        greenuse = True
                        startpos = rect



                    elif not reduse:
                        if rectangles[rect][1] == green:
                            break
                        else:
                            rectangles[rect] = (rectangles[rect][0], red, rectangles[rect][2], rectangles[rect][3])
                            reduse = True
                            stoppos = rect

                    else:
                        if rectangles[rect][1] == green or rectangles[rect][1] == red:
                            break
                        else:
                            rectangles[rect] = (rectangles[rect][0], black, rectangles[rect][2], rectangles[rect][3])
        screen.fill((30, 30, 30))

        for rect in rectangles:
            pg.draw.rect(screen, rectangles[rect][1], rectangles[rect][0])

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()
