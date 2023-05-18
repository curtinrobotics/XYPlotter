"""
turtlePlot.py
Simulation of plotting points using the python turtle library.
Should be similar to robotPlot.cpp.
"""

import turtle
import constants
from pointCreation import getMaxPoints

"""Main function for plotting image"""
def turtlePlot(pointList):
    maxX, maxY, minX, minY = getMaxPoints(pointList)
    screenWidth, screenHeight = setupScreen(maxX, maxY)
    t = setupTurtle()
    pointList = scalePoints(pointList, screenWidth, screenHeight)
    drawPoints(t, pointList)


"""Creates screen to plotting"""
def setupScreen(maxX, maxY):
    screen = turtle.Screen()
    screenWidth = maxX * constants.TURTLE_IMAGE_SCALING
    screenHeight = maxY * constants.TURTLE_IMAGE_SCALING
    turtle.screensize(screenWidth, screenHeight)
    screen.setup(screenWidth + 50, screenHeight + 50)
    return screenWidth, screenHeight


"""Creates turtle for plotting on screen"""
def setupTurtle():
    turtle.tracer(1, constants.DRAWING_DELAY)
    t = turtle.Turtle()
    t.hideturtle()
    t.left(90)
    return t


"""Scales points to fit on screen"""
def scalePoints(pointList, screenWidth, screenHeight):
    # Moves point to be in middle of screen, instead of only being positive
    # Inverts y-axis
    for i in range(0, len(pointList), 2):
        curX = pointList[i]
        if curX != "up" and curX != "down":
            pointList[i] = pointList[i] * constants.IMAGE_SCALING - screenWidth / 2
            pointList[i + 1] = pointList[i + 1] * -constants.IMAGE_SCALING + screenHeight / 2
    return pointList


"""Output points to screen with turtle"""
def drawPoints(t, pointList):
    for i in range(0, len(pointList), 2):
        if pointList[i] == "up":
            t.penup()
        elif pointList[i] == "down":
            t.pendown()
        else:
            t.setpos(pointList[i], pointList[i+1])
