"""
parseObjectToPoints.py - parse object data into points list

"""
# Libraries
import math
from classes import PointsListObj
from IO import printe, printw, printd, printp
from constants import CURVE_SAMPLE_POINTS, ROUND_DECIMAL_POINTS

"""Create Line"""
def makeLine(plo, i):
    plo.addPoint("up")
    plo.addPoint("point", i.x1, i.y1)
    plo.addPoint("down")
    plo.addPoint("point", i.x2, i.y2)
    plo.addPoint("up")

"""Create Polyline and Polygon"""
def makePolyline(plo, i):
    # Get line points as floats
    pointInt = []
    curPoint = ""
    for char in i.points:
        if char == "," or char == " " or (char == "-" and curPoint != ""):
            pointInt.append(float(curPoint))
            if char == "-":
                curPoint = char
            else:
                curPoint = ""
        else:
            curPoint += char
    pointInt.append(float(curPoint))
    
    # Plot points
    plo.addPoint("up")
    plo.addPoint("point", pointInt[0], pointInt[1])
    plo.addPoint("down")
    for pointIndex in range(2, len(pointInt), 2):
        plo.addPoint("point", pointInt[pointIndex], pointInt[pointIndex+1])
    if i.shapeName == "polygon":
        plo.addPoint("point", pointInt[0], pointInt[1])
    plo.addPoint("up")

"""Create Rectangle"""
def makeRect(plo, i):
    if i.rx == None:
        i.rx = 0
    if i.ry == None:
        i.ry = 0
    if i.rx > i.width/2:
        i.rx = i.width/2
    if i.ry > i.height/2:
        i.ry = i.height/2
    plo.newShape()
    plo.addPoint("up")
    plo.addPoint("point", i.x+i.rx, i.y)
    plo.addPoint("down")
    if i.rx+i.ry != 0:
        plo.addPoint("point", i.x+i.width-i.rx, i.y)
        plo.draw_arc(i.x+i.width-i.rx, i.y+i.ry, i.rx, i.ry, -90, 90, int(CURVE_SAMPLE_POINTS/4))
        plo.addPoint("point", i.x+i.width, i.y+i.height-i.ry)
        plo.draw_arc(i.x+i.width-i.rx, i.y+i.height-i.ry, i.rx, i.ry, 0, 90, int(CURVE_SAMPLE_POINTS/4))
        plo.addPoint("point", i.x+i.rx, i.y+i.height)
        plo.draw_arc(i.x+i.rx, i.y+i.height-i.ry, i.rx, i.ry, 90, 90, int(CURVE_SAMPLE_POINTS/4))
        plo.addPoint("point", i.x, i.y+i.ry)
        plo.draw_arc(i.x+i.rx, i.y+i.ry, i.rx, i.ry, -180, 90, int(CURVE_SAMPLE_POINTS/4))
    else:
        plo.addPoint("point", i.x+i.width, i.y)
        plo.addPoint("point", i.x+i.width, i.y+i.height)
        plo.addPoint("point", i.x, i.y+i.height)
        plo.addPoint("point", i.x, i.y)
    plo.addPoint("up")
    plo.raster()

"""Create Ellipse and Circles"""
def makeEllipse(plo, i):
    if i.shapeName == "circle":
        i.rx = i.r
        i.ry = i.r
    plo.addPoint("up")
    plo.addPoint("point", i.cx+i.rx, i.cy)
    plo.addPoint("down")
    plo.draw_arc(i.cx, i.cy, i.rx, i.ry, 0, 360, CURVE_SAMPLE_POINTS)
    plo.addPoint("up")

"""Create Paths"""
def makePath(plo, i):
    PATH_COMMANDS = {"M": 2,"L": 2,"H": 1,"V": 1,"C": 6,"S": 4,"Q": 4,"T": 2,"A": 99,"Z": 0}
    FULL_PATH_COMMANDS = {"M": 2,"L": 2,"H": 2,"V": 2,"C": 8,"S": 8,"Q": 6,"T": 6,"A": 99,"Z": 0}
    pathCur = ""
    pathShape = []

    # Split path into commands
    for char in i.d:
        if char.upper() in PATH_COMMANDS.keys():
            pathCur = "".join(pathCur)
            pathShape.append(pathCur)
            pathCur = []
        pathCur += char
    pathCur = "".join(pathCur)
    pathShape.append(pathCur)
    pathShape = pathShape[1:]
    printd(pathShape)

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
            commandPointsAdj = [None]*FULL_PATH_COMMANDS[commandType.upper()]
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
                        commandPointsAdj = [None]*FULL_PATH_COMMANDS[commandType.upper()]
                        commandNumOff = int(-PATH_COMMANDS[commandType.upper()] * commandPointNum/commandLength)

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
                        if( prevCommandType.upper() in ["C", "S"] ):
                            commandPointsAdj[2] = prevCommandPoints[-2] + (prevCommandPoints[-2] - prevCommandPoints[-4])
                            commandPointsAdj[3] = prevCommandPoints[-1] + (prevCommandPoints[-1] - prevCommandPoints[-3])
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
                        if( prevCommandType.upper() in ["Q", "T"]):
                            commandPointsAdj[2] = prevCommandPoints[-2] + (prevCommandPoints[-2] - prevCommandPoints[-4])
                            commandPointsAdj[3] = prevCommandPoints[-1] + (prevCommandPoints[-1] - prevCommandPoints[-3])
                        else:
                            additionalPoints = True
                        commandNumOff += 4

                    ## Need add "A" (arc)

                commandPointsAdj[commandPointNum+commandNumOff] = prevCommandPoints[(commandPointNum%2)-2]*moveRelative + commandPoints[commandPointNum]
                if commandType == "v":
                    commandPointsAdj[commandPointNum+commandNumOff] = prevCommandPoints[(1)-2]*moveRelative + commandPoints[commandPointNum]
            
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
                for i in range(0, CURVE_SAMPLE_POINTS+1, 1):
                    i /= CURVE_SAMPLE_POINTS
                    xPoint = (((1-i)**3) * iterCommandPoints[0]) + (3*i*((1-i)**2) * (iterCommandPoints[2])) + (3*(i**2) * (1-i) * (iterCommandPoints[4])) + (i**3 * (iterCommandPoints[6]))
                    yPoint = (((1-i)**3) * iterCommandPoints[1]) + (3*i*((1-i)**2) * (iterCommandPoints[3])) + (3*(i**2) * (1-i) * (iterCommandPoints[5])) + (i**3 * (iterCommandPoints[7]))
                    plo.addPoint("point", xPoint, yPoint)
            elif commandType.upper() in ["Q", "T"]:
                printd("Quadratic Curve/Smooth Quadratic curve")
                for i in range(0, CURVE_SAMPLE_POINTS+1, 1):
                    i /= CURVE_SAMPLE_POINTS
                    xPoint = (((1-i)**2) * iterCommandPoints[0]) + (2*i*(1-i) * (iterCommandPoints[2])) + (i**2 * (iterCommandPoints[4]))
                    yPoint = (((1-i)**2) * iterCommandPoints[1]) + (2*i*(1-i) * (iterCommandPoints[3])) + (i**2 * (iterCommandPoints[5]))
                    plo.addPoint("point", xPoint, yPoint)          
            elif commandType.upper() == "A":
                printe("Arc to be added ####################################################")
            elif commandType.upper() == "Z":
                printd("Close path")
                plo.addPoint("point", startPoint[0], startPoint[1])

    printd()

"""Draw Text"""
def makeText(plo, i):
    printd("Drawing text \"" + i.text + "\"")

"""Transform points in shape with transform attribute"""
def transformShape(plo, i):
    # Transform functions: matrix, translate, scale, rotate, skewX, skewY
    if "matrix" in i.transform:
        pointInt = _getTransformPoints("matrix", i)
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                newX = pointInt[0]*plo.pointsList[index] + pointInt[2]*plo.pointsList[index+1] + pointInt[4]
                newY = pointInt[1]*plo.pointsList[index] + pointInt[3]*plo.pointsList[index+1] + pointInt[5]
                plo.pointsList[index] = newX
                plo.pointsList[index+1] = newY

    if "translate" in i.transform:
        pointInt = _getTransformPoints("translate", i)
        if len(pointInt) == 1:
            pointInt.append(0)
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                plo.pointsList[index] += pointInt[0]
                plo.pointsList[index+1] += pointInt[1]
    
    if "scale" in i.transform:
        pointInt = _getTransformPoints("scale", i)
        if len(pointInt) == 1:
            pointInt.append(pointInt[0])
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                plo.pointsList[index] *= pointInt[0]
                plo.pointsList[index+1] *= pointInt[1]
    
    if "rotate" in i.transform:
        pointInt = _getTransformPoints("rotate", i)
        if len(pointInt) == 1:
            pointInt.append(0)
            pointInt.append(0)
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                x = plo.pointsList[index] - pointInt[1]
                y = plo.pointsList[index+1] - pointInt[2]
                s = math.sin(pointInt[0]*(math.pi/180))
                c = math.cos(pointInt[0]*(math.pi/180))
                newX = x*c - y*s
                newY = x*s + y*c
                plo.pointsList[index] = newX + pointInt[1]
                plo.pointsList[index+1] = newY + pointInt[2]
    
    if "skewX" in i.transform:
        pointInt = _getTransformPoints("skewX", i)
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                plo.pointsList[index] = plo.pointsList[index] + plo.pointsList[index+1]*math.tan(pointInt[0]*(math.pi/180))
    
    if "skewY" in i.transform:
        pointInt = _getTransformPoints("skewY", i)
        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                plo.pointsList[index+1] = plo.pointsList[index+1] + plo.pointsList[index]*math.tan(pointInt[0]*(math.pi/180))

def _getTransformPoints(word, i):
    printd("Found " + word + " at " + str(i.transform.index(word)))
    # Get translate points as string
    pointStr = ""
    pointIndex = 0
    pointIndexOffset = i.transform.index(word) + len(word) + 1
    while i.transform[pointIndex + pointIndexOffset] != ")":
        pointStr += i.transform[pointIndex + pointIndexOffset]
        pointIndex += 1
    printd(pointStr)

    # Get translate points as floats
    pointInt = []
    curPoint = ""
    for char in pointStr:
        if char == "," or char == " " or (char == "-" and curPoint != ""):
            pointInt.append(float(curPoint))
            if char == "-":
                curPoint = char
            else:
                curPoint = ""
        else:
            curPoint += char
    pointInt.append(float(curPoint))
    printd(pointInt)
    
    return pointInt


"""Parse objects into list"""
def parseObjects(shapeObjList):
    # New list object to add points to
    masterPlo = PointsListObj()

    for i in reversed(shapeObjList):
        printd("\nWorking on shape: " + str(i.shapeName))
        plo = PointsListObj()
        if i.checkShape():
            if i.shapeName == "line":
                makeLine(plo, i)
            if i.shapeName == "polyline" or i.shapeName == "polygon":
                makePolyline(plo, i)
            if i.shapeName == "rect":
                makeRect(plo, i)
            if i.shapeName == "circle" or i.shapeName == "ellipse":
                makeEllipse(plo, i)
            if i.shapeName == "path":
                makePath(plo, i)
            if i.shapeName == "text":
                makeText(plo, i)
        else:
            printe("Object invald, not drawing object: " + str(i.shapeName))
        
        if i.transform != "":
            transformShape(plo, i)
        
        masterPlo.addPlo(plo)
    
    return masterPlo


"""Reduces unnecessary resolution from points list and finds max/min xy points"""
def pointReduction(plo):
    # First loop: rounding
    for index, item in enumerate(plo.pointsList):
        if item != "up" and item != "down":
            plo.pointsList[index] = round(item, ROUND_DECIMAL_POINTS)

    # Second loop: removing duplicate point
    i = 0
    while i < len(plo.pointsList) - 2:
        if plo.pointsList[i] != "up" and plo.pointsList[i] != "down":
            if plo.pointsList[i] == plo.pointsList[i+2] and plo.pointsList[i+1] == plo.pointsList[i+3]:
                del plo.pointsList[i:i+2]
        i += 2
    
    # Third loop: shifting so all points positive
    maxXPoint, maxYPoint, minXPoint, minYPoint = plo.getMaxPoints(plo.pointsList)
    for i in range(0, len(plo.pointsList), 2):
        if plo.pointsList[i] != "up" and plo.pointsList[i] != "down":
            plo.pointsList[i] -= minXPoint
            plo.pointsList[i+1] -= minYPoint
    
    return plo