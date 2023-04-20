"""
shapeCreation.py
Extracts shape parameters from SVG file and fills shape objects from shape.py.
"""

from inputOutput import printd, printw, printe

# Constants used in file
# Types of elements
SINGLE = "single"
OPENING = "opening"
CLOSING = "closing"
VERSION = "version"
DOCTYPE = "doctype"
COMMENT = "comment"
CONTENT = "content"

# List of Shapes that can be processed
SHAPE_LIST = ["line", "polyline", "polygon", "rect", "circle", "ellipse", "path"]
# List of Shapes that are never to be processed
NEVER_SHAPE_LIST = []
# List of Containers that are never to be processed
NEVER_CONTAINER_LIST = []


"""Main function for shape creation"""
def shapeCreation(svgData):
    # Read file char by char, extracting elements
    elementList = findElements(svgData)

    # Extract element type and attributes from elements
    detailedElementList = extractElementDetails(elementList)
    for item in detailedElementList:
        printd(item)

    # Create shape objects
    shapeObjList = createShapeList(detailedElementList)

    return shapeObjList

    """
    Old formant
    splitStrip(fileText)
    objCreate(shapeStrList)
        getObjData(objData, objName)
        createShape(shapeName, shapeDataDict, gData)
    """


"""Finds and generates list of XML elements"""
"""Returns list of tuples of element types and element data"""
def findElements(svgData):
    elementList = []
    """
    Types of elements
    single  - stand alone                   <  ... />
    opening - multiline opening container   <  ...  >
    closing - multiline closing container   </ ...  >
    version - XML version number            <? ... ?>
    doctype - SVG document type             <! ...  >
    comment - comment                       <!-- ... -->
    content - not in element
    """
    curElement = ""
    for char in svgData:
        if char == '<':
            # Content type (not in element)
            curElement = curElement.strip()
            if curElement != "":
                elementList.append((CONTENT, curElement))
            curElement = ""
        elif char == '>':
            if curElement != "":
                if curElement[-1] == "/":
                    elementType = SINGLE
                    curElement = curElement[:-1]
                elif curElement[0] == "/":
                    elementType = OPENING
                    curElement = curElement[1:]
                elif curElement[0] == "?" and curElement[-1] == "?":
                    elementType = VERSION
                    curElement = curElement[1:-1]
                elif curElement[0] == "!":
                    elementType = DOCTYPE
                    if len(curElement) >= 5:
                        if curElement[:3] == "!--" and curElement[-2:] == "--":
                            elementType = COMMENT
                            curElement = curElement[3:-2]
                    if elementType == DOCTYPE:
                        curElement = curElement[1:]
                else:
                    elementType = OPENING
                elementList.append((elementType, curElement))
            curElement = ""
        else:
            curElement += char

    return elementList


"""Extracts SVG element types and attributes"""
"""Returns list of tuples of element types, element name, element attribute dictionary"""
def extractElementDetails(elementList):
    detailedElementList = []
    for item in elementList:
        elementType = item[0]
        elementName = item[1].split()[0]
        elementData = item[1][len(elementName):]
        elementDict = {}

        # Get element attributes (not all elements have attributes)
        if elementType in [DOCTYPE, COMMENT, CONTENT]:
            elementName = item[1]
        else:
            inQuote = False
            quoteType = ""
            curData = ""
            curAttName = ""
            # attribute name = "data"
            for char in elementData:
                if not inQuote and (char == '"' or char == "'"):  # New data
                    inQuote = True
                    quoteType = char
                elif inQuote and char == quoteType:  # End data, append attribute
                    inQuote = False
                    quoteType = ""
                    elementDict.update({curAttName: curData})
                    curData = ""
                    curAttName = ""
                elif inQuote:  # Add data
                    curData += char
                elif not (char.isspace() or char == '='):  # Add attribute name
                    curAttName += char

        detailedElementList.append((elementType, elementName, elementDict))

    return detailedElementList


"""Creates shape objects from element list"""
"""Returns list of shape objects (see shape.py)"""
def createShapeList(detailedElementList):
    shapeObjList = []
    containerList = []
    for element in detailedElementList:
        if element[0] == SINGLE:
            if element[1] in SHAPE_LIST:
                printd("Shape \"" + str(element[1]) + "\" being processed")
                shapeObjList.append(createShape(element[1], element[2], containerList))
            elif element[1] in NEVER_SHAPE_LIST:
                printw("Shape \"" + str(element[1]) + "\" to not be processed")
            else:
                printe("Shape \"" + str(element[1]) + "\" type not found")
        elif element[0] == OPENING:
            if element[1] == "g":
                printd("Opening Container \"" + str(element[1]) + "\" being processed")
                containerList.append(element[3])
            elif element[1] in NEVER_CONTAINER_LIST:
                printw("Opening Container \"" + str(element[1]) + "\" to not be processed")
            else:
                printe("Opening Container \"" + str(element[1]) + "\" type not found")
        elif element[0] == CLOSING:
            if element[1] == "g":
                printd("Closing Container \"" + str(element[1]) + "\" being processed")
                containerList.pop()
            elif element[1] in NEVER_CONTAINER_LIST:
                printw("Closing Container \"" + str(element[1]) + "\" to not be processed")
            else:
                printe("Closing Container \"" + str(element[1]) + "\" type not found")
        elif element[0] in [VERSION, DOCTYPE, COMMENT]:
            printd("SVG DATA: " + str(element[1]))
        elif element[0] == CONTENT:
            printw("Element Content found, data not in element")
        else:
            printe("Element \"" + str(element[0]) + "\" type not found")

    return shapeObjList


"""Creates shape object from shape attribute data"""
def createShape(shapeName, shapeData, groupContainerData):
    newShape = None
    if shapeName == "line":
        pass
    elif shapeName == "polyline":
        pass
    elif shapeName == "polygon":
        pass
    elif shapeName == "rect":
        pass
    elif shapeName == "circle":
        pass
    elif shapeName == "ellipse":
        pass
    elif shapeName == "path":
        pass
    else:
        printe("Shape \"" + str(shapeName) + "\" type not found")
    # case statement of shapeName: create shape obj
    # append g container data from outermost to innermost
    #   inner containers override outer containers
    # append shape data
    #    shape data overrides g containers

    return newShape


"""Creates list of attributes from g container"""
def createGroupAttributeList(groupContainerData):
    attributeList = []
    # extract attributes from g container, appending to list
    return attributeList

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
