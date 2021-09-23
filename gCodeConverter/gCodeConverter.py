"""
gCodeConverter - convert svg file to g-code

"""
# Libraries
from gCodeConverterObjects import Shape
import turtle
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
FILE = "test.svg"
PLOTTER_SIZE = (500, 500)
SHAPE_LIST = ["path", "rect", "circle", "ellipse", "line", "polyline", "polygon"]
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

# Print out instrutions
for item in shapeObjList:
    print(item)

# Turtle simulation
t = turtle.Turtle()
t.left(90)
for item in shapeObjList:
    if item.checkShape():
        if item.shapeName == "rect":
            t.penup()
            t.setpos(item.x, item.y)
            t.pendown()
            t.setpos(item.x+item.width, item.y)
            t.setpos(item.x+item.width, item.y+item.height)
            t.setpos(item.x, item.y+item.height)
            t.setpos(item.x, item.y)
            t.penup()
    else:
        print("Object invald, not drawing object: " + str(item.shapeName))

time.sleep(5)