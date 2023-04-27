"""
shapeCreation.py
Extracts shape parameters from SVG file and fills shape objects from shape.py.
"""

import shape
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
                    elementType = CLOSING
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
    TYPE = 0
    NAME = 1
    DATA = 2
    for element in detailedElementList:
        if element[TYPE] == SINGLE:
            if element[NAME] in SHAPE_LIST:
                printd("Shape \"" + str(element[NAME]) + "\" being processed")
                newShape = createShape(element[NAME], element[DATA], containerList)
                if newShape is not None:
                    shapeObjList.append(newShape)
            elif element[NAME] in NEVER_SHAPE_LIST:
                printw("Shape \"" + str(element[NAME]) + "\" to not be processed")
            else:
                printe("Shape \"" + str(element[NAME]) + "\" type not found")
        elif element[TYPE] == OPENING:
            if element[NAME] == "g":
                printd("Opening Container \"" + str(element[NAME]) + "\" being processed")
                containerList.append(element[DATA])
            elif element[NAME] in NEVER_CONTAINER_LIST:
                printw("Opening Container \"" + str(element[NAME]) + "\" to not be processed")
            else:
                printe("Opening Container \"" + str(element[NAME]) + "\" type not found")
        elif element[TYPE] == CLOSING:
            if element[NAME] == "g":
                printd("Closing Container \"" + str(element[NAME]) + "\" being processed")
                containerList.pop()
            elif element[NAME] in NEVER_CONTAINER_LIST:
                printw("Closing Container \"" + str(element[NAME]) + "\" to not be processed")
            else:
                printe("Closing Container \"" + str(element[NAME]) + "\" type not found")
        elif element[TYPE] in [VERSION, DOCTYPE, COMMENT]:
            printd("SVG DATA: " + str(element[NAME]))
        elif element[TYPE] == CONTENT:
            printw("Element Content found, data not in element")
        else:
            printe("Element \"" + str(element[0]) + "\" type not found")
    return shapeObjList


"""Creates shape object from shape attribute data"""
def createShape(shapeName, shapeData, groupContainerData):
    newShape = None
    if shapeName == "line":
        newShape = shape.Line()
    elif shapeName == "polyline":
        newShape = shape.Polyline()
    elif shapeName == "polygon":
        newShape = shape.Polygon()
    elif shapeName == "rect":
        newShape = shape.Rectangle()
    elif shapeName == "circle":
        newShape = shape.Circle()
    elif shapeName == "ellipse":
        newShape = shape.Ellipse()
    elif shapeName == "path":
        newShape = shape.Path()
    else:
        printe("Shape \"" + str(shapeName) + "\" type not found")

    if newShape is not None:
        for container in groupContainerData:
            for key, value in container.items():
                state = newShape.add(key, value)
                outputCreateShapeError(state, shapeName, key)
        for key, value in shapeData.items():
            state = newShape.add(key, value)
            outputCreateShapeError(state, shapeName, key)
    return newShape


"""Outputs error text for createShape function"""
def outputCreateShapeError(state, shapeName, attribute):
    if state == "warning":
        printw("Attribute \"" + str(attribute) + "\" not implemented for \"" + shapeName + "\"")
    elif state == "not found":
        printe("Attribute \"" + str(attribute) + "\" not found for \"" + shapeName + "\"")
    elif state == "error":
        printe("Attribute \"" + str(attribute) + "\" not invalid for \"" + shapeName + "\"")
    elif state != "success":
        printw("Attribute \"" + str(attribute) + "\" had internal error for \"" + shapeName + "\"")
    else:
        printd("Attribute \"" + str(attribute) + "\" added to \"" + shapeName + "\"")


"""Creates list of attributes from g container"""
def createGroupAttributeList(groupContainerData):
    attributeList = []
    # extract attributes from g container, appending to list
    return attributeList
