'''!
@file       lab1_encoder.py

@brief		test file used for encoder

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		January 31, 2023

'''
import pyb
import time
print('hello world')

pin_C6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
pin_C7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)


timer_8 = pyb.Timer(8, prescaler=0,period=0xFFFF)
timer_8_ch1 = timer_8.channel (1, pyb.Timer.ENC_AB, pin = pin_C6)
timer_8_ch2 = timer_8.channel (2, pyb.Timer.ENC_AB, pin = pin_C7)
pos = 0

while True:
    pos = timer_8.counter()
    print(pos)
    time.sleep(0.5)