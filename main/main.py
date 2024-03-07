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
import importlib
import subprocess
tp = importlib.import_module('turtlePlot')
# from turtlePlot import turtlePlot

import sys
#import gui



gui = False

print("\n--== SVG Processing Tool v.alpha ==--\n")
print('name is:', __name__)

if len(sys.argv) > 1 and sys.argv[1] == 'gui':
    
    tempLogFile = './logFiles/.tempLog.log'
    gui = True
    #inputOutput.appendFileData(tempLogFile, str(log.log.dLog))
    #print('log is ->', log.log)
    #inputOutput.writeFileData(tempLogFile, str(log.log))


# Setup debug log
#if sys.argv[1] != 'gui': log.createLog()
log.createLog()

# Import svg file
importlib.reload(constants)
svgData = inputOutput.readFileData(constants.FILE)

# Create shapes from file data
shapeList = shapeCreation.shapeCreation(svgData)

# Create points from shape data
pointList = pointCreation.pointCreation(shapeList)

if __name__ == '__main__':
    # Plot Points
    #subprocess.run(['python3', 'turtlePlot.py'])
    turt, s = tp.createVars()
    if not gui: tp.turtlePlot(pointList, gui=gui, turt=turt, s=s)

elif __name__ == 'main':
    print('was imported')