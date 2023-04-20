"""
shape.py
Shape classes for SVG.
List of shape inheritance:

Shape
├──Rectangle
├──Ellipse
│  └──Circle
├──Polyline
│  ├──Polygon
│  └──Line
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

class Shape():
    def __init__(self):
        self.transform = ""  #str# transformation of shape
        self.x = None  #float# x position of shape
        self.y = None  #float# y position of shape
        self.fill = "black"  #str# Color of shape
        self.style = ""  #str# Can be used to add attributes as string

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "transform":
            self.transform = value
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
        elif attribute == "fill":
            self.fill = value
            foundAttribute = "warning"
        elif attribute == "style": 
            self.style = value
            foundAttribute = "warning"
        else:
            foundAttribute = "error"
        return foundAttribute
        
class Rectangle(Shape):
    def __init__(self):
        self.width = None  #float# Width of rectangle
        self.height = None  #float# Height of rectangle
    
    def add(self, attribute, value):
        foundAttribute = "success"
        if(attribute == "width"):
            try:
                self.width = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Ellipse(Shape):
    def __init__(self):
        self.rx = None  #float# X radius of ellipse (also used in rectangle)
        self.ry = None  #float# Y radius of ellipse (also used in rectangle)

    def add(self, attribute, value):
        foundAttribute = "success"
        if(attribute == "rx"):
            try:
                self.rx = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        elif(attribute == "ry"):
            try:
                self.ry = float(value)
            except ValueError as err:
                foundAttribute = False
                printe(err)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Circle(Ellipse):
    def __init__(self):
        self.cx = None  #float# x position of round shape
        self.cy = None  #float# y position of round shape
        self.r = None  #float# Radius of circle

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "cx":
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
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Polyline(Shape):
    def __init__(self):
        self.points = None  #str# List of points
    
    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "points":
            self.points = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Polygon(Polyline):
    def __init__(self):
        self.points = None

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "points":
            self.points = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Line(Polyline):
    def __init__(self):
        self.x1 = None  #float# x position of start of line
        self.y1 = None  #float# y position of start of line
        self.x2 = None  #float# x position of end of line
        self.y2 = None  #float# y position of end of line
        self.stroke = ""  #str# Color of line, no color, no line
        self.stroke_width = 1  #float# Width of line
        self.stroke_linecap = "butt"  #str# End style of line
        self.stroke_dasharray = ""  #str# Creates dashed lines

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
        self.d = None  #str# List of instructions/points

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "d":
            self.d = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

class Text(Shape):
    def __init__(self):
        self.text = None  #str# Text to display

    def add(self, attribute, value):
        foundAttribute = "success"
        if attribute == "text":
            self.text = value
            foundAttribute = "warning"
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute