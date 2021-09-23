"""
gCodeConverterObjects.py - attrubute objects for "gCodeConverter.py"

NOTE: Due to python not accepting hyphens "-" as valid variables,
        all attribute with hyphens have been replaced with underscores "_"

"""
from typing import Tuple


class Shape():
    """Shapes from svg files"""

    def __init__(self, shapeName):
        self.shapeName = shapeName
        # Hierarchy of shapes:
        # General
        # General Shape
        #   Rectangle (rect)

        # Needed for General
        self.x = None  #int# x position of shape
        self.y = None  #int# y position of shape

        # Needed for General Shape
        # Needed for Rectangle
        self.width = None  #int# Width of shape
        self.height = None  #int# Height of shape


        # Not needed to create object, has default value
        # For General
        self.style = ""  #str# Can be used to add attributes as string

        # Stroke is properties of the line
        self.stroke = ""  #str# Color of line, no color, no line
        self.stroke_width = 1  #int# Width of line
        self.stroke_linecap = "butt"  #str# End style of line
        self.stroke_dasharray = ""  #str# Creates dashed lines

        # For General Shape
        self.fill = "black"  #str# Color of shape

        # For Rectangle
        self.rx = 0  #int# Curve indentation on x-axies of corners
        self.ry = 0  #int# Curve indentation on y-axies of corners


    def add(self, attribute, value):
        """Adds attribute to shape"""
        # Is in same order as "__init__" function
        foundAttribute = True
        if attribute == "x":
            try:
                self.x = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "y":
            try:
                self.y = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "width":
            try:
                self.width = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "height":
            try:
                self.height = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "style": 
            self.style = value
        elif attribute == "stroke":
            self.stroke = value
        elif attribute == "stroke-width":
            try:
                self.stroke_width = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "stroke-linecap":
            self.stroke_linecap = value
        elif attribute == "stroke-dasharray":
            self.stroke_dasharray = value
        elif attribute == "fill":
            self.fill = value
        elif attribute == "rx":
            try:
                self.rx = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err)
        elif attribute == "ry":
            try:
                self.ry = int(value)
            except ValueError as err:
                foundAttribute = False
                print(err) 
        else:
            foundAttribute = False
        return foundAttribute
    
    def checkShape(self):
        validObject = False
        if self.shapeName == "rect":
            if self.x >= 0 \
                and self.y >= 0 \
                and self.width >= 0 \
                and self.height >= 0:
                    validObject = True
    

        return validObject
