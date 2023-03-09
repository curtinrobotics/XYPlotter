"""
main.py - convert svg file to g(ish)-code

Overview:
  - Read file data
  - Parse data into objects
  - Parse objects into points
  - Output points to screen
  - Output points to xy-plotter (TBA)

"""
# Libraries
import constants
import IO
from parseDataToObject import splitStrip, objCreate
from parseObjectToPoints import parseObjects, pointReduction

# Import svg file
fileText = IO.readFileData(constants.FILE)

# Parse data into objects
# Split file string into shape list
shapeStrList = splitStrip(fileText)

# Create objects from shape list
shapeObjList = objCreate(shapeStrList)

# Parse objects into points
plo = parseObjects(shapeObjList)

# Point reduction
plo = pointReduction(plo)

# Turtle output
IO.drawPointsTurtle(plo)

input()  # delay to keep drawing open