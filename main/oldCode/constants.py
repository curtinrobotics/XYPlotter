"""
constants.py - holds constants used throughout the program

"""

# Print message type flag
ERROR_OUTPUT = True      # For errors that cause featues missing
WARNING_OUTPUT = True    # For partially implemented features
DEBUG_OUTPUT = True      # For general debugging
PROGRESS_OUTPUT = False  # For information to an end user

# File IO
FILE = "sgvFiles/freesample.svg"  # Source file for plotting

# Turtle Output
IMAGE_SCALING = 1  # Scale image to fit screen (>0)
DRAWING_DELAY = 10  # Delay between drawing points (0-30)

# Points Resolution
CURVE_SAMPLE_POINTS = 100  # Number of sample points on curves
ROUND_DECIMAL_POINTS = 1  # Number of decimal points to round to when culling image points
