'''!
@file test_code.py

@brief		Final Test code file that runs a DC motor and measures its position with an encoder, implemented in classes

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		January 31, 2023

'''


import pyb
import motor_driver as md
import encoder_reader as er
import time

#create motor driver object
en_pin = pyb.Pin.board.PC1
in1pin = pyb.Pin.board.PA0
in2pin = pyb.Pin.board.PA1
timer = 5
moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)

#create encoder object
enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
timer = 8
encd = er.EncoderReader (enc_pin1, enc_pin2, timer)

###### TESTING BLOCK ########################################
'''
Note on testing block: It's creating an automated script to test different duty cycles, directions, and edge cases
at once, the "TESTING BLOCK" woudl be created as a function with input parameters of duty_cycle and time_to_test. 
It could be called with different values and the visual inspected to ensure expected behavior
'''
#Set duty cycle to be tested
moe.set_duty_cycle (0)

#timer reset for timed test
start_time = pyb.millis()
test_time = 0

#Testing constant duty cycle
while test_time < 5: #5 second test
    test_time = (pyb.millis() - start_time)/1000 #time elapsed in while loop

    #determine and display encoder position
    encd.read() 
    print(encd.position)
    time.sleep(0.1)
 
print("Done testing!")


#############################################################

    
    

