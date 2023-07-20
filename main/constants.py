"""
constants.py
Contains globals constants/flags.
Can be changed with setup.py.
"""

# Flags to be changed by setup.py

# Print message type flag
ERROR_OUTPUT = True      # For errors that cause features missing
WARNING_OUTPUT = True    # For partially implemented features
DEBUG_OUTPUT = True      # For general debugging

# File IO
FILE = "sgvFiles/rectangleTest.svg"  # Source file for plotting

# Turtle Output
TURTLE_IMAGE_SCALING = 1  # Scale image to fit screen (>0)
DRAWING_DELAY = 0  # Delay between drawing points (0-30)
DRAW_PLOTTER_SIZE = True  # Overlay plotter size on turtle output
TURTLE_STANDARD_COLOR = "black"  # Color of turtle plot (see turtle.pencolor for more details)
TURTLE_PLOTTER_COLOR = "blue"  # Color of plotter size (only shown when DRAW_PLOTTER_SIZE is True)
TURTLE_ERROR_COLOR = "red"  # Color of shapes larger than plotter size (only shown when DRAW_PLOTTER_SIZE is True)

# Plotter Output (values only used when DRAW_PLOTTER_SIZE is True)
PLOTTER_IMAGE_SCALING = 1  # Scale image to fit sheet of paper (>0)
# Found from the maximum points outputted from the plotter
PLOTTER_WIDTH = 500  # Width of plotter drawing area
PLOTTER_HEIGHT = 300  # Height of plotter drawing area

# Points Resolution
CURVE_SAMPLE_POINTS = 100  # Number of sample points on curves
ROUND_DECIMAL_POINTS = 1  # Number of decimal points to round to when culling image points

# Constants no to be changed
