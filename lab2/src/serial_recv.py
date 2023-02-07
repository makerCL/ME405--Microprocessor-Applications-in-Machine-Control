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


print("Attempting Port Receive...")

transfer_started = False
    
with serial.Serial ('/dev/cu.usbmodem2103', 115200) as s_port:
    while(True):
        while(True):
            if s_port.in_waiting:
                charIn = s_port.readline()
                try:
                    print(f"char_in: {charIn}")
                    #test if the serial message is the start or end transfer prompt
                    if charIn == b'Data_Start\r\n' : #start looking for data after start prompt
                        print("Data Transfer Started")
                        transfer_started = True

                    elif charIn == b'Data_End\r\n' : #stop looking for data after stop prompt
                        print("Data Transfer Ended")
                        transfer_started = False
                        break
                    
                    elif transfer_started:#split data points if we are indeed receiving them
                        print("transfer_started")
                        x_val, y_val = charIn.split(b',')
                        x_pts.append(float(x_val))
                        y_pts.append(float(y_val))

                    else:
                        pass

                except:
                    pass

        #plot the data!
        plt.plot(x_pts,y_pts)
        plt.xlabel("Time (s)")
        plt.ylabel("Encoder Position (encoder counts)")
        plt.title("Lab 2 Plot")
        plt.show()

