"""
gCodeConverter - convert svg file to g-code

Overview:
  - Read file data
  - Parse data into objects
  - Parse objects into points
  - Output points to screen
  - Output points to xy-plotter (TBA)

"""
# Libraries
from gCodeConverterObjects import Shape
from parseObject import parseObjects
from turtleOutput import drawPointsTurtle, pointReduction
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

# Constants
FILE = "pathTest.svg"  # Source file for plotting
SHAPE_LIST = ["path", "rect", "circle", "ellipse"]  # not  implemented: , "line", "polyline", "polygon"]
FORMAT_SYSTAX = ["svg"]

# Variables
shapeObjList = []
gData = {}
pointsList = []

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


# Parse objects into points
pointsList = parseObjects(shapeObjList)

# Output points to screen
# Point reduction
maxPoints = pointReduction(pointsList)

# Turtle output
drawPointsTurtle(pointsList, maxPoints)

"""
# Curve Test

xVal = [0,0,200,200]
yVal = [0,200,0,200]
addPoint("up")
addPoint("point", 0, 0)
addPoint("down")
addPoint("point", 0,200)
addPoint("point", 0,0)
for i in range(0, 100, 1):
    i /= 100
    xPoint = (((1-i)**3) * xVal[0]) + (3*i*((1-i)**2) * xVal[1]) + (3*(i**2) * (1-i) * xVal[2]) + (i**3 * xVal[3])
    yPoint = (((1-i)**3) * yVal[0]) + (3*i*((1-i)**2) * yVal[1]) + (3*(i**2) * (1-i) * yVal[2]) + (i**3 * yVal[3])
    addPoint("point", xPoint, yPoint)
    print(str(xPoint) + ", " + str(yPoint))

addPoint("up")
"""
input()  # delay till enter