"""
turtlePlot.py
Simulation of plotting points using the python turtle library.
Should be similar to robotPlot.cpp.
"""

import turtle
import constants

"""Output points to screen with turtle"""
def drawPointsTurtle(plo):
    maxPoints = plo.getMaxPoints(plo.pointsList)
    # Turtle settings for screen
    screen = turtle.Screen()
    canvasWidth = maxPoints[0] * constants.IMAGE_SCALING
    canvasHeight = maxPoints[1] * constants.IMAGE_SCALING
    turtle.screensize(canvasWidth, canvasHeight)
    screen.setup(canvasWidth + 50, canvasHeight + 50)
    turtle.tracer(1, constants.DRAWING_DELAY)
    t = turtle.Turtle()
    t.hideturtle()
    t.left(90)

    # Drawing of points
    for i in range(int(len(plo.pointsList) / 2)):
        if plo.pointsList[i * 2] == "up":
            t.penup()
        elif plo.pointsList[i * 2] == "down":
            t.pendown()
        else:
            t.setpos(plo.pointsList[i * 2] * constants.IMAGE_SCALING - canvasWidth / 2,
                     -plo.pointsList[i * 2 + 1] * constants.IMAGE_SCALING + canvasHeight / 2)
