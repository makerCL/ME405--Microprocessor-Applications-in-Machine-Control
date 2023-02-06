'''FOR MAC ONLY

SCRIPT FOR RECEIVING SERIAL DATA FROM MCU

terminal command to see usb devices:
ls -l /dev/cu.usb*


'''


import serial
import time
start = time.time()
import matplotlib.pyplot as plt


labels_found = False #for finding labels
labels = [] #axis labels
x_pts = [] #x coordinates of points to plot
y_pts = [] #y coordinates of points to plot


print("Attempting Port Receive")

def format_str(item):
    try:
        item = str(item)
        item = item.strip(' b/\\rn\"\'')
        point = item.split(',')
    except:
        return
    else:
        try:
            item = [float(x) for x in point]
            return item[0], item[1]
        except:
            return
        
with serial.Serial ('/dev/cu.usbmodem2103', 115200) as s_port:
    while(True):
        if s_port.in_waiting:
            charIn = s_port.readline()
            try:
                x_val, y_val = format_str(charIn)
                x_pts += x_val
                y_pts += y_val
            except:
                print("couldn't convert char to str")

            print(charIn)

#TODO: some way to exit the while loop so that the data can be plotted:
#plot the data
plt.plot(x_pts, y_pts)
#plt.xlabel(labels[0])
#plt.ylabel(labels[1])
plt.title("Lab 2 Plot")
plt.show()
