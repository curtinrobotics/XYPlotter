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
        pointList = []
        for i in range(len(self.x)):
            if self.isRelative:
                pointList.append(self.xStart + self.x[i])
                pointList.append(self.yStart + self.y[i])
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
        for _ in range(len(self.x)):
            self.y.append(self.yStart)
        return super().getPoints()


class VerticalLine(Line):
    def __init__(self):
        super().__init__()
        self.length = 1  # DO NOT CHANGE

    def getPoints(self):
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
        for i in range(len(self.x1)):
            self.x1[i] += self.xStart
            self.y1[i] += self.yStart
            self.x2[i] += self.xStart
            self.y2[i] += self.yStart
            self.xEnd[i] += self.xStart
            self.yEnd[i] += self.yStart

    def getPoints(self):
        # Make point absolute
        if self.isRelative:
            self._makePointsAbsolute()
            self.isRelative = False

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
        self.x1 = self.x2
        self.y1 = self.y2

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
            for i in range(len(x0)):
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


class SmoothQuadraticCurve(QuadraticCurve):
    def __init__(self):
        super().__init__()
        self.length = 2  # DO NOT CHANGE
        self.xEnd = []
        self.yEnd = []
        self.prevIsQuadratic = False


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


class ClosePath(Path):
    def __init__(self):
        super().__init__()
        self.length = 0  # DO NOT CHANGE
        self.xEnd = 0
        self.yEnd = 0

    def getPoints(self):
        return [self.xStart, self.yStart, self.xEnd, self.yEnd]
