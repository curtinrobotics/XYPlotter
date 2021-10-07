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
FILE = "pathTest.svg"
PLOTTER_SIZE = (500, 500)
SHAPE_LIST = ["path", "rect", "circle", "ellipse"] # not  implemented: , "line", "polyline", "polygon"]
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
                draw_arc(i.x+i.width-i.rx, i.y+i.ry, i.rx, i.ry, -90, 90, 25)
                t.setpos(i.x+i.width, i.y+i.height-i.ry)
                draw_arc(i.x+i.width-i.rx, i.y+i.height-i.ry, i.rx, i.ry, 0, 90, 25)
                t.setpos(i.x+i.rx, i.y+i.height)
                draw_arc(i.x+i.rx, i.y+i.height-i.ry, i.rx, i.ry, 90, 90, 25)
                t.setpos(i.x, i.y+i.ry)
                draw_arc(i.x+i.rx, i.y+i.ry, i.rx, i.ry, -180, 90, 25)
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
            draw_arc(i.cx, i.cy, i.rx, i.ry, 0, 360, 100)
            t.penup()
        if i.shapeName == "path":
            for char in i.d:
                # Add code to interprate each char in string
                print(char, end="")


    else:
        print("Object invald, not drawing object: " + str(i.shapeName))

time.sleep(5)