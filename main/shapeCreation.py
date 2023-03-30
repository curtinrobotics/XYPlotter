"""
shapeCreation.py
Extracts shape parameters from SVG file and fills shape objects from shape.py.
"""

from inputOutput import printd

"""Main function for shape creation"""
def shapeCreation(svgData):
    """New format"""
    # Read file char by char, extracting elements
    elementList = findElements(svgData)
    for item in elementList:
        printd(item)

    # Extract element type and attributes from elements
    detailedElementList = extractElementDetails(elementList)

    """
    Old formant
    splitStrip(fileText)
    objCreate(shapeStrList)
        getObjData(objData, objName)
        createShape(shapeName, shapeDataDict, gData)
    """


"""Finds and generates list of XML elements"""
def findElements(svgData):
    elementList = []
    curElement = ""
    prevChar = ''
    elementType = "opening"
    newElement = True
    newElementMore = False
    """
    Types of elements
    single  - stand alone                   <  ... />
    opening - multiline opening container   <  ...  >
    closing - multiline closing container   </ ...  >
    version - XML version number            <? ... ?>
    doctype - SVG document type             <! ...  >
    comment - comment                       <!-- ... -->
    """
    for char in svgData:
        if char == '<':  # New element
            curElement = ""
            elementType = "opening"
            newElement = True
            newElementMore = False
        elif char == '>':  # Close element, append onto list
            if prevChar == '/':
                elementType = "single"
                curElement = curElement[:-1]
            if prevChar == '?' and elementType == "version":
                curElement = curElement[:-1]
            if prevChar == '-' and elementType == "comment":
                curElement = curElement[1:-2]
            elementList.append((elementType, curElement))
        elif char == '/' and newElement:  # Closing type element
            elementType = "closing"
        elif char == '?' and newElement:  # Version type element
            elementType = "version"
        elif char == '!' and newElement:  # Doctype or Comment type element
            newElementMore = True
            newElement = False
        elif newElementMore:  # Doctype of Comment type element
            newElementMore = False
            if char == '-':
                elementType = "comment"
            else:
                elementType = "doctype"
                curElement += char
        else:
            curElement += char
            newElement = False
        prevChar = char

    return elementList

"""Extracts SVG element types and attributes"""
def extractElementDetails(elementList):
    detailedElementList = []

    return detailedElementList


"""!!!OLD CODE!!

# Gets data from file string and retruns dict
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
        if index % 2 == 0:
            objDataDict[item] = objDataClean[index + 1]
    # Removes ID tag from data
    try:
        del objDataDict["id"]
    except KeyError as err:
        if str(err) != "'id'":
            raise KeyError(str(err))
    return objDataDict


# Creates shape objects from dict
def createShape(shapeName, shapeDataDict, gData):
    # Note: some objects may not exist
    newShape = Shape(shapeName)
    for gDict in gData:
        if (gDict != None):
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


# Split file string into shape list
def splitStrip(fileText):
    fileList = fileText.split("<")
    fileListStrip = []
    for item in fileList:
        item = item.strip()
        fileListStrip.append(item)
    return fileListStrip


# Create objects from shape list
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
"""
