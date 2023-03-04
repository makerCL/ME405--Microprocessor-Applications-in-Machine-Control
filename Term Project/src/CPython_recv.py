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
import seaborn as sns

start = time.time()

port_path = '/dev/cu.usbmodem11103'
print(f"Attempting Port Receive on {port_path}")

def heatmap(data):
    hm = sns.heatmap(data, cmap = 'coolwarm')
    plt.show()
##TODO: make this update live
#https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/

reading_data = False

data = np.empty((0, 32), dtype=int)

with serial.Serial (port_path, 115200) as s_port:
    while(True):
        try:
            if s_port.in_waiting:
                charIn = s_port.readline()

                if charIn == b'Data_Start\r\n':
                    reading_data = True
                elif charIn == b'Data_Stop\r\n':
                    print(data)  # print the updated data array
                    #print(data.shape)
                    print("\n\n\n\n")
                    reading_data = False
                    heatmap(data)

                    #Reinitialize array as empty
                    data = np.empty((0, 32), dtype=int)

                elif reading_data:
                    # decode the bytes to string, remove any whitespace characters, and strip the b and '
                    charIn = charIn.decode().strip(' ,\r\nb')
                    int_row = []
                    for x in charIn.split(','):
                        try:
                            int_row.append(int(x))
                        except:
                            int_row.append(0)
                    if not len(int_row) == 32:
                        raise Exception("Row of data was invalid, and thus array will be wrong size to concatenate")
                        #alternatively could just assign row of zeros.

                    # split the line into comma-separated values and convert them to floats
                    np_row = np.array(int_row)
                    
                    # append the row to the data array
                    data = np.vstack((data, np_row))
                    
            

        except KeyboardInterrupt:
            print("Port Closing")
            break

