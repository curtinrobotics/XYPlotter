"""
parseObjectToPoints.py - parse object data into points list

"""
# Libraries
from classes import PointsListObj
from IO import printe, printw, printd, printp

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
    plo.addPoint("up")
    plo.addPoint("point", i.x+i.rx, i.y)
    plo.addPoint("down")
    if i.rx+i.ry != 0:
        plo.addPoint("point", i.x+i.width-i.rx, i.y)
        plo.draw_arc(i.x+i.width-i.rx, i.y+i.ry, i.rx, i.ry, -90, 90, 25)
        plo.addPoint("point", i.x+i.width, i.y+i.height-i.ry)
        plo.draw_arc(i.x+i.width-i.rx, i.y+i.height-i.ry, i.rx, i.ry, 0, 90, 25)
        plo.addPoint("point", i.x+i.rx, i.y+i.height)
        plo.draw_arc(i.x+i.rx, i.y+i.height-i.ry, i.rx, i.ry, 90, 90, 25)
        plo.addPoint("point", i.x, i.y+i.ry)
        plo.draw_arc(i.x+i.rx, i.y+i.ry, i.rx, i.ry, -180, 90, 25)
    else:
        plo.addPoint("point", i.x+i.width, i.y)
        plo.addPoint("point", i.x+i.width, i.y+i.height)
        plo.addPoint("point", i.x, i.y+i.height)
        plo.addPoint("point", i.x, i.y)
    plo.addPoint("up")

"""Create Ellipse and Circles"""
def makeEllipse(plo, i):
    if i.shapeName == "circle":
        i.rx = i.r
        i.ry = i.r
    plo.addPoint("up")
    plo.addPoint("point", i.cx+i.rx, i.cy)
    plo.addPoint("down")
    plo.draw_arc(i.cx, i.cy, i.rx, i.ry, 0, 360, 100)
    plo.addPoint("up")

"""Create Line"""
def makeLine(plo, i):
    pass
    #Add line code here
    # "i" is the item, get attributes from "i"
    # e.g. i.x, i.y, i.length ect.
    # plo is the points list object (the list of points)
    # plo.addPoint(sel, x, y)
    # sel is selection (takes string "point", "up", "down")
    # if up/down, nothing for x or y
    # if point, add x and y cord of point

"""Create PolyLine"""
def makePolyline(plo, i):
    pass
    #Add polyline code here

"""Create Polygon"""
def makePolygon(plo, i):
    pass
    #Add polygon code here

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
                for i in range(0, 101, 1):
                    i /= 100
                    xPoint = (((1-i)**3) * iterCommandPoints[0]) + (3*i*((1-i)**2) * (iterCommandPoints[2])) + (3*(i**2) * (1-i) * (iterCommandPoints[4])) + (i**3 * (iterCommandPoints[6]))
                    yPoint = (((1-i)**3) * iterCommandPoints[1]) + (3*i*((1-i)**2) * (iterCommandPoints[3])) + (3*(i**2) * (1-i) * (iterCommandPoints[5])) + (i**3 * (iterCommandPoints[7]))
                    plo.addPoint("point", xPoint, yPoint)
            elif commandType.upper() in ["Q", "T"]:
                printd("Quadratic Curve/Smooth Quadratic curve")
                for i in range(0, 101, 1):
                    i /= 100
                    xPoint = (((1-i)**2) * iterCommandPoints[0]) + (2*i*(1-i) * (iterCommandPoints[2])) + (i**2 * (iterCommandPoints[4]))
                    yPoint = (((1-i)**2) * iterCommandPoints[1]) + (2*i*(1-i) * (iterCommandPoints[3])) + (i**2 * (iterCommandPoints[5]))
                    plo.addPoint("point", xPoint, yPoint)          
            elif commandType.upper() == "A":
                printe("Arc to be added ####################################################")
            elif commandType.upper() == "Z":
                printd("Close path")
                plo.addPoint("point", startPoint[0], startPoint[1])

    printd()

"""Transform points in shape with transform attribute"""
def transformShape(plo, i):
    # Transform function: matrix, translate, scale, rotate, skewX, skewY
    if "translate" in i.transform:
        printd("Found translate at " + str(i.transform.index("translate")))
        # Get translate points as string
        pointStr = ""
        pointIndex = 0
        pointIndexOffset = i.transform.index("translate") + len("translate") + 1
        while i.transform[pointIndex + pointIndexOffset] != ")":
            pointStr += i.transform[pointIndex + pointIndexOffset]
            pointIndex += 1
        
        # Get translate points as floats
        pointInt = [0.0, 0.0]
        curPoint = ""
        for char in pointStr:
            if char == "," or char == " " or (char == "-" and curPoint != ""):
                pointInt[0] = float(curPoint)
                if char == "-":
                    curPoint = char
                else:
                    curPoint = ""
            else:
                curPoint += char
        pointInt[1] = float(curPoint)
        printd(pointInt)

        # Translate plo points
        for index in range(0, len(plo.pointsList), 2):
            if plo.pointsList[index] != "up" and plo.pointsList[index] != "down":
                plo.pointsList[index] += pointInt[0]
                plo.pointsList[index+1] += pointInt[1]
                

                    



"""Parse objects into list"""
def parseObjects(shapeObjList):
    # New list object to add points to
    masterPlo = PointsListObj()

    for i in shapeObjList:
        printd("\nWorking on shape: " + str(i.shapeName))
        plo = PointsListObj()
        if i.checkShape():
            if i.shapeName == "rect":
                makeRect(plo, i)
            if i.shapeName == "circle" or i.shapeName == "ellipse":
                makeEllipse(plo, i)
            if i.shapeName == "line":
                makeLine(plo, i)
            #add rest here ##############################################################
            if i.shapeName == "path":
                makePath(plo, i)
        else:
            printe("Object invald, not drawing object: " + str(i.shapeName))
        
        if i.transform != "":
            transformShape(plo, i)
        
        masterPlo.addPlo(plo)
    

    return masterPlo.pointsList


"""Reduces unnecessary resolution from points list and finds max/min xy points"""
def pointReduction(pointsList):
    # First loop: rounding
    for index, item in enumerate(pointsList):
        if item != "up" and item != "down":
            pointsList[index] = round(item, 1)

    # Second loop: removing duplicate point; finding max X and Y points
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

            if pointsList[i] == pointsList[i+2] and pointsList[i+1] == pointsList[i+3]:
                del pointsList[i:i+2]
        i += 2
    
    return maxXPoint, maxYPoint, minXPoint, minYPoint