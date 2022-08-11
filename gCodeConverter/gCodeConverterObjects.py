"""
gCodeConverterObjects.py - objects, just a bunch of objects

NOTE: Due to python not accepting hyphens "-" as valid variables,
        all attribute with hyphens have been replaced with underscores "_"

"""
# Libraries
import math
from fileIO import printe, printw, printd, printp

"""Shapes with attrubutes from svg files"""
class Shape():

    """Constructor created blank shape to be added on later"""
    def __init__(self, shapeName):
        self.shapeName = shapeName
        # Hierarchy of shapes:
        # General
        # General Shape
        #   Rectangle (rect)
        #   Circle (circle)
        #   Ellipse (ellipse)
        # Path (path)

        # Needed for General

        # Needed for General Shape
        # Needed for Rectangle
        self.x = None  #float# x position of rectangle
        self.y = None  #float# y position of rectangle
        self.width = None  #float# Width of rectangle
        self.height = None  #float# Height of rectangle

        # Needed for Circle
        self.cx = None  #float# x position of round shape
        self.cy = None  #float# x position of round shape
        self.r = None  #float# Radius of circle

        # Needed for Ellipse
        self.rx = None  #float# X radius of ellipse (also used in rectangle)
        self.ry = None  #float# Y radius of ellipse (also used in rectangle)

        # Needed for Path
        self.d = None

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
        if attribute == "x":
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
        if self.shapeName == "rect":
            if self.x >= 0 \
                and self.y >= 0 \
                and self.width >= 0 \
                and self.height >= 0:
                    validObject = True
        if self.shapeName == "circle":
            if self.cx >= 0 \
                and self.cy >= 0 \
                and self.r >= 0:
                    validObject = True
        if self.shapeName == "ellipse":
            if self.cx >= 0 \
                and self.cy >= 0 \
                and self.rx >= 0 \
                and self.ry >= 0:
                    validObject = True
        if self.shapeName == "line":
            pass
            #Add min requirement here
            #e.g. needs at least start and end points
        #Add other shapes here ####################################################################
        if self.shapeName == "path":
            if self.d != "":
                validObject = True
        
        return validObject


"""Object for holding list data from pased objects"""
class pointsListObj():

    """Constructor created blank list to be added to"""
    def __init__(self):
        self.pointsList = []

    """Adds points to list"""
    def addPoint(self, sel, xPos=0, yPos=0):
        if sel == "point":
            self.pointsList.append(xPos)
            self.pointsList.append(yPos)
        elif sel == "up" or sel == "down":
            self.pointsList.append(sel)
            self.pointsList.append(sel)
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