"""
inputOutput.py
Inputs from SVG file.
Outputs of error/warning/debug messages.
Interfaces with gui.py and lcd.py for messages.
"""

import constants
import log
import os

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
    fileText = False
    try:
        with open(file, "r") as fileObj:
            fileText = fileObj.read()
    except FileNotFoundError:
        printe(f"ERROR: Invalid file. - {file}\n Please recomplie with valid file")
    return fileText

"""Write data to file"""
def writeFileData(file, data, createNewFile = True):
    success = False
    try:
        if not createNewFile:
            open(file) # Verify if file exists before being able to write to file
        # Any exceptions will be thrown before given file is created

        with open(file, "w") as fileObj:
            fileObj.write(data)
            success = True
    except FileNotFoundError:
        printe(f"ERROR: Invalid file. - {file}\n Please recomplie with valid file")
        success = False
    except TypeError:
        printe(f"ERROR: Invalid data type. - {type(data)}\n Please recompile with valid data")
        success = False
    return success

def appendFileData(file, data):
    success = False
    try:
        with open(file, "a+") as fileObj:
            fileObj.write(data)
            success = True
    except FileNotFoundError:
        printe(f"ERROR: Invalid file. - {file}\n Please recomplie with valid file")
        success = False
    except TypeError:
        printe(f"ERROR: Invalid data type. - {type(data)}\n Please recompile with valid data")
        success = False
    return success

"""Remove file from given path"""
def deleteFile(path):
    success = True
    try:
        os.remove(path)
    except FileNotFoundError:
        printe(f"ERROR: Invalid file. - {path}\n Please recomplie with valid file")
        success = False
    except Exception as e:
        print(e)
        success = False

    return success