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

import constants
import shapePath
import pointList
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
        self.id = ""  # str # ID for shape, internal use only
        # Later
        self.fill = "black"  # str # Color of shape
        self.style = ""  # str # Can be used to add attributes as string
        self.stroke = ""  # str # Color of line, no color, no line
        self.stroke_dasharray = ""  # str # Creates dashed lines
        # Never
        self.stroke_width = 1  # float # Width of line
        self.stroke_linecap = "butt"  # str # End style of line
        self.stroke_linejoin = "miter"  # str # Line bend style
        self.stroke_miterlimit = 4  # float # Miter line bend style

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "transform":
            self.transform = value
        elif attribute == "id":
            self.id = value
            foundAttribute = WARNING
        elif attribute == "fill":
            self.fill = value
            foundAttribute = WARNING
        elif attribute == "style":
            self.style = value
            foundAttribute = WARNING
        elif attribute == "stroke":
            self.stroke = value
            foundAttribute = WARNING
        elif attribute == "stroke-dasharray":
            self.stroke_dasharray = value
            foundAttribute = WARNING
        elif attribute == "stroke-width":
            foundAttribute, self.stroke_width = _addFloat(value)
            foundAttribute = WARNING
        elif attribute == "stroke-linecap":
            self.stroke_linecap = value
            foundAttribute = WARNING
        elif attribute == "stroke-linejoin":
            self.stroke_linecap = value
            foundAttribute = WARNING
        elif attribute == "stroke-miterlimit":
            foundAttribute = self.stroke_linecap = _addFloat(value)
            foundAttribute = WARNING
        else:
            foundAttribute = NOT_FOUND
        return foundAttribute

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        # Optional
        return isValid

    """Returns name of shape with id"""
    def name(self):
        outString = str(type(self)).split("'")[1]
        if self.id != "":
            outString += " (" + str(self.id) + ")"
        return outString

    """Transforms points from shape with respect to transform attribute"""
    def transformPoints(self, pointList):
        # not implemented yet
        return pointList


class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.x = None  # float # X position of shape
        self.y = None  # float # Y position of shape
        self.width = None  # float # Width of rectangle
        self.height = None  # float # Height of rectangle
        # Optional
        self.rx = 0  # float # X radius of corner
        self.ry = 0  # float # Y radius of corner
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "x":
            foundAttribute, self.x = _addFloat(value)
        elif attribute == "y":
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

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.x is None:
            isValid = False
        elif self.y is None:
            isValid = False
        elif self.width <= 0:
            isValid = False
        elif self.height <= 0:
            isValid = False
        # Optional
        if isValid:
            if 0 > self.rx > self.width / 2:
                isValid = False
            if 0 > self.ry > self.height / 2:
                isValid = False
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        pl = pointList.PointList()
        pl.penUp()
        pl.addPoint(self.x + self.rx, self.y)
        pl.penDown()
        if self.rx + self.ry != 0:
            pl.addPoint(self.x + self.width - self.rx, self.y)
            pl.drawArc(self.x + self.width - self.rx, self.y + self.ry, self.rx, self.ry, -90, 90,
                       int(constants.CURVE_SAMPLE_POINTS / 4))
            pl.addPoint(self.x + self.width, self.y + self.height - self.ry)
            pl.drawArc(self.x + self.width - self.rx, self.y + self.height - self.ry, self.rx, self.ry, 0, 90,
                       int(constants.CURVE_SAMPLE_POINTS / 4))
            pl.addPoint(self.x + self.rx, self.y + self.height)
            pl.drawArc(self.x + self.rx, self.y + self.height - self.ry, self.rx, self.ry, 90, 90,
                       int(constants.CURVE_SAMPLE_POINTS / 4))
            pl.addPoint(self.x, self.y + self.ry)
            pl.drawArc(self.x + self.rx, self.y + self.ry, self.rx, self.ry, -180, 90,
                       int(constants.CURVE_SAMPLE_POINTS / 4))
        else:
            pl.addPoint(self.x + self.width, self.y)
            pl.addPoint(self.x + self.width, self.y + self.height)
            pl.addPoint(self.x, self.y + self.height)
            pl.addPoint(self.x, self.y)
        pl.penUp()
        return pl


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

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.cx is None:
            isValid = False
        elif self.cy is None:
            isValid = False
        elif self.rx <= 0:
            isValid = False
        elif self.ry <= 0:
            isValid = False
        # Optional
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        pl = pointList.PointList()

        pl.penUp()
        pl.addPoint(self.cx + self.rx, self.cy)
        pl.penDown()
        pl.drawArc(self.cx, self.cy, self.rx, self.ry, 0, 360, constants.CURVE_SAMPLE_POINTS)
        pl.penUp()

        pl.penUp()
        return pl


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

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.r <= 0:
            isValid = False
        # Optional
        # Parent
        if isValid:
            self.rx = self.r
            self.ry = self.r
            isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        return super().getPoints()


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

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.points is None:
            isValid = False
        # Optional
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    
    def getPoints(self):
        pl = pointList.PointList()

        floatList = _getFloatPoints(self.points)

        print('FloatList rest', floatList[2:])

        pl.penUp()
        pl.addPoint(floatList[0], floatList[1])
        pl.penDown()
        for i in range(int(len(floatList[2:])/2)): 
            pl.addPoint(floatList[2+2*i], floatList[3+2*i])
        #pl.extend(floatList[2:])
        pl.penUp()
        return pl


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

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        # Optional
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        pl = pointList.PointList()

        floatList = _getFloatPoints(self.points)

        pl.penUp()
        pl.addPoint(floatList[0], floatList[1])
        pl.penDown()
        pl.extend(floatList[2:])
        pl.addPoint(floatList[0], floatList[1])
        pl.penUp()
        return pl
    def getPoints(self):
        pl = pointList.PointList()

        floatList = _getFloatPoints(self.points)

        #pl.penUp()
        #pl.addPoint(floatList[0], floatList[1])
        #pl.penDown()
        #for i in range(int(len(floatList[2:])/2)): 
        #    pl.addPoint(floatList[2+2*i], floatList[3+2*i])
        #pl.extend(floatList[2:])
        
        pl = super().getPoints()
        pl.penDown()
        pl.addPoint(floatList[0], floatList[1])
        pl.penUp()
        return pl


class Line(Polyline):
    def __init__(self):
        super().__init__()
        # Require
        self.x1 = None  # float # X position of start of line
        self.y1 = None  # float # Y position of start of line
        self.x2 = None  # float # X position of end of line
        self.y2 = None  # float # Y position of end of line
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "x1":
            foundAttribute, self.x1 = _addFloat(value)
        elif attribute == "y1":
            foundAttribute, self.y1 = _addFloat(value)
        elif attribute == "x2":
            foundAttribute, self.x2 = _addFloat(value)
        elif attribute == "y2":
            foundAttribute, self.y2 = _addFloat(value)
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.x1 is None:
            isValid = False
        elif self.y1 is None:
            isValid = False
        if self.x2 is None:
            isValid = False
        elif self.y2 is None:
            isValid = False
        # Optional
        # Parent
        if isValid:
            self.points = str(self.x1) + "," + str(self.y1) + "," + str(self.x2) + "," + str(self.y2)
            isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        return super().getPoints()


class Path(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.d = None  # str # List of instructions/points
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "d":
            self.d = value
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.d is None:
            isValid = False
        # Optional
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        pl = pointList.PointList()

        PATH_COMMAND_LENGTH = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}
        FULL_PATH_COMMANDS = {"M": 2, "L": 2, "H": 2, "V": 2, "C": 8, "S": 8, "Q": 6, "T": 6, "A": 9, "Z": 0}

        PATH_COMMANDS = ["M", "L", "H", "V", "C", "S", "Q", "T", "A", "Z"]

        # Split path into commands of strings
        curCommandString = ""
        commandStringList = []
        for char in self.d:
            if char.upper() in PATH_COMMANDS:
                commandStringList.append(curCommandString.strip())
                curCommandString = ""
            curCommandString += char
        commandStringList.append(curCommandString)
        commandStringList = commandStringList[1:]
        printd(commandStringList)

        # Splits strings into commands and point list
        commandPointList = []
        for commandString in commandStringList:
            commandName = commandString[0]
            pointString = commandString[1:]

            floatList = _getFloatPoints(pointString)

            commandPointList.append((commandName, floatList))
        printd(commandPointList)

        # Create path objects from points
        TYPE = 0
        POINT = 1
        commandPathList = []
        xStart = commandPointList[0][POINT][0]
        yStart = commandPointList[0][POINT][1]
        for cmd in commandPointList:
            newCommand = None
            if cmd[TYPE].upper() == "M":
                newCommand = shapePath.Move()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength,  cmdLength):
                    newCommand.x.append(cmd[POINT][i])
                    newCommand.y.append(cmd[POINT][i+1])
            elif cmd[TYPE].upper() == "L":
                newCommand = shapePath.Line()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.x.append(cmd[POINT][i])
                    newCommand.y.append(cmd[POINT][i + 1])
            elif cmd[TYPE].upper() == "H":
                newCommand = shapePath.HorizontalLine()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.x.append(cmd[POINT][i])
            elif cmd[TYPE].upper() == "V":
                newCommand = shapePath.VerticalLine()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.y.append(cmd[POINT][i])
            elif cmd[TYPE].upper() == "C":
                newCommand = shapePath.CubicCurve()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.x1.append(cmd[POINT][i])
                    newCommand.y1.append(cmd[POINT][i + 1])
                    newCommand.x2.append(cmd[POINT][i + 2])
                    newCommand.y2.append(cmd[POINT][i + 3])
                    newCommand.xEnd.append(cmd[POINT][i + 4])
                    newCommand.yEnd.append(cmd[POINT][i + 5])
            elif cmd[TYPE].upper() == "S":
                newCommand = shapePath.SmoothCubicCurve()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.x2.append(cmd[POINT][i])
                    newCommand.y2.append(cmd[POINT][i + 1])
                    newCommand.xEnd.append(cmd[POINT][i + 2])
                    newCommand.yEnd.append(cmd[POINT][i + 3])
            elif cmd[TYPE].upper() == "Q":
                newCommand = shapePath.QuadraticCurve()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.x1.append(cmd[POINT][i])
                    newCommand.y1.append(cmd[POINT][i + 1])
                    newCommand.xEnd.append(cmd[POINT][i + 2])
                    newCommand.yEnd.append(cmd[POINT][i + 3])
            elif cmd[TYPE].upper() == "T":
                newCommand = shapePath.SmoothQuadraticCurve()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.xEnd.append(cmd[POINT][i])
                    newCommand.yEnd.append(cmd[POINT][i + 1])
            elif cmd[TYPE].upper() == "A":
                newCommand = shapePath.Arc()
                cmdLength = newCommand.length
                totalCmdLength = len(cmd[POINT])
                for i in range(0, totalCmdLength, cmdLength):
                    newCommand.rx.append(cmd[POINT][i])
                    newCommand.ry.append(cmd[POINT][i + 1])
                    newCommand.rotation.append(cmd[POINT][i + 2])
                    newCommand.largeArcFlag.append(cmd[POINT][i + 3])
                    newCommand.sweepFlag.append(cmd[POINT][i + 4])
                    newCommand.xEnd.append(cmd[POINT][i + 5])
                    newCommand.yEnd.append(cmd[POINT][i + 6])
            elif cmd[TYPE].upper() == "Z":
                newCommand = shapePath.ClosePath()
                newCommand.xEnd = xStart
                newCommand.yEnd = yStart
            else:
                printe("Path \"" + str(cmd[TYPE]) + "\" type not found")
            if newCommand is not None:
                if cmd[TYPE] in PATH_COMMANDS:
                    newCommand.isRelative = False
                else:
                    newCommand.isRelative = True
            commandPathList.append(newCommand)

        # Get points
        pl = pointList.PointList()
        xPrev = 0
        yPrev = 0
        xPrev2 = 0
        yPrev2 = 0
        prevCmd = "Z"
        for cmd in commandPathList:
            # Set previous points
            cmd.xStart = xPrev
            cmd.yStart = yPrev
            if type(cmd) in [shapePath.CubicCurve, shapePath.SmoothCubicCurve] and prevCmd == "C":
                cmd.xPrev2 = xPrev2
                cmd.yPrev2 = yPrev2
                cmd.prevIsCubic = True
            if type(cmd) in [shapePath.QuadraticCurve, shapePath.SmoothQuadraticCurve] and prevCmd == "Q":
                cmd.xPrev2 = xPrev2
                cmd.yPrev2 = yPrev2
                cmd.prevIsQuadratic = True


            # Get points
            
            curPointList = cmd.getPoints()
            if type(cmd) == shapePath.Move:
                pl.penUp()
            else:
                pl.penDown()
            
            if type(cmd) == shapePath.Arc:
                pl.drawPathArc(cmd.xStart, cmd.yStart, cmd.rx[0], cmd.ry[0], cmd.rotation[0], int(cmd.largeArcFlag[0]), int(cmd.sweepFlag[0]), cmd.xEnd[0], cmd.yEnd[0])
                #pl.drawArc(curPointList[0], curPointList[1], int(cmd.rx[0]), int(cmd.ry[0]), 10, 0, 130)
            else:
                for i in range(int(len(curPointList)/2)): 
                    pl.addPoint(curPointList[0+2*i], curPointList[1+2*i])
                    pl.list[-1].cat = pointList.PointCategory.Command
            #pl.extend(curPointList)
            #pl.addPoint(curPointList[0], curPointList[1])

            # Get previous points
            xPrev = pl.list[-1].x
            yPrev = pl.list[-1].y
            #xPrev = curPointList[-2]
            #yPrev = curPointList[-1]
            prevCmd = "Z"
            if type(cmd) in [shapePath.CubicCurve, shapePath.SmoothCubicCurve]:
                xPrev2 = cmd.x2[-1]
                yPrev2 = cmd.y2[-1]
                prevCmd = "C"
            if type(cmd) in [shapePath.QuadraticCurve, shapePath.SmoothQuadraticCurve]:
                xPrev2 = cmd.x1[-1]
                yPrev2 = cmd.y1[-1]
                prevCmd = "Q"

        pl.penUp()
        return pl


        '''
        # Split commands into points
        startPoint = [0, 0]
        prevCommandPoints = [0, 0]
        prevCommandType = ""
        commandPointsAdj = [0, 0, 0, 0]
        for command in pathShape:
            command = command.strip()
            commandType = command[0]
            # Find points in string
            commandPoints = [""]
            commandPointsIndex = 0
            for char in command[1:]:
                if char == "," or char == " " or char == "-":
                    commandPointsIndex += 1
                    if char == "-":
                        commandPoints.append(char)
                    else:
                        commandPoints.append("")
                else:
                    commandPoints[commandPointsIndex] += char
            while "" in commandPoints:
                commandPoints.remove("")
            for index, point in enumerate(commandPoints):
                commandPoints[index] = float(point)
            # Number of commands per commands
            commandLength = PATH_COMMANDS[commandType.upper()]
            if commandLength != 0:
                # Relative vs absolute points
                moveRelative = False
                if commandType not in PATH_COMMANDS.keys():
                    moveRelative = True
                # Pre-calculation of points
                commandPointsAdjList = []
                commandPointsAdj = [None] * FULL_PATH_COMMANDS[commandType.upper()]
                commandNumOff = 0
                additionalPoints = False
                printd("\n" + str(commandType))

                for commandPointNum in range(len(commandPoints)):
                    # Update previous command data if new iteration
                    if commandPointNum % commandLength == 0:
                        # Previous point "clean up"
                        if commandPointNum != 0:
                            if additionalPoints:
                                commandPointsAdj[2] = commandPointsAdj[4]
                                commandPointsAdj[3] = commandPointsAdj[5]
                            prevCommandPoints = commandPointsAdj
                            prevCommandType = commandType
                            commandPointsAdjList.append(commandPointsAdj)
                            commandPointsAdj = [None] * FULL_PATH_COMMANDS[commandType.upper()]
                            commandNumOff = int(-PATH_COMMANDS[commandType.upper()] * commandPointNum / commandLength)

                        # Current point extra additions
                        if commandType.upper() == "M":
                            startPoint = prevCommandPoints[-2:-1]
                        elif commandType.upper() == "H":
                            commandPointsAdj[1] = prevCommandPoints[-1]
                        elif commandType.upper() == "V":
                            commandPointsAdj[0] = prevCommandPoints[-2]
                            commandNumOff += 1
                        elif commandType.upper() == "C":
                            commandPointsAdj[0] = prevCommandPoints[-2]
                            commandPointsAdj[1] = prevCommandPoints[-1]
                            commandNumOff += 2
                        elif commandType.upper() == "S":
                            commandPointsAdj[0] = prevCommandPoints[-2]
                            commandPointsAdj[1] = prevCommandPoints[-1]
                            if (prevCommandType.upper() in ["C", "S"]):
                                commandPointsAdj[2] = prevCommandPoints[-2] + (
                                            prevCommandPoints[-2] - prevCommandPoints[-4])
                                commandPointsAdj[3] = prevCommandPoints[-1] + (
                                            prevCommandPoints[-1] - prevCommandPoints[-3])
                            else:
                                additionalPoints = True
                            commandNumOff += 4
                        elif commandType.upper() == "Q":
                            commandPointsAdj[0] = prevCommandPoints[-2]
                            commandPointsAdj[1] = prevCommandPoints[-1]
                            commandNumOff += 2
                        elif commandType.upper() == "T":
                            commandPointsAdj[0] = prevCommandPoints[-2]
                            commandPointsAdj[1] = prevCommandPoints[-1]
                            if (prevCommandType.upper() in ["Q", "T"]):
                                commandPointsAdj[2] = prevCommandPoints[-2] + (
                                            prevCommandPoints[-2] - prevCommandPoints[-4])
                                commandPointsAdj[3] = prevCommandPoints[-1] + (
                                            prevCommandPoints[-1] - prevCommandPoints[-3])
                            else:
                                additionalPoints = True
                            commandNumOff += 4

                        ## Need add "A" (arc)

                    commandPointsAdj[commandPointNum + commandNumOff] = prevCommandPoints[
                                                                            (commandPointNum % 2) - 2] * moveRelative + \
                                                                        commandPoints[commandPointNum]
                    if commandType == "v":
                        commandPointsAdj[commandPointNum + commandNumOff] = prevCommandPoints[(1) - 2] * moveRelative + \
                                                                            commandPoints[commandPointNum]

                # Previous point "clean up"
                if additionalPoints:
                    commandPointsAdj[2] = commandPointsAdj[4]
                    commandPointsAdj[3] = commandPointsAdj[5]
                commandPointsAdjList.append(commandPointsAdj)
                prevCommandPoints = commandPointsAdj
                prevCommandType = commandType
                # Starting point of path
                if commandType.upper() == "M":
                    startPoint = commandPointsAdjList[0][0:2]

                printd(commandPoints)
                printd(commandPointsAdjList)

            # Plot points from commands points
            for iterCommandPoints in commandPointsAdjList:
                if commandType.upper() == "M":
                    printd("Move")
                    plo.addPoint("up")
                    plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                    plo.addPoint("down")
                elif commandType.upper() == "L":
                    printd("Line")
                    plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                elif commandType.upper() == "H":
                    printd("Horizontal line")
                    plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                elif commandType.upper() == "V":
                    printd("Vertical line")
                    plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                elif commandType.upper() in ["C", "S"]:
                    printd("Curve/Smooth Curve")
                    for i in range(0, CURVE_SAMPLE_POINTS + 1, 1):
                        i /= CURVE_SAMPLE_POINTS
                        xPoint = (((1 - i) ** 3) * iterCommandPoints[0]) + (
                                    3 * i * ((1 - i) ** 2) * (iterCommandPoints[2])) + (
                                             3 * (i ** 2) * (1 - i) * (iterCommandPoints[4])) + (
                                             i ** 3 * (iterCommandPoints[6]))
                        yPoint = (((1 - i) ** 3) * iterCommandPoints[1]) + (
                                    3 * i * ((1 - i) ** 2) * (iterCommandPoints[3])) + (
                                             3 * (i ** 2) * (1 - i) * (iterCommandPoints[5])) + (
                                             i ** 3 * (iterCommandPoints[7]))
                        plo.addPoint("point", xPoint, yPoint)
                elif commandType.upper() in ["Q", "T"]:
                    printd("Quadratic Curve/Smooth Quadratic curve")
                    for i in range(0, CURVE_SAMPLE_POINTS + 1, 1):
                        i /= CURVE_SAMPLE_POINTS
                        xPoint = (((1 - i) ** 2) * iterCommandPoints[0]) + (
                                    2 * i * (1 - i) * (iterCommandPoints[2])) + (i ** 2 * (iterCommandPoints[4]))
                        yPoint = (((1 - i) ** 2) * iterCommandPoints[1]) + (
                                    2 * i * (1 - i) * (iterCommandPoints[3])) + (i ** 2 * (iterCommandPoints[5]))
                        plo.addPoint("point", xPoint, yPoint)
                elif commandType.upper() == "A":
                    printe("Arc to be added ####################################################")
                elif commandType.upper() == "Z":
                    printd("Close path")
                    plo.addPoint("point", startPoint[0], startPoint[1])

        printd()

        pl.penUp()
        '''
        return pl


class Text(Shape):
    def __init__(self):
        super().__init__()
        # Required
        self.text = None  # str # Text to display
        # Optional
        # Later
        # Never

    def add(self, attribute, value):
        foundAttribute = SUCCESS
        if attribute == "text":
            self.text = value
            foundAttribute = WARNING
        else:
            foundAttribute = super().add(attribute, value)
        return foundAttribute

    """Checks if shape has required attributes and attributes are valid"""
    def checkShape(self):
        isValid = True
        # Required
        if self.text is None:
            isValid = False
        # Optional
        # Parent
        isValid *= super().checkShape()
        return isValid

    """Creates points based of attributes of shape"""
    def getPoints(self):
        pl = pointList.PointList()

        printw("Text Shape not implemented")
        printd("Text: " + self.text)

        return pl


"""Checks if value is a float, returning value if float"""
def _addFloat(value):
    foundAttribute = SUCCESS
    floatValue = None
    try:
        floatValue = float(value)
    except ValueError as err:
        foundAttribute = ERROR
        printe(err)
    return foundAttribute, floatValue

"""Gets points from string"""
def _getFloatPoints(pointString):
    pointList = []
    curPoint = ""
    for char in pointString:
        if char == "," or char == " " or char == "-":
            curPoint = curPoint.strip()
            if curPoint != "" and curPoint != "-":
                pointList.append(float(curPoint))
            if char == "-":
                curPoint = char
            else:
                curPoint = ""
        else:
            curPoint += char
    curPoint = curPoint.strip()
    if curPoint != "" and curPoint != "-":
        pointList.append(float(curPoint))
    return pointList

