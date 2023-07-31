"""
turtlePlot.py
Simulation of plotting points using the python turtle library.
Should be similar to robotPlot.cpp.
"""

import turtle
import constants
import pointList

"""Main function for plotting image"""
def turtlePlot(pl):
    imageScaling = constants.TURTLE_IMAGE_SCALING
    scaledWidth = constants.PLOTTER_WIDTH * imageScaling
    scaledHeight = constants.PLOTTER_HEIGHT * imageScaling

    maxPoints = pl.getMaxPoints()
    setupScreen(maxPoints, imageScaling)
    t = setupTurtle()
    pl = scalePoints(pl, imageScaling, scaledWidth, scaledHeight)
    if constants.DRAW_PLOTTER_SIZE:
        drawPlotterSize(t, scaledWidth, scaledHeight)
    drawPoints(t, pl)

    t.screen.mainloop() # Waits for process termination to close the plot

"""Creates screen to plotting"""
def setupScreen(maxPoints, imageScaling):
    screen = turtle.Screen()
    screen.colormode(255) # Allows for rgb values between 0-255
    screenWidth = maxPoints.maxX * imageScaling
    screenHeight = maxPoints.maxY * imageScaling
    turtle.screensize(screenWidth, screenHeight)
    screen.setup(screenWidth + 50, screenHeight + 50)


"""Creates turtle for plotting on screen"""
def setupTurtle():
    turtle.tracer(1, constants.DRAWING_DELAY)
    t = turtle.Turtle()
    t.hideturtle()
    t.left(90)
    return t


"""Scales points to fit on screen"""
def scalePoints(pl, imageScaling, width, height):
    # Moves point to be in middle of screen, instead of only being positive
    # Inverts y-axis for visual representation
    for curPoint in pl.list:
        if curPoint.type == pointList.PointType.Point:
            curPoint.x = curPoint.x * imageScaling - width / 2
            curPoint.y = curPoint.y * -imageScaling + height / 2
    return pl


"""Output points to screen with turtle"""
def drawPoints(t, pl):
    prevPoint = pl.list[0]
    for curPoint in pl.list:
        if curPoint.type == pointList.PointType.Up:
            t.penup()
        elif curPoint.type == pointList.PointType.Down:
            t.pendown()
        else:
            if constants.DRAW_PLOTTER_SIZE:
                if curPoint.cat == pointList.PointCategory.Outside \
                        or prevPoint.cat == pointList.PointCategory.Outside:
                    t.pencolor(constants.TURTLE_ERROR_COLOR)
                else:
                    t.pencolor(constants.TURTLE_STANDARD_COLOR)

            t.setpos(curPoint.x, curPoint.y)
        prevPoint = curPoint

"""Output a rectangle representing the size of the plotter"""
def drawPlotterSize(t, width, height):
    t.pencolor(constants.TURTLE_PLOTTER_COLOR)
    t.penup()
    t.setpos(-width / 2, -height / 2)
    t.pendown()
    t.setpos(width / 2, -height / 2)
    t.setpos(width / 2, height / 2)
    t.setpos(-width / 2, height / 2)
    t.setpos(-width / 2, -height / 2)
    t.penup()
    t.pencolor(constants.TURTLE_STANDARD_COLOR)

