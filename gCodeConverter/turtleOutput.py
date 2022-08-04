"""
turtleOuput - outputs turtle image from points list

"""
# Libraries
import turtle

# Constants
IMAGE_SCALING = 1.5  # Scale image to fit screen (>0)
DRAWING_DELAY = 0  # Delay between drawing points (0-30)

"""Reduces unnecessary resolution from points list and finds max/min xy points"""
def pointReduction(pointsList):
    # First loop: rounding
    for index, item in enumerate(pointsList):
        if item != "up" and item != "down":
            pointsList[index] = round(item, 1)

    # Second loop: removing duplicate point; finding max X and Y points
    maxXPoint = 0
    maxYPoint = 0
    minXPoint = 0
    minYPoint = 0
    i = 0
    while i < len(pointsList) - 2:
        if pointsList[i] != "up" and pointsList[i] != "down":
            if pointsList[i] > maxXPoint:
                maxXPoint = pointsList[i]
            if pointsList[i+1] > maxYPoint:
                maxYPoint = pointsList[i+1]
            if pointsList[i] < minXPoint:
                minXPoint = pointsList[i]
            if pointsList[i+1] < minYPoint:
                minYPoint = pointsList[i+1]

            if pointsList[i] == pointsList[i+2] and pointsList[i+1] == pointsList[i+3]:
                del pointsList[i:i+2]
            else:
                i += 2
        else:
            i += 1
    
    return maxXPoint, maxYPoint, minXPoint, minYPoint


"""Draws image from points list using turtle"""
def drawPointsTurtle(pointsList, maxPoints):
    # Turtle settings for screen
    screen = turtle.Screen()
    canvasWidth = (maxPoints[0]-maxPoints[2])*IMAGE_SCALING
    canvasHeight = (maxPoints[1]-maxPoints[3])*IMAGE_SCALING
    turtle.screensize(canvasWidth, canvasHeight)
    screen.setup(canvasWidth+50, canvasHeight+50)
    turtle.tracer(1, DRAWING_DELAY)
    t = turtle.Turtle()
    t.hideturtle()
    t.left(90)
    
    # Drawing of points
    for i in range(int(len(pointsList)/2)):
        if pointsList[i*2] == "up":
            t.penup()
        elif pointsList[i*2] == "down":
            t.pendown()
        else:
            t.setpos(pointsList[i*2]*IMAGE_SCALING-canvasWidth/2, -pointsList[i*2+1]*IMAGE_SCALING+canvasHeight/2)
