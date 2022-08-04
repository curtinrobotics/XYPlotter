"""
parseObject.py - parse object data into points list

"""
from gCodeConverterObjects import pointsListObj


"""Parse objects into list"""
def parseObjects(shapeObjList):
    # New list object to add points to
    plo = pointsListObj()

    for i in shapeObjList:
        print(i)
        if i.checkShape():
            if i.shapeName == "rect":
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
            if i.shapeName == "circle" or i.shapeName == "ellipse":
                if i.shapeName == "circle":
                    i.rx = i.r
                    i.ry = i.r
                plo.addPoint("up")
                plo.addPoint("point", i.cx+i.rx, i.cy)
                plo.addPoint("down")
                plo.draw_arc(i.cx, i.cy, i.rx, i.ry, 0, 360, 100)
                plo.addPoint("up")
            if i.shapeName == "path":
                pathCommands = {"M": 2,"L": 2,"H": 1,"V": 1,"C": 6,"S": 4,"Q": 4,"T": 2,"A": 99,"Z": 0}
                fullPathCommands = {"M": 2,"L": 2,"H": 2,"V": 2,"C": 8,"S": 8,"Q": 6,"T": 6,"A": 99,"Z": 0}
                pathCur = ""
                pathShape = []

                # Split path into commands
                for char in i.d:
                    if char.upper() in pathCommands.keys():
                        pathCur = "".join(pathCur)
                        pathShape.append(pathCur)
                        pathCur = []
                    pathCur += char
                pathCur = "".join(pathCur)
                pathShape.append(pathCur)
                pathShape = pathShape[1:]
                print(pathShape)

                # Split commands into points
                startPoint = [0, 0]
                prevPoint = [0, 0]
                prevCommandPoints= [0, 0]
                prevCommandType = ""
                prevSmoothPoint = [0, 0]
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
                    commandLength = pathCommands[commandType.upper()]
                    if commandLength != 0:
                        commandIterations = (int( len(commandPoints) / commandLength ))
                        # Relative vs absolute points
                        moveRelative = False
                        if commandType not in pathCommands.keys():
                            moveRelative = True
                        # Pre-calculation of points
                        commandPointsAdjList = []
                        commandPointsAdj = [None]*fullPathCommands[commandType.upper()]
                        commandNumOff = 0
                        additionalPoints = False
                        print("New command")
                        print(commandType)

                        for commandPointNum in range(len(commandPoints)):
                            # Update previous command data if new iteration
                            if commandPointNum % commandLength == 0:
                                # Previous point "clean up"
                                '''
                                if len(commandPointsAdj) >= 2:
                                    prevPoint = [commandPointsAdj[-2], commandPointsAdj[-1]]
                                elif prevCommandType.upper() == "H":
                                    prevPoint = [commandPointsAdj[0], prevPoint[1]]
                                elif prevCommandType.upper() == "V":
                                    prevPoint = [prevPoint[0], commandPointsAdj[0]]
                                elif prevCommandType.upper() == "Z":
                                    prevPoint = startPoint
                                else:
                                    print("prevPoint ERROR")
                                if commandType.upper() == "M":
                                    startPoint = prevPoint
                                if prevCommandType.upper() in ["C", "S", "Q", "T"]:
                                    prevSmoothPoint = [moveRelative+commandPointsAdj[-4], commandPointsAdj[-3]]
                                prevCommandType = commandType
                                '''

                                if commandPointNum != 0:
                                    if additionalPoints:
                                        commandPointsAdj[2] = commandPointsAdj[4]
                                        commandPointsAdj[3] = commandPointsAdj[5]
                                    prevCommandPoints = commandPointsAdj
                                    prevCommandType = commandType
                                    commandPointsAdjList.append(commandPointsAdj)
                                    commandPointsAdj = [None]*fullPathCommands[commandType.upper()]
                                    commandNumOff = int(-pathCommands[commandType.upper()] * commandPointNum/commandLength)

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
                                ## Working here, close path "Z" needs fixing

                            commandPointsAdj[commandPointNum+commandNumOff] = prevCommandPoints[(commandPointNum%2)-2]*moveRelative + commandPoints[commandPointNum]
                            if commandType == "v":
                                commandPointsAdj[commandPointNum+commandNumOff] = prevCommandPoints[(1)-2]*moveRelative + commandPoints[commandPointNum]
                        
                        if additionalPoints:
                            commandPointsAdj[2] = commandPointsAdj[4]
                            commandPointsAdj[3] = commandPointsAdj[5]
                        commandPointsAdjList.append(commandPointsAdj)
                        prevCommandPoints = commandPointsAdj
                        prevCommandType = commandType
                        print(commandPointsAdjList)
                        print(commandPoints)


                    # Plot points from commands points
                    for iterCommandPoints in commandPointsAdjList:
                        print(iterCommandPoints)
                    
                        if commandType.upper() == "M":
                            print("Move")
                            plo.addPoint("up")
                            plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                            plo.addPoint("down")
                        elif commandType.upper() == "L":
                            print("Line")
                            plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                        elif commandType.upper() == "H":
                            print("Horizontal line")
                            plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                        elif commandType.upper() == "V":
                            print("Vertical line")
                            plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1])
                        elif commandType.upper() in ["C", "S"]:
                            print("Curve/Smooth Curve")
                            for i in range(0, 101, 1):
                                i /= 100
                                xPoint = (((1-i)**3) * iterCommandPoints[0]) + (3*i*((1-i)**2) * (iterCommandPoints[2])) + (3*(i**2) * (1-i) * (iterCommandPoints[4])) + (i**3 * (iterCommandPoints[6]))
                                yPoint = (((1-i)**3) * iterCommandPoints[1]) + (3*i*((1-i)**2) * (iterCommandPoints[3])) + (3*(i**2) * (1-i) * (iterCommandPoints[5])) + (i**3 * (iterCommandPoints[7]))
                                plo.addPoint("point", xPoint, yPoint)
                        elif commandType.upper() == "Q":
                            print("Quaratic curve")
                            for i in range(0, 101, 1):
                                i /= 100
                                xPoint = (((1-i)**2) * prevPoint[0]) + (2*i*(1-i) * (iterCommandPoints[0])) + (i**2 * (iterCommandPoints[2]))
                                yPoint = (((1-i)**2) * prevPoint[1]) + (2*i*(1-i) * (iterCommandPoints[1])) + (i**2 * (iterCommandPoints[3]))
                                plo.addPoint("point", xPoint, yPoint)
                        elif commandType.upper() == "T":
                            print("Smooth quadratic curve to be added Reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                            
                        elif commandType.upper() == "A":
                            print("Arc to be added Reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                        elif commandType.upper() == "Z":
                            print("Close path")
                            plo.addPoint("point", iterCommandPoints[0], iterCommandPoints[1]) 
                    
                    #if len(commandPoints) >= 2:
                    #    prevPoint = [prevPoint[0]*moveRelative + commandPoints[-2], prevPoint[1]*moveRelative + commandPoints[-1]]
                    #prevCommandType = commandType

                    #print(commandPoints)
                    #print(prevPoint)
                    #print(prevCommandType)
                    #print(prevSmoothPoint)
                        
                    
                print()
                  
                    


        else:
            print("Object invald, not drawing object: " + str(i.shapeName))
    
    return plo.pointsList