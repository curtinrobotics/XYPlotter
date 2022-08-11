"""
fileIO - read and write from file

"""
import constants

"""Read data from file"""
def fileRunner(file):
    with open(file, "r") as fileObj:
        try:
            fileText = fileObj.read()
        except FileNotFoundError:
            printe("ERROR: Invalid file.\n Please recomplie with valid file")
    
    return fileText

"""Print functions with print types"""
"""Print Error"""
def printe(msg="", end="\n"):
    if constants.ERROR_OUTPUT:
        print(msg, end=end)

"""Print Warning"""
def printw(msg="", end="\n"):
    if constants.WARNING_OUTPUT:
        print(msg, end=end)

"""Print Debug"""
def printd(msg="", end="\n"):
    if constants.DEBUG_OUTPUT:
        print(msg, end=end)

"""Print Progress"""
def printp(msg="", end="\n"):
    if constants.PROGRESS_OUTPUT:
        print(msg, end=end)