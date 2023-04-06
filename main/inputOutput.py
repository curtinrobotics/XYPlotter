"""
inputOutput.py
Inputs from SVG file.
Outputs of error/warning/debug messages.
Interfaces with gui.py and lcd.py for messages.
"""

import constants
import log

"""Print functions with print types for log"""
"""Print Error"""
def printe(msg="", end="\n"):
    log.log.newLog("error", msg)
    if constants.ERROR_OUTPUT:
        print(msg, end=end)

"""Print Warning"""
def printw(msg="", end="\n"):
    log.log.newLog("warning", msg)
    if constants.WARNING_OUTPUT:
        print(msg, end=end)

"""Print Debug"""
def printd(msg="", end="\n"):
    log.log.newLog("debug", msg)
    if constants.DEBUG_OUTPUT:
        print(msg, end=end)

"""Read data from file"""
def readFileData(file):
    with open(file, "r") as fileObj:
        try:
            fileText = fileObj.read()
        except FileNotFoundError:
            printe("ERROR: Invalid file.\n Please recomplie with valid file")
    return fileText
