"""
pointList.py
Classes and enums for creating a list of points
"""

import math
import numpy as np
from enum import Enum
import constants as const

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

    def __str__(self):
        return f"{self.type}: {self.x}, {self.y}"

"""PointsList - a list of Points"""
class PointList:
    def __init__(self):
        self.list = []

    """---------- Adding Points ----------"""

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
    def addPoint(self, x: float, y: float):
        newPoint = Point(PointType.Point, x, y)
        self.list.append(newPoint)

    """Adds x and y to point list at index"""
    def addPointIndex(self, x: float, y: float, index: int):
        newPoint = Point(PointType.Point, x, y)
        self.list.insert(index, newPoint)

    """Appends list of point objects onto current list"""
    def extend(self, pList: list[Point]) -> None:
        self.list.extend(pList)

    """Appends list of float points onto current list"""
    def extendFloat(self, pList: list[float]) -> None:
        newList = PointList()
        for i in range(0, len(pList), 2):
            newList.addPoint(pList[i], pList[i+1])
        self.extend(newList.list)

    """Appends list of points to create arc"""
    def drawArc(self, xPos, yPos, rx, ry, startDegree=None, arcDegree=None, res=100):

        if startDegree != None and arcDegree != None:
            sRad = startDegree * math.pi/180  # Start pos
            rad = arcDegree * math.pi/180  # Move amount
            for step in range(res+1):
                x = xPos + rx * math.cos((rad/res)*step + sRad)
                y = yPos + ry * math.sin((rad/res)*step + sRad)
                self.addPoint(x, y)

    """---------- Removing Points ----------"""

    """Removes last point from point list"""
    def removePoint(self):
        self.list.pop()

    """---------- Other Methods ----------"""

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

    """Returns list of strings of g-code commands"""  # TODO: make use of point category
    def getGCode(self) -> list[str]:
        """
        G-code commands implemented
        G0 Rapid Linear Move
            G1 X___ Y___ Z___
            X: x position
            Y: y position
            Z: z position
        G1 Linear move at feed rate
            G0 X___ Y___ Z___
            X: x position
            Y: y position
            Z: z position

        XYZ Space
        Y0 = top of page, Y+ = down (confirm?)
        X0 = left of page, x+ = right
        Z0 = pen down, Z1 = pen up

        """
        outList = []
        for curPoint in self.list:
            if curPoint.type == PointType.Point:
                outList.append(f"G1 X{curPoint.x:.4f} Y{curPoint.y:.4f}")
            elif curPoint.type == PointType.Up:
                outList.append(f"G1 Z1")
            elif curPoint.type == PointType.Down:
                outList.append(f"G1 Z0")
        return outList

"""PointMinMax - data structure for holding minimum and maximum points"""
class PointMinMax:
    def __init__(self):
        self.maxX = -9999
        self.maxY = -9999
        self.minX = 9999
        self.minY = 9999
