"""!
@file main.py

@brief Main file to interact with motor, encoder and controller drivers

@author Miles Alderman
@author Caleb Erlenborn


"""


import encoder_reader as er
import motor_driver as md
import feedback_control as fc
import pyb
import utime

## Create Motor Driver Obejct
en_pin = pyb.Pin.board.PA10
in1pin = pyb.Pin.board.PB4
in2pin = pyb.Pin.board.PB5
timer = 3
moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)

## Create Encoder Driver Object
enc_pin1 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
enc_pin2 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
timer = 4
encd = er.EncoderReader (enc_pin1, enc_pin2, timer)

## Create Feedback Control Object
mc = fc.FeedbackControl()
mc.init_VCP()
mc.set_setpoint(1000) # Define setpoint as 1000 encoder counts

## Loop that prompts for K_p and runs step response based on that.
while True:
    kp = '' 
    while kp == '': #while there isn't a kp, keep trying to get an input for one
        inp = input('Enter Kp ')
        try: 
            kp = float(inp) #if input is invalid, like a string, the try fails and reprompts user
            mc.set_kp(kp) #set kp in feedback controller object
        except:
            print("Please enter valid Kp")    
    t = 0
    
    ## Start time plotting perposes
    start_time = pyb.millis() 

    encd.zero() #zeroes encoder posn
    mc.data_clear() #clears old data
    
    while t<1000:   #record data for 1 second
        encd.read() #runs encoder reader, updating object property
        mc.run(encd.position) #runs controller based on latest position reading
        moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result
        
        #append current time and position data point
        t =pyb.millis() - start_time 
        mc.add_point([t, encd.position]) #add point to pos_data property of feedback controlelr 
        utime.sleep_ms(10) #delay for spacing of data points

    #wait until all the recording is done, then send all the data over serial
    moe.set_duty_cycle (0) # stop motor
    mc.data_transfer() #serial send data
    mc.print_pos_data() # can comment out if desired
