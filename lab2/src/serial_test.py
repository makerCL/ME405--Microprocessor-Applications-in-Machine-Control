'''
For mac: attempting to open usb port with pyserial

'/dev/cu.usbmodem207537B3424B2' for right side usb-c to micro-py usb-b port on nucleo, w/ direct code not adapter

terminal command to see usb devices:
ls -l /dev/cu.usb*


'''

import serial
import time

print("Starting")

try:
    ser = serial.Serial('/dev/cu.usbmodem1103')  # open serial port
    print(ser.name)         # check which port was really used
    ser.write(b'hello')     # write a string
    ser.close()             # close port
#     with serial.Serial ('/dev/cu.usbmodem207537B3424B2', 115200) as s_port:
#         while(True):
#             print("attempting to send bytes")
#             s_port.write (b'something')       # Write bytes, not a string
#             print("sent? maybe?")
#             time.sleep(0.5)
except:
    print("Couldn't open serial port")