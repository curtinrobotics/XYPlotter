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
from fileIO import fileRunner
from parseData import splitStrip, objCreate
from parseObject import parseObjects
from turtleOutput import drawPointsTurtle, pointReduction

# Constants
FILE = "pathTest.svg"  # Source file for plotting


# Import svg file
fileText = fileRunner(FILE)

with open(FILE, "r") as fileObj:
    fileText = fileObj.read()

# Parse data into objects
# Split file string into shape list
shapeStrList = splitStrip(fileText)

# Create objects from shape list
shapeObjList = objCreate(shapeStrList)

# Parse objects into points
pointsList = parseObjects(shapeObjList)

# Output points to screen
# Point reduction
maxPoints = pointReduction(pointsList)

# Turtle output
drawPointsTurtle(pointsList, maxPoints)

input()  # delay till enter