'''FOR MAC ONLY

SCRIPT FOR RECEIVING SERIAL DATA FROM MCU

terminal command to see usb devices:
ls -l /dev/cu.usb*


'''


import serial
import time

print("Attempting Port Receive")

#try:
with serial.Serial ('/dev/cu.usbmodem11403', 115200) as s_port:
    while(True):
        if s_port.in_waiting:
            charIn = s_port.readline()
            print(charIn)
           

#except:
#    print('did not work!')