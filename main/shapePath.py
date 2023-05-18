"""
shapePath.py
Path classes for path shape

List of paths:
M: move
L: line
H: horizontal line
V: vertical line
C: cubic Bézier curves
S: smooth cubic Bézier curves
Q: quadratic Bézier curves
T: smooth quadratic Bézier curves
A: arc
Z: end path

More info on paths
https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
"""

import constants
from inputOutput import printd, printw, printe

class Path:
    def __init__(self):
        self.isRelative = False
        self.xStart = 0
        self.yStart = 0


class Move(Path):
    def __init__(self):
        super().__init__()
        self.length = 2  # DO NOT CHANGE
        self.x = []
        self.y = []

    def getPoints(self):
        printd("Move: " + str(self.x) + ", " + str(self.y))
        pointList = []
        xPrev = self.xStart
        yPrev = self.yStart
        for i in range(len(self.x)):
            if self.isRelative:
                pointList.append(self.x[i] + xPrev)
                pointList.append(self.y[i] + yPrev)
                xPrev = pointList[-2]
                yPrev = pointList[-1]
            else:
                pointList.append(self.x[i])
                pointList.append(self.y[i])
        return pointList


class Line(Move):
    def __init__(self):
        super().__init__()
        self.length = 2  # DO NOT CHANGE

    def getPoints(self):
        return super().getPoints()


class HorizontalLine(Line):
    def __init__(self):
        super().__init__()
        self.length = 1  # DO NOT CHANGE

    def getPoints(self):
        # Make point absolute
        if self.isRelative:
            xPrev = self.xStart
            for i in range(len(self.x)):
                self.x[i] += xPrev
                xPrev = self.x[i]
            self.isRelative = False

        for _ in range(len(self.x)):
            self.y.append(self.yStart)
        return super().getPoints()


class VerticalLine(Line):
    def __init__(self):
        super().__init__()
        self.length = 1  # DO NOT CHANGE

    def getPoints(self):
        # Make point absolute
        if self.isRelative:
            yPrev = self.yStart
            for i in range(len(self.y)):
                self.y[i] += yPrev
                yPrev = self.y[i]
            self.isRelative = False

        for _ in range(len(self.y)):
            self.x.append(self.xStart)
        return super().getPoints()


class CubicCurve(Path):
    def __init__(self):
        super().__init__()
        self.length = 6  # DO NOT CHANGE
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.xEnd = []
        self.yEnd = []

    def _makePointsAbsolute(self):
        xPrev = self.xStart
        yPrev = self.yStart
        for i in range(len(self.x1)):
            self.x1[i] += xPrev
            self.y1[i] += yPrev
            self.x2[i] += xPrev
            self.y2[i] += yPrev
            self.xEnd[i] += xPrev
            self.yEnd[i] += yPrev
            xPrev = self.xEnd[i]
            yPrev = self.yEnd[i]

    def getPoints(self):
        # Make point absolute
        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

        printd("CubicCurve: (" + str(self.xStart) + ", " + str(self.yStart) + "), ("
               + str(self.x1) + ", " + str(self.y1) + "), ("
               + str(self.x2) + ", " + str(self.y2) + "), ("
               + str(self.xEnd) + ", " + str(self.yEnd) + ")")

        # Create curve
        pointList = []
        x0 = [self.xStart]
        x0.extend(self.xEnd[:-1])
        y0 = [self.yStart]
        y0.extend(self.yEnd[:-1])
        for i in range(len(self.x1)):
            for t in range(0, constants.CURVE_SAMPLE_POINTS + 1, 1):
                t /= constants.CURVE_SAMPLE_POINTS
                xPoint = (((1 - t) ** 3) * x0[i]) + (3 * t * ((1 - t) ** 2) * (self.x1[i])) + (
                        3 * (t ** 2) * (1 - t) * (self.x2[i])) + (t ** 3 * (self.xEnd[i]))
                yPoint = (((1 - t) ** 3) * y0[i]) + (3 * t * ((1 - t) ** 2) * (self.y1[i])) + (
                        3 * (t ** 2) * (1 - t) * (self.y2[i])) + (t ** 3 * (self.yEnd[i]))
                pointList.append(xPoint)
                pointList.append(yPoint)

        return pointList


class SmoothCubicCurve(CubicCurve):
    def __init__(self):
        super().__init__()
        self.length = 4  # DO NOT CHANGE
        self.xPrev2 = 0
        self.yPrev2 = 0
        self.prevIsCubic = False

    def getPoints(self):
        self.x1 = self.x2.copy()
        self.y1 = self.y2.copy()

        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

        if self.prevIsCubic:
            x0 = [self.xStart]
            x0.extend(self.xEnd[:-1])
            y0 = [self.yStart]
            y0.extend(self.yEnd[:-1])
            xn1 = [self.xPrev2]
            xn1.extend(self.x2[:-1])
            yn1 = [self.yPrev2]
            yn1.extend(self.y2[:-1])
            for i in range(len(self.x1)):
                self.x1[i] = x0[i] + (x0[i] - xn1[i])
                self.y1[i] = y0[i] + (y0[i] - yn1[i])

        return super().getPoints()


class QuadraticCurve(Path):
    def __init__(self):
        super().__init__()
        self.length = 4  # DO NOT CHANGE
        self.x1 = []
        self.y1 = []
        self.xEnd = []
        self.yEnd = []

    def _makePointsAbsolute(self):
        xPrev = self.xStart
        yPrev = self.yStart
        for i in range(len(self.x1)):
            self.x1[i] += xPrev
            self.y1[i] += yPrev
            self.xEnd[i] += xPrev
            self.yEnd[i] += yPrev
            xPrev = self.xEnd[i]
            yPrev = self.yEnd[i]

    def getPoints(self):
        # Make point absolute
        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

        printd("QuadraticCurve: (" + str(self.xStart) + ", " + str(self.yStart) + "), ("
               + str(self.x1) + ", " + str(self.y1) + "), ("
               + str(self.xEnd) + ", " + str(self.yEnd) + ")")

        # Create curve
        pointList = []
        x0 = [self.xStart]
        x0.extend(self.xEnd[:-1])
        y0 = [self.yStart]
        y0.extend(self.yEnd[:-1])
        for i in range(len(self.x1)):
            for t in range(0, constants.CURVE_SAMPLE_POINTS + 1, 1):
                t /= constants.CURVE_SAMPLE_POINTS
                xPoint = (((1 - t) ** 2) * x0[i]) + (2 * t * (1 - t) * (self.x1[i])) + (
                            t ** 2 * (self.xEnd[i]))
                yPoint = (((1 - t) ** 2) * y0[i]) + (2 * t * (1 - t) * (self.y1[i])) + (
                            t ** 2 * (self.yEnd[i]))
                pointList.append(xPoint)
                pointList.append(yPoint)

        return pointList


class SmoothQuadraticCurve(QuadraticCurve):
    def __init__(self):
        super().__init__()
        self.length = 2  # DO NOT CHANGE
        self.xPrev2 = 0
        self.yPrev2 = 0
        self.prevIsQuadratic = False

    def getPoints(self):
        self.x1 = [self.xStart]
        self.x1.extend(self.xEnd[:-1])
        self.y1 = [self.yStart]
        self.y1.extend(self.yEnd[:-1])

        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

        if self.prevIsQuadratic:
            x0 = [self.xStart]
            x0.extend(self.xEnd[:-1])
            y0 = [self.yStart]
            y0.extend(self.yEnd[:-1])
            xn1 = [self.xPrev2]
            xn1.extend(self.x1[:-1])
            yn1 = [self.yPrev2]
            yn1.extend(self.y1[:-1])
            for i in range(len(self.x1)):
                self.x1[i] = x0[i] + (x0[i] - xn1[i])
                self.y1[i] = y0[i] + (y0[i] - yn1[i])

        return super().getPoints()


class Arc(Path):
    def __init__(self):
        super().__init__()
        self.length = 7  # DO NOT CHANGE
        self.rx = []
        self.ry = []
        self.rotation = []
        self.largeArcFlag = []
        self.sweepFlag = []
        self.xEnd = []
        self.yEnd = []

    def _makePointsAbsolute(self):
        xPrev = self.xStart
        yPrev = self.yStart
        for i in range(len(self.rx)):
            self.rx[i] += xPrev
            self.ry[i] += yPrev
            self.xEnd[i] += xPrev
            self.yEnd[i] += yPrev
            xPrev = self.xEnd[i]
            yPrev = self.yEnd[i]

    def getPoints(self):
        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

        return [self.xStart, self.yStart]



class ClosePath(Path):
    def __init__(self):
        super().__init__()
        self.length = 0  # DO NOT CHANGE
        self.xEnd = 0
        self.yEnd = 0

    def getPoints(self):
        return [self.xStart, self.yStart, self.xEnd, self.yEnd]
