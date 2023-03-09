'''FOR MAC ONLY

Author: Miles Alderman

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

port_path = '/dev/cu.usbmodem1103'
print(f"Attempting Port Receive on {port_path}")

def heatmap(data, width = 32, height = 24):
    
    plt.close()
    hm = sns.heatmap(data, cmap = 'coolwarm')

    ##TODO: make this update live
    #https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
    max_temp = np.amax(data)
    min_temp = np.amin(data)

    scaled_array = (data - min_temp) / (max_temp - min_temp) * 255
    print(f"np_arr[0][0] = {data[0][0]}")
    print(f"np_arr[1][4] = {data[1][4]}")
    print(f"np_arr[23][32] = {data[23][32]}")
    print(f"np_arr[12][12] = {data[12][12]}")
    print(f"np_arr[5][6] = {data[5][6]}")
    #Create mask where the heat is higher than a certain value
    #TODO: maybe this would be better if it was absolute temperatures instead? anything about 80 F?
    temp_mask = (scaled_array > 150)

    #Find centroid of target by averaging the indexes of filtered points
    centr_y, centr_x = np.array(np.where(temp_mask)).mean(axis=1)

    plt.scatter(centr_x, centr_y, marker='o', s=100, c='chartreuse')

    # Ideal Setpoint as seen on thermal camera
    yaw_center = width / 2 #centered, pixels from left
    pitch_center = height / 2 #cetnered, pixels top; may change with distance/velocity
    
    plt.show()

    #angle = (0,0)
    #yield (angle)
    
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

