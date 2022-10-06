"""
classes.py - classes, just a bunch of classes

NOTE: Due to python not accepting hyphens "-" as valid variables,
        all attribute with hyphens have been replaced with underscores "_"

"""
# Libraries
import math
from turtle import pendown
import constants
from IO import printe, printw, printd, printp

"""Shapes with attrubutes from svg files"""
class Shape():

    """Constructor created blank shape to be added on later"""
    def __init__(self, shapeName):
        self.shapeName = shapeName
        # Hierarchy of shapes:
        # General
        #   Line (line)
        #   Polyline (polyline)
        #   Polygon (polygon)
        # General Shape
        #   Rectangle (rect)
        #   Circle (circle)
        #   Ellipse (ellipse)
        # Path (path)
        # Text (text)

        # Needed for General
        self.transform = ""  #str# transformation of shape
        self.x = None  #float# x position of shape
        self.y = None  #float# y position of shape

        # Needed for Line
        self.x1 = None  #float# x position of start of line
        self.y1 = None  #float# y position of start of line
        self.x2 = None  #float# x position of end of line
        self.y2 = None  #float# y position of end of line

        # Needed for Polyline and Polygon
        self.points = None  #str# List of points

        # Needed for General Shape
        # Needed for Rectangle
        self.width = None  #float# Width of rectangle
        self.height = None  #float# Height of rectangle

        # Needed for Circle
        self.cx = None  #float# x position of round shape
        self.cy = None  #float# y position of round shape
        self.r = None  #float# Radius of circle

        # Needed for Ellipse
        self.rx = None  #float# X radius of ellipse (also used in rectangle)
        self.ry = None  #float# Y radius of ellipse (also used in rectangle)

        # Needed for Path
        self.d = None  #str# List of instructions/points

        # Needed for Text
        self.text = None  #str# Text to display

        # Not needed to create object, has default value
        # For General
        self.style = ""  #str# Can be used to add attributes as string

        # Stroke is properties of the line
        self.stroke = ""  #str# Color of line, no color, no line
        self.stroke_width = 1  #float# Width of line
        self.stroke_linecap = "butt"  #str# End style of line
        self.stroke_dasharray = ""  #str# Creates dashed lines

        # For General Shape
        self.fill = "black"  #str# Color of shape


    """Adds attribute to shape"""
    def add(self, attribute, value):
        # Is in same order as "__init__" function
        foundAttribute = "success"
        if attribute == "transform":
            self.transform = value
        elif attribute == "x1":
            try:
                self.x1 = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "y1":
            try:
                self.y1 = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "x2":
            try:
                self.x2 = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "y2":
            try:
                self.y2 = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "points":
            self.points = value
        elif attribute == "x":
            try:
                self.x = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "y":
            try:
                self.y = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "width":
            try:
                self.width = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "height":
            try:
                self.height = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "cx":
            try:
                self.cx = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "cy":
            try:
                self.cy = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "r":
            try:
                self.r = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "rx":
            try:
                self.rx = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "ry":
            try:
                self.ry = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "d":
            self.d = value
        elif attribute == "text":
            self.text = value
            foundAttribute = "warning"
        elif attribute == "style": 
            self.style = value
            foundAttribute = "warning"
        elif attribute == "stroke":
            self.stroke = value
            foundAttribute = "warning"
        elif attribute == "stroke-width":
            try:
                self.stroke_width = float(value)
                foundAttribute = "warning"
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif attribute == "stroke-linecap":
            self.stroke_linecap = value
            foundAttribute = "warning"
        elif attribute == "stroke-dasharray":
            self.stroke_dasharray = value
            foundAttribute = "warning"
        elif attribute == "fill":
            self.fill = value
            foundAttribute = "warning"
        else:
            foundAttribute = "error"
        return foundAttribute
    
    """Checks if a shape is valid"""
    def checkShape(self):
        validObject = False
        if self.shapeName == "line":
            if self.x1 != None \
                and self.y1 != None \
                and self.x2 != None \
                and self.y2 != None:
                    validObject = True
        if self.shapeName == "polyline":
            if self.points != "":
                validObject = True
        if self.shapeName == "polygon":
            if self.points != "":
                validObject = True
        if self.shapeName == "rect":
            if self.x != None \
                and self.y != None \
                and self.width >= 0 \
                and self.height >= 0:
                    validObject = True
        if self.shapeName == "circle":
            if self.cx != None \
                and self.cy != None \
                and self.r >= 0:
                    validObject = True
        if self.shapeName == "ellipse":
            if self.cx != None \
                and self.cy != None \
                and self.rx >= 0 \
                and self.ry >= 0:
                    validObject = True
        if self.shapeName == "path":
            if self.d != "":
                validObject = True
        if self.shapeName == "text":
            if self.x != None \
                and self.y != None \
                and self.text != None:
                    validObject = True
        
        return validObject


"""Class for holding list data from pased objects"""
class PointsListObj():

    """Constructor created blank list to be added to"""
    def __init__(self):
        self.pointsList = []
        self.rasterArray = []
        self.curShape = []

    """Adds points to list"""
    def addPoint(self, sel, xPos=0, yPos=0):
        if sel == "point":
            self.pointsList.append(xPos)
            self.pointsList.append(yPos)
            self.curShape.append(xPos)
            self.curShape.append(yPos)
        elif sel == "up" or sel == "down":
            self.pointsList.append(sel)
            self.pointsList.append(sel)
            self.curShape.append(sel)
            self.curShape.append(sel)
        else:
            printe("addPoint error, \"" + str(sel) + "\" not valid selection")
            raise TypeError("addPoint error, \"" + str(sel) + "\" not valid selection")
    
    """Adds points in arc shape with radius r, starting at sDegree"""
    def draw_arc(self, xPos, yPos, rx, ry, sDegree, degree, res):
        sRad = sDegree * math.pi/180  # Start pos
        rad = degree * math.pi/180  # Move amount
        for step in range(res+1):
            x = xPos + rx * math.cos((rad/res)*step + sRad)
            y = yPos + ry * math.sin((rad/res)*step + sRad)
            self.addPoint("point", x, y)
    
    """Adds plo on end of plo"""
    def addPlo(self, plo):
        for item in plo.pointsList:
            self.pointsList.append(item)
            self.curShape.append(item)
    
    """Creates new shape to be rastered"""
    def newShape(self):
        curShape = []

    """Rasters shape onto array"""
    def raster(self):
        maxPoints = self.getMaxPoints(self.curShape)
        # Adjust for origin not being at 00
        xOffset = -maxPoints[2]
        yOffset = -maxPoints[3]

        # Create blank array
        rasterArray = []
        for i in range(int(maxPoints[0]-maxPoints[2])+1):
            rasterArray.append([])
            for j in range(int(maxPoints[1]-maxPoints[3])+1):
                rasterArray[i].append(0)
        
        # Add points to array
        printd(self.pointsList)
        curX = 0
        curY = 0
        nextX = 0
        nextY = 0
        penDown = False
        for i in range(2, len(self.pointsList), 2):
            cur = self.pointsList[i]
            printd(cur)
            if( cur == "up" ):
                penDown = False
                if( i+2 < len(self.pointsList) ):
                    curX = self.pointsList[i+2]
                    curY = self.pointsList[i+3]
                    nextX = self.pointsList[i+2]
                    nextY = self.pointsList[i+3]
            elif( cur == "down" ):
                penDown = True
                if( i+2 < len(self.pointsList) ):
                    nextX = self.pointsList[i+2]
                    nextY = self.pointsList[i+3]
            else:
                nextX = self.pointsList[i+0]
                nextY = self.pointsList[i+1]

            if( pendown ):
                curX = float(curX)
                curY = float(curY)
                nextX = float(nextX)
                nextY = float(nextY)
                printd(str(curX) + "," + str(curY))
                xStep = (nextX - curX)/constants.CURVE_SAMPLE_POINTS
                yStep = (nextY - curY)/constants.CURVE_SAMPLE_POINTS
                for step in range(0, constants.CURVE_SAMPLE_POINTS+1, 1):
                    curX += xStep
                    curY += yStep
                    printd(str(curX) + "," + str(curY))
                    # add points to array

            curX = nextX
            curY = nextY


        for row in rasterArray:
            printd(row)
    
    def getMaxPoints(self, pointsList):
        maxXPoint = 0
        maxYPoint = 0
        minXPoint = 0
        minYPoint = 0
        i = 0
        while i < len(pointsList) - 2:
            if pointsList[i] != "up" and pointsList[i] != "down":
                if pointsList[i] > maxXPoint:
                    maxXPoint = pointsList[i]
                if pointsList[i+1] > maxYPoint:
                    maxYPoint = pointsList[i+1]
                if pointsList[i] < minXPoint:
                    minXPoint = pointsList[i]
                if pointsList[i+1] < minYPoint:
                    minYPoint = pointsList[i+1]
            i += 2
        
        return maxXPoint, maxYPoint, minXPoint, minYPoint        

            