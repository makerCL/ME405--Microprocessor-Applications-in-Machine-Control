"""!

Author: Miles Alderman

Helpful mac terminal commands for USB configuration
#Display list of connected USB devices (for port_path)
ls -l /dev/cu.usb*

#For displaying received camera data
screen /dev/cu.usb_________

"""

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns



start = time.time()

width  = 32
height = 24

# Ideal Setpoint as seen on thermal camera
yaw_center = width / 2 #centered, pixels from left
pitch_center = height / 2 #cetnered, pixels top; may change with distance/velocity


port_path = '/dev/cu.usbmodem1103'
print(f"Attempting Port Receive on {port_path}")

def heatmap(data, yaw_aim, pitch_aim):
    
    plt.close()
    hm = sns.heatmap(data, cmap = 'coolwarm')

    ##TODO: make this update live
    #https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/

    #plt.scatter(yaw_aim, pitch_aim, marker='o', s=100, c='chartreuse')
    plt.show()
    
reading_data = False

data = np.empty((0, 32), dtype=int)

with serial.Serial (port_path, 115200) as s_port:
    while(True):
        try:
            if s_port.in_waiting:
                charIn = s_port.readline()

                if charIn == b'Data_Start\r\n':
                    reading_data = True
                    array = []
                elif charIn == b'Data_Stop\r\n':
                    #print(data)  # print the updated data array
                    #print(data.shape)
                    #print("\n\n\n\n")
                    reading_data = False
                    
                    # list of column average heats
                    col_avgs = []

                    # Add to list
                    for column in range(width):
                        #print()
                        col = []
                        for i in range(0, width * height, width):
                            col.append(array[i + column])

                        col_avgs.append(sum(col) / len(col))

                    # Index of column that has max avg value
                    max_col_idx = col_avgs.index(max(col_avgs))

                    # Column that has maximum average heat
                    max_col = []

                    # Extract column
                    for i in range(0, height*width, width):
                        max_col.append(array[i])

                    #Find max value from the top of the row
                    vert_max = max_col.index(max(max_col))
                   # print(vert_max)

                    # PLOT
                    heatmap(data, max_col_idx, vert_max)

                    #Reinitialize array as empty
                    data = np.empty((0, 32), dtype=int)

                elif reading_data:
                    # decode the bytes to string, remove any whitespace characters, and strip the b and '
                    charIn = charIn.decode().strip(' ,\r\nb')
                    int_row = []

                    for x in charIn.split(','):
                        try:
                            int_row.append(int(x))
                            array.append(int(x))
                        except:
                            int_row.append(0)
                            array.append(0)
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

