"""
shape.py
Shape classes for SVG.
List of shape inheritance:

Shape
├──Rectangle
├──Ellipse
│  └──Circle
├──Polyline
│  └──Polygon
├──Line
├──Path
└──Text

Not sure where to fit in:
 - a
 - clipPath
 - defs
 - foreignObject
 - g
 - image
 - switch
 - use

Types of class fields:
 - Required: Need for shape to be drawn
 - Optional: Adds to shape, not needed
 - Later: Not currently implemented, but can be later
 - Never: Not implemented, won't be implemented
"""

from inputOutput import printd, printw, printe

# Constants used in file
# Errors/Warnings returned
SUCCESS = "success"
WARNING = "warning"
NOT_FOUND = "not found"
ERROR = "error"


class Shape:
    def __init__(self):
        # Required
        # Optional
        self.transform = ""  # str # Transformation of shape
        # Later
        self.fill = "black"  # str # Color of shape
        self.style = ""  # str # Can be used to add attributes as string
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "transform":
            self.transform = value
        elif attribute == "fill":
            self.fill = value
            foundAttribute = WARNING
        elif attribute == "style":
            self.style = value
            foundAttribute = WARNING
        else:
            foundAttribute = NOT_FOUND
        return foundAttribute


class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.x = None  # float # X position of shape
        self.y = None  # float # Y position of shape
        self.width = None  # float # Width of rectangle
        self.height = None  # float # Height of rectangle
        # Optional
        self.rx = None  # float # X radius of corner
        self.ry = None  # float # Y radius of corner
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "x":
            foundAttribute, self.x = _addFloat(value)
        if attribute == "y":
            foundAttribute, self.y = _addFloat(value)
        elif attribute == "width":
            foundAttribute, self.width = _addFloat(value)
        elif attribute == "height":
            foundAttribute, self.height = _addFloat(value)
        elif attribute == "rx":
            foundAttribute, self.rx = _addFloat(value)
        elif attribute == "ry":
            foundAttribute, self.ry = _addFloat(value)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Ellipse(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.cx = None  # float # X position of round shape
        self.cy = None  # float # Y position of round shape
        self.rx = None  # float # X radius of ellipse
        self.ry = None  # float # Y radius of ellipse
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "cx":
            foundAttribute, self.cx = _addFloat(value)
        elif attribute == "cy":
            foundAttribute, self.cy = _addFloat(value)
        elif attribute == "rx":
            foundAttribute, self.rx = _addFloat(value)
        elif attribute == "ry":
            foundAttribute, self.ry = _addFloat(value)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Circle(Ellipse):
    def __init__(self):
        super().__init__()
        # Required
        self.r = None  # float # Radius of circle
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "r":
            foundAttribute, self.r = _addFloat(value)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Polyline(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.points = None  # str # List of points
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "points":
            self.points = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Polygon(Polyline):
    def __init__(self):
        super().__init__()
        # Required
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = super().add(attribute, value)
        return foundAttribute


class Line(Shape):
    def __init__(self):
        super().__init__()
        # Required
        # Optional
        # Later
        # Never
        self.x1 = None  # float# x position of start of line
        self.y1 = None  # float# y position of start of line
        self.x2 = None  # float# x position of end of line
        self.y2 = None  # float# y position of end of line
        self.stroke = ""  # str# Color of line, no color, no line
        self.stroke_width = 1  # float# Width of line
        self.stroke_linecap = "butt"  # str# End style of line
        self.stroke_dasharray = ""  # str# Creates dashed lines

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "x1":
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
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Path(Shape):
    def __init__(self):
        super().__init__()
        # Required
        # Optional
        # Later
        # Never
        self.d = None  # str# List of instructions/points

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "d":
            self.d = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute


class Text(Shape):
    def __init__(self):
        super().__init__()
        # Required
        # Optional
        # Later
        # Never
        self.text = None  # str# Text to display

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "text":
            self.text = value
            foundAttribute = "warning"
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

""" Checks if value is a float, returning value if float """
def _addFloat(value):
    foundAttribute = SUCCESS
    floatValue = None
    try:
        floatValue = float(value)
    except ValueError as err:
        foundAttribute = ERROR
        printe(err)
    return foundAttribute, floatValue
