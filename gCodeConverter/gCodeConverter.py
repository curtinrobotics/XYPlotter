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
from parseData import splitStrip, objCreate
from parseObject import parseObjects
from turtleOutput import drawPointsTurtle, pointReduction

# Constants
FILE = "pathTest.svg"  # Source file for plotting

# Import svg file
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