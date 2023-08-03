"""How it all works:
This file will recieve an array full of x and y coords, AS WELL AS some Up and DOWN commands
for eg: ["up", "up", xstart,ystart, "down", "down", x2,y2, x3,y3,........., xn,yn]

The job for this script will be to convert the array values into dx and dy values, 
so then the stepper motor will know how much to turn to make each movment of the pen

IMPORTANT:
delta coordinate of 1 == 1.8 degrees -> HOWEVER, might need DISTANCES to work it out
ASSUME: 
BOTH CW == UP; then
BOTH ACW == DOWN
if A is CW, and B is ACW, THEN == NorthEast
if A is ACW, and B is CW, THEN == SouthWest"""


import serial
import numpy as np


#VARIABLES:
ArduinoCOM = 'com3'
Baudrate = 115200

#Make sure to have an arduino in this COM Port!!!
###arduinoData=serial.Serial(ArduinoCOM, Baudrate)


#Loading up the array
VirginArray = np.array(['up', 'up', 75.0, 25.0, 'down', 'down', 125.0, 25.0, 128.1, 25.1, 131.3, 
                        25.4, 134.4, 25.9, 137.4, 26.6, 140.5, 27.4, 143.4, 28.5, 146.3, 29.8, 149.1, 
                        31.2, 151.8, 32.8, 154.4, 34.5, 156.9, 36.5, 159.2, 38.6, 161.4, 40.8, 163.5, 
                        43.1, 165.5, 45.6, 167.2, 48.2, 168.8, 50.9, 170.2, 53.7, 171.5, 56.6, 172.6, 
                        59.5, 173.4, 62.6, 174.1, 65.6, 174.6, 68.7, 174.9, 71.9, 175.0, 75.0, 175.0, 
                        125.0, 174.9, 128.1, 174.6, 131.3, 174.1, 134.4, 173.4, 137.4, 172.6, 140.5, 
                        171.5, 143.4, 170.2, 146.3, 168.8, 149.1, 167.2, 151.8, 165.5, 154.4, 163.5, 
                        156.9, 161.4, 159.2, 159.2, 161.4, 156.9, 163.5, 154.4, 165.5, 151.8, 167.2, 
                        149.1, 168.8, 146.3, 170.2, 143.4, 171.5, 140.5, 172.6, 137.4, 173.4, 134.4, 
                        174.1, 131.3, 174.6, 128.1, 174.9, 125.0, 175.0, 75.0, 175.0, 71.9, 174.9, 68.7, 
                        174.6, 65.6, 174.1, 62.6, 173.4, 59.5, 172.6, 56.6, 171.5, 53.7, 170.2, 50.9, 
                        168.8, 48.2, 167.2, 45.6, 165.5, 43.1, 163.5, 40.8, 161.4, 38.6, 159.2, 36.5, 
                        156.9, 34.5, 154.4, 32.8, 151.8, 31.2, 149.1, 29.8, 146.3, 28.5, 143.4, 27.4, 
                        140.5, 26.6, 137.4, 25.9, 134.4, 25.4, 131.3, 25.1, 128.1, 25.0, 125.0, 25.0, 
                        75.0, 25.1, 71.9, 25.4, 68.7, 25.9, 65.6, 26.6, 62.6, 27.4, 59.5, 28.5, 56.6, 
                        29.8, 53.7, 31.2, 50.9, 32.8, 48.2, 34.5, 45.6, 36.5, 43.1, 38.6, 40.8, 40.8, 
                        38.6, 43.1, 36.5, 45.6, 34.5, 48.2, 32.8, 50.9, 31.2, 53.7, 29.8, 56.6, 28.5, 
                        59.5, 27.4, 62.6, 26.6, 65.6, 25.9, 68.7, 25.4, 71.9, 25.1, 75.0, 25.0, 
                        'up', 'up', 'up', 'up', 0.0, 0.0, 'down', 'down', 60.0, 0.0, 60.0, 60.0, 
                        0.0, 60.0, 0.0, 0.0, 'up', 'up'])
print("The unedited array is: "+str(VirginArray), "With a size of: "+ str(VirginArray.size))

#ArrayZeros = np.array([])

#print()
#print("The ORIGINAL Array Zeros is: "+str(ArrayZeros)) 

#Processing the array - calculating dx and dy
NoUDArray = np.array([])
for i in range(0, VirginArray.size, 1):
    if VirginArray[i]=='up':
        NoUDArray = np.append(NoUDArray, -1.0)
    elif VirginArray[i]=='down':
        NoUDArray = np.append(NoUDArray, -2.0)
    else:
        NoUDArray = np.append(NoUDArray, VirginArray[i])
        
    #elif VirginArray[i-2] != 'up' and VirginArray[i-2] != 'down' and i != 2 and i != 3:
     #   if VirginArray[i-2] == 'up' and VirginArray[i-2] == 'down':
      #      #print(VirginArray[i-4])
       #     EditedArray = np.append(EditedArray, VirginArray[i] - VirginArray[i-4])
        #else:
         #   #print(VirginArray[i-2]+str(i))
          #  EditedArray = np.append(EditedArray, VirginArray[i] - VirginArray[i-2])
        
        
print("")
print("The NEW Array is: "+str(NoUDArray))
"""probably should use seperate if statements and 
idk how to make the servos work, but i still need it to output pen UP or pen DOWN"""
#Adjusting the values so that each 1 = 1.8 deg of movement


"""
#Sending it to the Arduino
while True:
    dxdy = "SOMETHINGGGG"
    dxdy = dxdy+'\r'
    #arduinoData.write(dxdy.encode())
    print(dxdy)"""