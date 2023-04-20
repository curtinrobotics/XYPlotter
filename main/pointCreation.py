"""
pointCreation.py
Creates a list of points from shapes created in shapeCreation.py.
"""

from inputOutput import printd, printw, printe

"""Main function for point creation"""
def pointCreation(shapeList):
    pointList = []
    for shape in shapeList:
        printd("\nWorking on shape: " + str(shape.name()))
        shapePointList = shape.getPoints()
        shapePointList = shape.transform(shapePointList)
        shapePointList = Shape.pointReduction(shapePointList)

        pointList.append(shapePointList)

    return pointList

