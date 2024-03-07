"""
pointCreation.py
Creates a list of points from shapes created in shapeCreation.py.
"""
import math

import constants
import pointList
from inputOutput import printd, printw, printe

"""Main function for point creation"""
def pointCreation(shapeList):
    pl = pointList.PointList()
    for curShape in shapeList:
        printd("\nWorking on shape: " + str(curShape.name()))
        if curShape.checkShape():
            curPointList = curShape.getPoints()
            curPointList = curShape.transformPoints(curPointList)
            curPointList = pointReduction(curPointList)
            pl.extend(curPointList.list)
        else:
            printe("Shape " + str(curShape.name()) + " is invalid")

    pl = pointAlignment(pl)
    pl = scalePoints(pl)
    pl = findPointCategory(pl)

    return pl


"""Removes unnecessary points"""
def pointReduction(pl):
    # First loop: rounding
    for curPoint in pl.list:
        if curPoint.type == pointList.PointType.Point:
            curPoint.x = round(curPoint.x, constants.ROUND_DECIMAL_POINTS)
            curPoint.y = round(curPoint.y, constants.ROUND_DECIMAL_POINTS)

    # Second loop: removing duplicate point
    i = 0
    while i < pl.length() - 1:
        curPoint = pl.list[i]
        nextPoint = pl.list[i + 1]
        if curPoint.type == pointList.PointType.Point and nextPoint.type == pointList.PointType.Point \
                and curPoint.x == nextPoint.x and curPoint.y == nextPoint.y:
            del pl.list[i]
        i += 1

    return pl


"""Adjust points to be aligned with 0,0"""
def pointAlignment(pl):
    maxPoints = pl.getMaxPoints()
    for curPoint in pl.list:
        if curPoint.type == pointList.PointType.Point:
            curPoint.x -= maxPoints.minX
            curPoint.y -= maxPoints.minY

    return pl

"""Scales to points desired amount"""
def scalePoints(pl):
    if constants.DRAW_PLOTTER_SIZE:
        for curPoint in pl.list:
            if curPoint.type == pointList.PointType.Point:
                curPoint.x = curPoint.x * constants.PLOTTER_IMAGE_SCALING
                curPoint.y = curPoint.y * constants.PLOTTER_IMAGE_SCALING
    return pl


"""Finds the category of the point list (inside, outside, border of plotting area)"""
def findPointCategory(pl):
    if constants.DRAW_PLOTTER_SIZE:
        plotterWidth = constants.PLOTTER_WIDTH
        plotterHeight = constants.PLOTTER_HEIGHT

        # Categorize points into inside or outside the plotting area
        for curPoint in pl.list:
            if curPoint.type == pointList.PointType.Point:
                if 0 < curPoint.x < plotterWidth \
                        and 0 < curPoint.y < plotterHeight:
                    curPoint.cat = pointList.PointCategory.Inside
                elif curPoint.x == 0 or curPoint.x == plotterWidth \
                        or curPoint.y == 0 or curPoint.y == plotterHeight:
                    curPoint.cat = pointList.PointCategory.Border
                else:
                    curPoint.cat = pointList.PointCategory.Outside

        for i in range(pl.length() - 1):
            curPoint = pl.list[i]
            nextPoint = pl.list[i + 1]

            # If intersection with border of plotter area
            if (curPoint.cat == pointList.PointCategory.Inside and nextPoint.cat == pointList.PointCategory.Outside) \
                or (curPoint.cat == pointList.PointCategory.Outside and nextPoint.cat == pointList.PointCategory.Inside):

                if curPoint.cat == pointList.PointCategory.Outside:
                    outsidePoint = curPoint
                else:
                    outsidePoint = nextPoint
                # given point p(x,y) and q(x,y)
                # (py – qy)x + (qx – px)y + (pxqy – qxpy) = 0
                # a = (p_y - q_y)
                # b = (q_x - p_x)
                # c = (p_x * q_y - q_x * p_y)
                # intersection at (x_0, y_0)
                # x_0 = ( b1 * c2 - b2 * c1 )/( a1 * b2 - a2 * b1 )
                # y_0 = ( c1 * a2 - c2 * a1 )/( a1 * b2 - a2 * b1 )

                # Line calculated from points
                # ax + by + c = 0
                lineA, lineB, lineC = _lineCalc(curPoint.x, curPoint.y, nextPoint.x, nextPoint.y)
                midX = (curPoint.x + nextPoint.x) / 2
                midY = (curPoint.y + nextPoint.y) / 2

                pointDistances = {}

                # Line of side border
                sideDistance = 0
                if lineB != 0:
                    # Left and right lines
                    leftA, leftB, leftC = _lineCalc(0, 0, 0, plotterHeight)
                    rightA, rightB, rightC = _lineCalc(plotterWidth, 0, plotterWidth, plotterHeight)

                    # Intersection with left and right
                    leftIntX, leftIntY = _intersectionCalc(lineA, lineB, lineC, leftA, leftB, leftC)
                    rightIntX, rightIntY = _intersectionCalc(lineA, lineB, lineC, rightA, rightB, rightC)

                    # Distance to middle of line
                    leftSideDistance = _distanceCal(midX, midY, leftIntX, leftIntY)
                    pointDistances[leftSideDistance] = (leftIntX, leftIntY)
                    rightSideDistance = _distanceCal(midX, midY, rightIntX, rightIntY)
                    pointDistances[rightSideDistance] = (rightIntX, rightIntY)

                    sideDistance = min(leftSideDistance, rightSideDistance)

                # Line of top/bottom border
                topDistance = 0
                if lineA != 0:
                    # Top and bottom lines
                    topA, topB, topC = _lineCalc(0, plotterHeight, plotterWidth, plotterHeight)
                    bottomA, bottomB, bottomC = _lineCalc(0, 0, plotterWidth, 0)

                    # Intersection with top and bottom
                    topIntX, topIntY = _intersectionCalc(lineA, lineB, lineC, topA, topB, topC)
                    bottomIntX, bottomIntY = _intersectionCalc(lineA, lineB, lineC, bottomA, bottomB, bottomC)

                    # Distance to middle of line
                    topTopDistance = _distanceCal(midX, midY, topIntX, topIntY)
                    pointDistances[topTopDistance] = (topIntX, topIntY)
                    bottomTopDistance = _distanceCal(midX, midY, bottomIntX, bottomIntY)
                    pointDistances[bottomTopDistance] = (bottomIntX, bottomIntY)

                    topDistance = min(topTopDistance, bottomTopDistance)

                # Get intersection point
                if lineB != 0 and lineA != 0:
                    minDistance = min(sideDistance, topDistance)
                elif lineB != 0:
                    minDistance = sideDistance
                else:
                    minDistance = topDistance

                intX, intY = pointDistances[minDistance]

                # Add point at intersection
                pl.addPointIndex(intX, intY, i+1)
                pl.list[i + 1].cat = pointList.PointCategory.Border
    return pl

"""Calculates line from 2 points in form ax+by+c=0"""
def _lineCalc(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c

"""Calculates intersection between two lines in form of ax+by+c=0"""
def _intersectionCalc(a1, b1, c1, a2, b2, c2):
    den = a1 * b2 - a2 * b1
    x = None
    y = None
    if den != 0:
        x = (b1 * c2 - b2 * c1) / den
        y = (c1 * a2 - c2 * a1) / den
    return x, y

"""Calculates distance between two points"""
def _distanceCal(x1, y1, x2, y2):
    d = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return d
