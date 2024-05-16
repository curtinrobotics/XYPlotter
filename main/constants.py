"""
constants.py
Contains globals constants/flags.
Can be changed with setup.py.
"""

# Flags to be changed by setup.py

# Note: any tags after a | symbol signify the type of variable that should be passed in,
#       which is used by the gui to determine type of variable

# Print message type flag
ERROR_OUTPUT = True      # For errors that cause features missing   | type=bool  log
WARNING_OUTPUT = True    # For partially implemented features   | type=bool  log
DEBUG_OUTPUT = True      # For general debugging    | type=bool  log

# File IO
FILE = "sgvFiles/circleTest.svg"   # Source file for plotting

# Turtle Output
TURTLE_IMAGE_SCALING = 1  # Scale image to fit screen (>0)  | type=int  min=1   max=10
DRAWING_DELAY = 0  # Delay between drawing points (0-30)    | type=int  min=0   max=30
DRAW_PLOTTER_SIZE = True  # Overlay plotter size on turtle output   | type=bool
TURTLE_STANDARD_COLOR = "black"  # Color of turtle plot (see turtle.pencolor for more details)  | type=colour
TURTLE_PLOTTER_COLOR = "blue"  # Color of plotter size (only shown when DRAW_PLOTTER_SIZE is True)  | type=colour
TURTLE_ERROR_COLOR = "red"  # Color of shapes larger than plotter size (only shown when DRAW_PLOTTER_SIZE is True)  | type=colour

# Plotter Output (values only used when DRAW_PLOTTER_SIZE is True)
PLOTTER_IMAGE_SCALING = 1  # Scale image to fit sheet of paper (>0) | type=int  min=0   max=10
# Found from the maximum points outputted from the plotter
PLOTTER_WIDTH = 500  # Width of plotter drawing area    | type=int  min=1   max=1000
PLOTTER_HEIGHT = 300  # Height of plotter drawing area  | type=int  min=1   max=600

# Points Resolution
CURVE_SAMPLE_POINTS = 100  # Number of sample points on curves  | type=int  min=1   max=1000
ROUND_DECIMAL_POINTS = 1  # Number of decimal points to round to when culling image points  | type=int  min=0   max=10


# RESTRICTED
# ^ Do not change - signifies to setup.py that constants below this are not to be changed

TEMP_LOG_PATH = './logFiles/.tempLog.log'