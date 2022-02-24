"""
gCodeConverter - convert svg file to g-code

"""
# Libraries
from gCodeConverterObjects import Shape
import turtle
import math
import time

# Functions
def get_obj_data(objData):
    """Gets data from file string and retruns dict"""
    # Make object data into list
    objData = objData.split("\"")
    objDataClean = []
    for item in objData:
        item = item.strip()
        item = item.strip("=")
        item = item.strip()
        if len(objDataClean) == 0:
            item = item.split()
            item = item[1].strip()
        objDataClean.append(item)
    objDataClean = objDataClean[:-1]
    # Make list into dict
    objDataDict = {}
    for index, item in enumerate(objDataClean):
        if index%2 == 0:
            objDataDict[item] = objDataClean[index+1]
    # Removes ID tag from data
    try:
        del objDataDict["id"]
    except KeyError as err:
        if str(err) != "'id'":
            raise KeyError(str(err))
    return objDataDict

def create_shape(shapeName, shapeDataDict, gData):
    """Creates shape objects"""
    # Note: some objects may not exist
    newShape = Shape(shapeName)
    for item in gData:
        itemAdded = newShape.add(item, gData[item])
        if itemAdded:
            print("Successfully added\t" + str(item) + "\tto " + str(shapeName))
        else:
            print("Could not find\t\t" + str(item) + "\tin " + str(shapeName))
    for item in shapeDataDict:
        itemAdded = newShape.add(item, shapeDataDict[item])
        if itemAdded:
            print("Successfully added\t" + str(item) + "\tto " + str(shapeName))
        else:
            print("Could not find\t\t" + str(item) + "\tin " + str(shapeName))
    return newShape

def draw_arc(xPos, yPos, rx, ry, sDegree, degree, res):
    """Draws arc with radius r, starting at sDegree"""
    sRad = sDegree * math.pi/180  # Start pos
    rad = degree * math.pi/180  # Move amount
    for step in range(res+1):
        x = xPos + rx * math.cos((rad/res)*step + sRad)
        y = yPos + ry * math.sin((rad/res)*step + sRad)
        t.setpos(x, y)
    

# Constants
FILE = "inkScapeTest.svg"  # Source file for plotting
PLOTTER_SIZE = (500, 500)  # Size of plot (Check fathethest point in svg file)
CURVE_RES = 25  # Resolution of curves (lower res faster drawing but more segmented), Must be whole number
SHAPE_LIST = ["path", "rect", "circle", "ellipse"]  # not  implemented: , "line", "polyline", "polygon"]
FORMAT_SYSTAX = ["svg"]

# Variables
shapeObjList = []
gData = {}

# Import svg file
with open(FILE, "r") as fileObj:
    fileText = fileObj.read()

# Split file into instructions
fileList = fileText.split("<")
fileListStrip = []
for item in fileList:
    item = item.strip()
    fileListStrip.append(item)

# Identify objects
for item in fileListStrip:
    if item != "":
        objName = item.split()[0]
        if objName in SHAPE_LIST:
            # Create shape object
            print("Creating object: " + objName)
            objDict = get_obj_data(item)
            shapeObj = create_shape(objName, objDict, gData)
            shapeObjList.append(shapeObj)
        elif objName in FORMAT_SYSTAX:
            print(objName + " format")
        elif objName == "g":
            # Creates g container
            print("Open g container")
            gData = get_obj_data(item)
        elif objName == "/g>":
            # Close g container
            print("Close g container")
            gData = {}
        elif "/" in objName:
            print("Closing: " + str(objName[1:-1]))
        else:
            print("What dis: " + str(objName))

# Turtle simulation
t = turtle.Turtle()
t.left(90)
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
            t.penup()
            t.setpos(i.x+i.rx, i.y)
            t.pendown()
            if i.rx+i.ry != 0:
                t.setpos(i.x+i.width-i.rx, i.y)
                draw_arc(i.x+i.width-i.rx, i.y+i.ry, i.rx, i.ry, -90, 90, CURVE_RES)
                t.setpos(i.x+i.width, i.y+i.height-i.ry)
                draw_arc(i.x+i.width-i.rx, i.y+i.height-i.ry, i.rx, i.ry, 0, 90, CURVE_RES)
                t.setpos(i.x+i.rx, i.y+i.height)
                draw_arc(i.x+i.rx, i.y+i.height-i.ry, i.rx, i.ry, 90, 90, CURVE_RES)
                t.setpos(i.x, i.y+i.ry)
                draw_arc(i.x+i.rx, i.y+i.ry, i.rx, i.ry, -180, 90, CURVE_RES)
            else:
                t.setpos(i.x+i.width, i.y)
                t.setpos(i.x+i.width, i.y+i.height)
                t.setpos(i.x, i.y+i.height)
                t.setpos(i.x, i.y)
            t.penup()
        if i.shapeName == "circle" or i.shapeName == "ellipse":
            if i.shapeName == "circle":
                i.rx = i.r
                i.ry = i.r
            t.penup()
            t.setpos(i.cx+i.rx, i.cy)
            t.pendown()
            draw_arc(i.cx, i.cy, i.rx, i.ry, 0, 360, CURVE_RES*4)
            t.penup()
        if i.shapeName == "path":
            pathCommands = ["M", "L", "H", "V", "C", "S", "Q", "T", "A", "Z"]
            pathCur = ""
            pathShape = []

            # Split path into commands
            for char in i.d:
                if char.upper() in pathCommands:
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
            for command in pathShape:
                command = command.strip()
                commandType = command[0]
                # Find point in string
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
                # Plot points with respect to command
                moveRelative = False
                if commandType not in pathCommands:
                    moveRelative = True
                    print("relaive points")
                if commandType.upper() == "M":
                    print("Move")
                    t.penup()
                    t.setpos(prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1]*moveRelative + commandPoints[1])
                    t.pendown()
                    startPoint = [prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1]*moveRelative + commandPoints[1]]
                    prevPoint = [prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1]*moveRelative + commandPoints[1]]
                elif commandType.upper() == "L":
                    print("Line")
                    t.setpos(prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1]*moveRelative + commandPoints[1])
                elif commandType.upper() == "H":
                    print("Horizontal line")
                    t.setpos(prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1])
                    prevPoint = [prevPoint[0]*moveRelative + commandPoints[0], prevPoint[1]]
                elif commandType.upper() == "V":
                    print("Vertical line rel")
                    t.setpos(prevPoint[0], prevPoint[1]*moveRelative + commandPoints[0])
                    prevPoint = [prevPoint[0], prevPoint[1]*moveRelative + commandPoints[0]]
                elif commandType.upper() == "C":
                    print("Curve")
                    for i in range(0, CURVE_RES*4+1, 1):
                        i /= CURVE_RES*4
                        xPoint = (((1-i)**3) * prevPoint[0]) + (3*i*((1-i)**2) * (prevPoint[0]*moveRelative+commandPoints[0])) + (3*(i**2) * (1-i) * (prevPoint[0]*moveRelative+commandPoints[2])) + (i**3 * (prevPoint[0]*moveRelative+commandPoints[4]))
                        yPoint = (((1-i)**3) * prevPoint[1]) + (3*i*((1-i)**2) * (prevPoint[1]*moveRelative+commandPoints[1])) + (3*(i**2) * (1-i) * (prevPoint[1]*moveRelative+commandPoints[3])) + (i**3 * (prevPoint[1]*moveRelative+commandPoints[5]))
                        t.setpos(xPoint, yPoint)
                elif commandType.upper() == "S":
                    print("Smooth curve to be added ###########################################")
                elif commandType.upper() == "Q":
                    print("Quaratic curve to be added #########################################")
                elif commandType.upper() == "T":
                    print("Smooth quadratic curve to be added #################################")
                elif commandType.upper() == "A":
                    print("Arc to be added ####################################################")
                elif commandType.upper() == "Z":
                    print("Close path")
                    t.setpos(startPoint)
                    prevPoint = startPoint


                if len(commandPoints) >= 2:
                    prevPoint = [prevPoint[0]*moveRelative + commandPoints[-2], prevPoint[1]*moveRelative + commandPoints[-1]]
                

                print(commandPoints)
                print(prevPoint)
                    
                




            print()
                
                


    else:
        print("Object invald, not drawing object: " + str(i.shapeName))

"""
# Curve Test

xVal = [0,0,200,200]
yVal = [0,200,0,200]
t.penup()
t.setpos(0, 0)
t.pendown()
t.setpos(0,200)
t.setpos(0,0)
for i in range(0, 100, 1):
    i /= 100
    xPoint = (((1-i)**3) * xVal[0]) + (3*i*((1-i)**2) * xVal[1]) + (3*(i**2) * (1-i) * xVal[2]) + (i**3 * xVal[3])
    yPoint = (((1-i)**3) * yVal[0]) + (3*i*((1-i)**2) * yVal[1]) + (3*(i**2) * (1-i) * yVal[2]) + (i**3 * yVal[3])
    t.setpos(xPoint, yPoint)
    print(str(xPoint) + ", " + str(yPoint))

t.penup()
"""
input()  # delay till enter