'''!
@file       lab1_motor.py

@brief		test file used for motor

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		January 31, 2023

'''


import pyb
import time

IN_1B = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
IN_2B = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
EN_B =  pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pull = pyb.Pin.PULL_UP)

timer_5 = pyb.Timer(5, prescaler=0,period=0xFFFF)

timer_5_ch1 = timer_5.channel (1, pyb.Timer.PWM, pin = IN_1B)
timer_5_ch2 = timer_5.channel (2, pyb.Timer.PWM, pin = IN_2B)
EN_B.value([True])

while True:
    timer_5_ch1.pulse_width_percent(50)
    timer_5_ch2.pulse_width_percent(0)
    time.sleep(5)
    timer_5_ch1.pulse_width_percent(0)
    time.sleep(5)
    