'''FOR MAC ONLY
SCRIPT FOR RECEIVING SERIAL DATA FROM MCU
terminal command to see usb devices:
ls -l /dev/cu.usb*
'''


import serial
import time
start = time.time()
import matplotlib.pyplot as plt
port_path = '/dev/cu.usbmodem207537B3424B2'
print(f"Attempting Port Receive on {port_path}")
'''
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
'''

with serial.Serial (port_path, 115200) as s_port:
    while(True):
        try:
            if s_port.in_waiting:
                charIn = s_port.readline()
                print(charIn)

        except KeyboardInterrupt:
            print("Port Closing")
            break

