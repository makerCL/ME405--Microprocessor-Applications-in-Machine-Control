"""!
@file serial_recv.py

SCRIPT FOR RECEIVING SERIAL DATA FROM MCU
terminal (OSX) command to see usb devices:
ls -l /dev/cu.usb*

@author Miles Alderman
@author Caleb Erlenborn


"""

import serial
from matplotlib import pyplot as plt


x_pts = [] #x coordinates of points to plot
y_pts = [] #y coordinates of points to plot


print("Attempting Port Receive...")

## boolean to indicate if serial data should be interpreted as data points
transfer_started = False

##open the serial port to receive
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

        #Plot the data!
        plt.plot(x_pts,y_pts)
        plt.xlabel("Time (s)")
        plt.ylabel("Encoder Position (encoder counts)")
        plt.title(f"Lab 2 Plot, k_p = 0.02")
        plt.show()

