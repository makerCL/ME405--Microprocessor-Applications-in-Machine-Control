'''FOR MAC ONLY
SCRIPT FOR RECEIVING SERIAL DATA FROM MCU
terminal command to see usb devices:
ls -l /dev/cu.usb*
screen /dev/cu.usb_________
'''


import serial
import time
import matplotlib.pyplot as plt
import numpy as np

start = time.time()

port_path = '/dev/cu.usbmodem11103'
print(f"Attempting Port Receive on {port_path}")

def heatmap():
    pass


reading_data = False

data = np.empty((0, 32), dtype=float)

with serial.Serial (port_path, 115200) as s_port:
    while(True):
        try:
            if s_port.in_waiting:
                charIn = s_port.readline()

                if charIn == b'Data_Start\r\n':
                    reading_data = True
                elif charIn == b'Data_Stop\r\n':
                    reading_data = False
                    heatmap()
                    data = np.empty((0, 32), dtype=float)
                elif reading_data:
                    # decode the bytes to string, remove any whitespace characters, and strip the b and '
                    charIn = charIn.decode().strip(' ,')[2:-1]
                    print(charIn)
                    # split the line into comma-separated values and convert them to floats
                    row = np.array([int(x) for x in charIn.split(',')])
                    
                    # append the row to the data array
                    data = np.vstack((data, row))
                    
                    print(data)  # print the updated data array

        except KeyboardInterrupt:
            print("Port Closing")
            break

