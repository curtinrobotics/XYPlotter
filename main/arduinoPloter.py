import serial
import pointList.py


"""

handels comunication with arduino

in:

  string: the name of the port the arduino is on
    supplyed by GUI
    ** to be done automatically in future version **

  pointList: instructions
    wrapper for a list of point objects
    points are instructions to raise pen, lower pen, or move pen to a given co-ord

  bool: ready
    boolean value recieved from arduino to indicate readiness to recieve (more) instructions
out:

  int: x coord to move to.  -1 if raising pen, -2 if lowering
  int: y coord to move to.  -1 if raising pen, -2 if lowering
"""


