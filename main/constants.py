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
FILE = "sgvFiles/pathTest.svg"  # Source file for plotting

# Turtle Output 
IMAGE_SCALING = 0.5  # Scale image to fit screen (>0) 
DRAWING_DELAY = 0  # Delay between drawing points (0-30)

# Plotter Output
PIXELS_MULTIPLIER = 1 # Scale image to fit sheet of paper
# Found from the maximum points outputted from the plotter

# Points Resolution
CURVE_SAMPLE_POINTS = 100  # Number of sample points on curves
ROUND_DECIMAL_POINTS = 1  # Number of decimal points to round to when culling image points

# Constants no to be changed
