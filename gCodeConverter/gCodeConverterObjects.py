"""
gCodeConverterObjects.py - attrubute objects for "gCodeConverter.py"

"""
class Shape():
    """Shapes from svg files"""

    def __init__(self, shapeName):
        self.shapeName = shapeName
        # Needed to create object
        self.x = None
        self.y = None

        # Not needed to create object, has default

    def add(self, attribute, value):
        foundAttribute = True
        if attribute == "x":
            self.x = value
        elif attribute == "y":
            self.y = value
        else:
            foundAttribute = False
        return foundAttribute


class Rect(Shape):
    """Rectangle shape from svg files"""

    def __init__(self):
        super().__init__("rect")
        # Need to create object
        width = None
        height = None

        # Not needed to create object, has default
        self.rx = 0
        self.ry = 0

        self.fill = 0
        self.stroke = 0
        self.strokeWidth = 0

    def add(self, attribute, value):
        foundAttribute = True
        if attribute == "width":
            self.width = value
        elif attribute == "height":
            self.height = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute