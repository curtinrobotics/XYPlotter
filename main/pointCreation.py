"""
pointCreation.py
Creates a list of points from shapes created in shapeCreation.py.
"""

import constants
from inputOutput import printd, printw, printe

"""Main function for point creation"""
def pointCreation(shapeList):
    pointList = []
    for curShape in shapeList:
        printd("\nWorking on shape: " + str(curShape.name()))
        shapePointList = curShape.getPoints()
        shapePointList = curShape.transform(shapePointList)
        shapePointList = pointReduction(shapePointList)
        pointList.append(shapePointList)

    pointList = pointAdjustment(pointList)

    return pointList


"""Removes unnecessary points"""
def pointReduction(pointList):
    # First loop: rounding
    for index, curPoint in enumerate(pointList):
        if curPoint != "up" and curPoint != "down":
            pointList[index] = round(curPoint, constants.ROUND_DECIMAL_POINTS)

    # Second loop: removing duplicate point
    i = 0
    while i < len(pointList) - 2:
        if pointList[i] == pointList[i + 2] and pointList[i + 1] == pointList[i + 3]:
            del pointList[i:i + 2]
        i += 2

    return pointList

"""Adjust points to be aligned with 0,0"""
def pointAdjustment(pointList):
    maxXPoint, maxYPoint, minXPoint, minYPoint = getMaxPoints(pointList)
    for i in range(0, len(pointList), 2):
        curX = pointList[i]
        if curX != "up" and curX != "down":
            pointList[i] -= minXPoint
            pointList[i + 1] -= minYPoint

    return pointList


"""Gets maximum and minimum points out of a list"""
def getMaxPoints(pointList):
    maxXPoint = pointList[0]
    maxYPoint = pointList[1]
    minXPoint = pointList[0]
    minYPoint = pointList[1]

    for i in range(0, len(pointList), 2):
        curX = pointList[i]
        curY = pointList[i + 1]
        if curX != "up" and curX != "down":
            if curX > maxXPoint:
                maxXPoint = curX
            if curY > maxYPoint:
                maxYPoint = curY
            if curX < minXPoint:
                minXPoint = curX
            if curY < minYPoint:
                minYPoint = curY

    return maxXPoint, maxYPoint, minXPoint, minYPoint
