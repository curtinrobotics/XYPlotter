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

# Setup debug log
log.createLog()

# Import svg file
svgData = inputOutput.readFileData(constants.FILE)

shapeList = shapeCreation.shapeCreation(svgData)

"""
Point Creation
pointList = pointCreation.pointCreation(shapeList)

Plot Points
turtlePlot.turtlePlot(pointList)

"""


input()  # delay to keep drawing open
