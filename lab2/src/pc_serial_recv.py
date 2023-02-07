'''FOR MAC ONLY

SCRIPT FOR RECEIVING SERIAL DATA FROM MCU

terminal command to see usb devices:
ls -l /dev/cu.usb*


'''


import serial
import time
start = time.time()
from matplotlib import pyplot as plt


labels_found = False #for finding labels
labels = [] #axis labels
x_pts = [] #x coordinates of points to plot
y_pts = [] #y coordinates of points to plot


print("Attempting Port Receive")

        
with serial.Serial ('COM7', 115200) as s_port:
    while(True):
        if s_port.in_waiting:
            charIn = s_port.readline()
            try:
                x_val, y_val = charIn.split(b',')
                x_val = float(x_val)
                y_val = float(y_val)
                x_pts.append(x_val)
                y_pts.append(y_val)
            except:
                print("couldn't convert char to str")
        plt.plot(x_pts,y_pts)

            


#TODO: some way to exit the while loop so that the data can be plotted:
#plot the data
plt.plot(x_pts, y_pts)
#plt.xlabel(labels[0])
#plt.ylabel(labels[1])
plt.title("Lab 2 Plot")
plt.show()
