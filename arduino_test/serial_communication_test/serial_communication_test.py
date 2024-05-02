# Libraries
import serial
import time

from serial.serialutil import Timeout

# Constants
COM_PORT = "COM15"

# Variables
arduino = serial.Serial(port=COM_PORT, baudrate=9600, timeout=.1)

# Main
while True:
    num = input("on/off: ")
    arduino.write(bytes(num, 'utf-8'))
    time.sleep(.05)
    data = arduino.readline()
    print(data)