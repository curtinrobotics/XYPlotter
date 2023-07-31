"""
main.py
Call to start the program.
Calls other functions to run program.
Has command line arguments for running in different modes (CLI(default), GUI, LCD)
"""

# Libraries
import constants
import log
import inputOutput
import shapeCreation
import pointCreation
import turtlePlot

print("\n--== SVG Processing Tool v.alpha ==--\n")

# Setup debug log
log.createLog()

# Import svg file
svgData = inputOutput.readFileData(constants.FILE)

# Create shapes from file data
shapeList = shapeCreation.shapeCreation(svgData)

# Create points from shape data
pointList = pointCreation.pointCreation(shapeList)

# Plot Points
turtlePlot.turtlePlot(pointList)