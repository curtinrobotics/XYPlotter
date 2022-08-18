"""
IO - input and output data

"""
import turtle
import constants
import debugLogClass

# Variables
debugLogObj = debugLogClass.DebugLog()

"""Print functions with print types"""
"""Print Error"""
def printe(msg="", end="\n"):
    debugLogObj.newLog("error", msg)
    if constants.ERROR_OUTPUT:
        print(msg, end=end)

"""Print Warning"""
def printw(msg="", end="\n"):
    debugLogObj.newLog("warning", msg)
    if constants.WARNING_OUTPUT:
        print(msg, end=end)

"""Print Debug"""
def printd(msg="", end="\n"):
    debugLogObj.newLog("debug", msg)
    if constants.DEBUG_OUTPUT:
        print(msg, end=end)

"""Print Progress"""
def printp(msg="", end="\n"):
    if constants.PROGRESS_OUTPUT:
        print(msg, end=end)

"""Print Final Log"""
def printDebugLog(terminal):
    debugLogObj.outputLog(constants.ERROR_OUTPUT, constants.WARNING_OUTPUT, constants.DEBUG_OUTPUT, terminal)


"""Read data from file"""
def readFileData(file):
    with open(file, "r") as fileObj:
        try:
            fileText = fileObj.read()
        except FileNotFoundError:
            printe("ERROR: Invalid file.\n Please recomplie with valid file")
    return fileText

"""Output points to screen with turtle"""
def drawPointsTurtle(pointsList, maxPoints):
    # Turtle settings for screen
    screen = turtle.Screen()
    canvasWidth = (maxPoints[0]-maxPoints[2])*constants.IMAGE_SCALING
    canvasHeight = (maxPoints[1]-maxPoints[3])*constants.IMAGE_SCALING
    turtle.screensize(canvasWidth, canvasHeight)
    screen.setup(canvasWidth+50, canvasHeight+50)
    turtle.tracer(1, constants.DRAWING_DELAY)
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
            t.setpos(pointsList[i*2]*constants.IMAGE_SCALING-canvasWidth/2, -pointsList[i*2+1]*constants.IMAGE_SCALING+canvasHeight/2)