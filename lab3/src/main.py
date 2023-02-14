"""!
@file main.py
    This file contains main operations of ME405 lab3 as adapted from basictasks.py
    from ME405 source library. The file creates and runs two tasks to independently
    and simultaneously run two position controlled DC motors.


@author JR Ridgely
@author Caleb Erlenborn
@author Miles Alderman
@date   2/13/2023
"""
import gc
import pyb
import cotask
import task_share

import encoder_reader as er
import motor_driver as md
import feedback_control as fc

def motor1_task_fun():
"""!
    Task which performs position control on motor 1.
"""
    ## Create Motor Driver Obejct for 1A motor
    en_pin = pyb.Pin.board.PA10
    in1pin = pyb.Pin.board.PB4
    in2pin = pyb.Pin.board.PB5
    timer = 3
    moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)
    ## Create Encoder Driver Object for encoder with pins B6/B7
    enc_pin1 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = 4
    encd = er.EncoderReader (enc_pin1, enc_pin2, timer)
    ## Create Feedback Control Object
    mc = fc.FeedbackControl()
    mc.init_VCP()
    mc.set_setpoint(1000) # Define setpoint as 1000 encoder counts
    # Set the proportional gain to 0.02 (found to be optimal in lab2)
    mc.set_kp(0.02)
    # Initalize the start time and encoder position
    start_time = pyb.millis()
    encd.zero() #zeroes encoder posn
    
    while True:
        t = pyb.millis() - start_time	# time from last reset
        if t<2000:   #record data for 2 second
            encd.read() #runs encoder reader, updating object property
            mc.run(encd.position) #runs controller based on latest position reading
            moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result
            #append current time and position data point
            mc.add_point([t, encd.position]) #add point to pos_data property of feedback controlelr
        else: #Once data is done recording, then send all the data over serial
            moe.set_duty_cycle (0) # stop motor
            #mc.data_transfer() #serial send data
            #mc.print_pos_data() # can comment out if desired  
            encd.zero() #zeroes encoder posn
            mc.data_clear() #clears old data
            start_time = pyb.millis()
        yield 0        
 
def motor2_task_fun():
"""!
    Task which performs position control on motor 2.
"""
## Create Motor Driver Obejct for 1B motor
    en_pin = pyb.Pin.board.PC1
    in1pin = pyb.Pin.board.PA0
    in2pin = pyb.Pin.board.PA1
    timer = 5
    moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)
    
    ## Create Encoder Driver Object
    enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    timer = 8
    encd = er.EncoderReader (enc_pin1, enc_pin2, timer)
    
    ## Create Feedback Control Object
    mc = fc.FeedbackControl()
    mc.init_VCP()
    mc.set_setpoint(1000) # Define setpoint as 1000 encoder counts
    # Set the proportional gain to 0.02 (found to be optimal in lab2)
    mc.set_kp(0.02)
    # Initalize the start time and encoder position
    start_time = pyb.millis()
    encd.zero() #zeroes encoder posn
    
    while True:
        ## Start time plotting perposes
        t = pyb.millis() - start_time
        if t<2000:   #record data for 1 second
            encd.read() #runs encoder reader, updating object property
            mc.run(encd.position) #runs controller based on latest position reading
            moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result
            #append current time and position data point
            mc.add_point([t, encd.position]) #add point to pos_data property of feedback controlelr
        else: #Once data is done recording, then send all the data over serial
            moe.set_duty_cycle (0) # stop motor
            #mc.data_transfer() #serial send data
            #mc.print_pos_data() # can comment out if desired  
            encd.zero() #zeroes encoder posn
            mc.data_clear() #clears old data
            start_time = pyb.millis()
        yield 0 


# This code creates two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(motor1_task_fun, name="Task_1", priority=1, period=10,
                        profile=True, trace=False)
    task2 = cotask.Task(motor2_task_fun, name="Task_2", priority=2, period=10,
                        profile=True, trace=False)

    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
