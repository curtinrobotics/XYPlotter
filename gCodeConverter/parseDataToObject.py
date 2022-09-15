"""
parseDatatoObject.py - parse file data (as a string) into objects

"""
# Libraries
from classes import Shape
from IO import printe, printw, printd, printp

#Constants
# Full shape list: <a>, <circle>, <clipPath>, <defs>, <ellipse>, <foreignObject>, <g>, <image>, <line>, <path>, <polygon>, <polyline>, <rect>, <switch>, <text>, <use>
# Todo shape list: <a>, <clipPath>, <defs>, <foreignObject>, <g>, <image>, <path>.arch, <switch>, <text>, <use>
SHAPE_LIST = ["line", "polyline", "polygon", "rect", "circle", "ellipse", "path", "text"]
FORMAT_SYSTAX = ["svg"]

"""Gets data from file string and retruns dict"""
def getObjData(objData, objName):
    # Make object data into list
    objData = objData.split("\"")
    objDataClean = []
    for item in objData:
        item = item.strip()
        item = item.strip("=")
        item = item.strip()
        if len(objDataClean) == 0:
            item = item.split()
            item = item[1].strip()
        objDataClean.append(item)
    if objName == "text":
        textData = objDataClean[-1].strip(">")   
        objDataClean = objDataClean[:-1]
        objDataClean.append("text")
        objDataClean.append(textData)
    else:
        objDataClean = objDataClean[:-1]
    # Make list into dict
    objDataDict = {}
    printd(objDataClean)
    for index, item in enumerate(objDataClean):
        if index%2 == 0:
            objDataDict[item] = objDataClean[index+1]
    # Removes ID tag from data
    try:
        del objDataDict["id"]
    except KeyError as err:
        if str(err) != "'id'":
            raise KeyError(str(err))
    return objDataDict

"""Creates shape objects from dict"""
def createShape(shapeName, shapeDataDict, gData):
    # Note: some objects may not exist
    newShape = Shape(shapeName)
    for gDict in gData:
        if( gDict != None ):
            for item in gDict:
                itemAdded = newShape.add(item, gDict[item])
                if itemAdded == "success":
                    printd("Successfully added\t" + str(item) + "\tto " + str(shapeName))
                elif itemAdded == "warning":
                    printw("Warning: added\t" + str(item) + "\tto " + str(shapeName) + " but not implemented")
                else:
                    printe("Could not find\t\t" + str(item) + "\tin " + str(shapeName))
    for item in shapeDataDict:
        itemAdded = newShape.add(item, shapeDataDict[item])
        if itemAdded == "success":
            printd("Successfully added\t" + str(item) + "\tto " + str(shapeName))
        elif itemAdded == "warning":
            printw("Warning: added\t" + str(item) + "\tto " + str(shapeName) + " but not implemented")
        else:
            printe("Could not find\t\t" + str(item) + "\tin " + str(shapeName))
    return newShape

"""Split file string into shape list"""
def splitStrip(fileText):
    fileList = fileText.split("<")
    fileListStrip = []
    for item in fileList:
        item = item.strip()
        fileListStrip.append(item)
    return fileListStrip

"""Create objects from shape list"""
def objCreate(shapeStrList):
    shapeObjList = []
    gData = []
    for item in shapeStrList:
        if item != "":
            objName = item.split()[0]
            if objName in SHAPE_LIST:
                # Create shape object
                printd("\nCreating object: " + objName)
                objDict = getObjData(item, objName)
                shapeObj = createShape(objName, objDict, gData)
                shapeObjList.append(shapeObj)
            elif objName in FORMAT_SYSTAX:
                printd(objName + " format")
            elif objName == "g":
                # Creates g container
                printd("\nOpen g container")
                gData.append(getObjData(item, objName))
            elif objName == "g>":
                # Create empty g container
                printd("\nOpen g empty container")
                gData.append(None)
            elif objName == "/g>":
                # Close g container
                printd("Close g container")
                gData.pop()
            elif "/" in objName:
                printd("Closing: " + str(objName[1:-1]))
            else:
                printe("What dis: " + str(objName))
    
    return shapeObjList

