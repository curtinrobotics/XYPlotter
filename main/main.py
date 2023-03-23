"""
main.py
Call to start the program.
Calls other functions to run program.
Has command line arguments for running in different modes (CLI(default), GUI, LCD)
"""

# Libraries
import constants
import log
import io

# Setup debug log
log.createLog()

# Import svg file
svgData = io.readFileData(constants.FILE)

"""
Shape Creation
shapeList = shapeCreation.shapeCreation(svgData)

Point Creation
pointList = pointCreation.pointCreation(shapeList)

Plot Points
turtlePlot.turtlePlot(pointList)

"""

# Parse data into objects
# Split file string into shape list
shapeStrList = splitStrip(svgData)

# Create objects from shape list
shapeObjList = objCreate(shapeStrList)

# Parse objects into points
plo = parseObjects(shapeObjList)

# Point reduction
plo = pointReduction(plo)

# Turtle output
IO.drawPointsTurtle(plo)

input()  # delay to keep drawing open
