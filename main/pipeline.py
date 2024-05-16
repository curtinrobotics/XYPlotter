"""
pipeline.py - process image and create points list
Calls other functions to run program.
Use constants.py to change parameters
"""

# Libraries
import constants
import log
import inputOutput
import shapeCreation
import pointCreation
import importlib


# Creates points list (uses global variables in constants.py)
def pipeline():
    # Setup debug log
    log.createLog()
    # Import svg file
    importlib.reload(constants)
    svgData = inputOutput.readFileData(constants.FILE)
    # Create shapes from file data
    shapeList = shapeCreation.shapeCreation(svgData)
    # Create points from shape data
    pointList = pointCreation.pointCreation(shapeList)
    return pointList
