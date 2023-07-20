"""
pointList.py
Classes and enums for creating a list of points
"""

import math
from enum import Enum

"""PointType - for whether the point is a position or and action"""
class PointType(Enum):
    Up = 1
    Down = 2
    Point = 3

"""PointCategory - for whether the point is inside or outside the plotter size"""
class PointCategory(Enum):
    Unknown = 1
    Inside = 2
    Border = 3
    Outside = 4
    Command = 5

"""Point - a single point/action"""
class Point:
    def __init__(self, pointType, x=None, y=None):
        self.type = pointType
        self.x = x
        self.y = y
        self.cat = PointCategory.Unknown

"""PointsList - a list of Points"""
class PointList:
    def __init__(self):
        self.list = []

    """Appends pen up command"""
    def penUp(self):
        newPoint = Point(PointType.Up)
        newPoint.cat = PointCategory.Command
        self.list.append(newPoint)

    """Appends pen down command"""
    def penDown(self):
        newPoint = Point(PointType.Down)
        newPoint.cat = PointCategory.Command
        self.list.append(newPoint)

    """Appends x and y to point list"""
    def addPoint(self, x, y):
        newPoint = Point(PointType.Point, x, y)
        self.list.append(newPoint)

    """Adds x and y to point list at index"""
    def addPointIndex(self, x, y, index):
        newPoint = Point(PointType.Point, x, y)
        self.list.insert(index, newPoint)

    """Appends list of points onto current list"""
    def extend(self, pList):
        self.list.extend(pList.list)

    """Removes last point from point list"""
    def removePoint(self):
        self.list.pop()

    """Appends list of points to create arc"""
    def drawArc(self, xPos, yPos, rx, ry, startDegree, arcDegree, res):
        sRad = startDegree * math.pi/180  # Start pos
        rad = arcDegree * math.pi/180  # Move amount
        for step in range(res+1):
            x = xPos + rx * math.cos((rad/res)*step + sRad)
            y = yPos + ry * math.sin((rad/res)*step + sRad)
            self.addPoint(x, y)

    """Returns length of the point list"""
    def length(self):
        return len(self.list)


    """Gets maximum and minimum points from"""
    def getMaxPoints(self):
        minMax = PointMinMax()

        for curPoint in self.list:
            if curPoint.type == PointType.Point:
                if curPoint.x > minMax.maxX:
                    minMax.maxX = curPoint.x
                if curPoint.y > minMax.maxY:
                    minMax.maxY = curPoint.y
                if curPoint.x < minMax.minX:
                    minMax.minX = curPoint.x
                if curPoint.y < minMax.minY:
                    minMax.minY = curPoint.y

        return minMax

"""PointMinMax - data structure for holding minimum and maximum points"""
class PointMinMax:
    def __init__(self):
        self.maxX = -9999
        self.maxY = -9999
        self.minX = 9999
        self.minY = 9999
