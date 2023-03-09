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
