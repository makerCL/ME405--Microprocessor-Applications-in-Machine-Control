"""!
@file main.py

@brief Main file for Nerf Sentry gun

@author Miles Alderman
@author Caleb Erlenborn


"""

import gc
import pyb
from machine import Pin, I2C

import cotask
import task_share
import encoder_reader as er
import motor_driver as md
import feedback_control as fc
import servo_controller as sc
import mlx_cam as mlx

import time
import math


def yaw_mtr_fcn(shares):

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

    # Set Gains
    mc.set_kp(0.05)

    # Initalize the encoder position
    encd.zero() #zeroes encoder posn
    
    while True:
        
        #unpack shares
        yaw_target = shares
        print(f"yaw shares {yaw_target.get()}")
        #Update Target
        mc.set_setpoint(yaw_target.get()) # Define setpoint as 1000 encoder counts
        encd.read() #runs encoder reader, updating object property
        mc.run(encd.position) #runs controller based on latest position reading
        
        #print(f"Time: {pyb.millis()/1000}")
        print(f"encoder posn {encd.position}")
        #print(f"motor pwm {mc.PWM}")
        #print()
        
        moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result

        yield 0   

def pitch_mtr_fcn(shares):

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
    
    # Set gains
    mc.set_kp(0.25)
    mc.set_ki(0.005)
    #mc.set_kd(2)

    encd.zero() #zeroes encoder posn
    
    while True:
        #unpack shares
        pitch_target = shares
        #Update Target
        mc.set_setpoint(pitch_target.get()) # Define setpoint as 1000 encoder counts

        encd.read() #runs encoder reader, updating object property
        mc.run(encd.position) #runs controller based on latest position reading
        print(f"encoder position {encd.position}")
        moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result

        yield 0 


def trigger_mtr_fcn():
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    ## Initialize the servo motor pin
    PA9 = pyb.Pin.board.PA9
    timer = 1
    ch = 2
    servo = sc.servo_controller(PA9, timer, ch)
    servo.set_servo_ang(0)
    
    fire = True
    reset = False
    start = pyb.millis()

    while True:
        if pyb.millis() - start > 2000 and fire:
            print(f"servo time {pyb.millis()}")
            servo.set_servo_ang(30)
            print(f"servo time {pyb.millis()}")
            print("FIREDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            fire = False
        elif pyb.millis() - start > 3000 and not reset:
            print(f"servo time {pyb.millis()}")
            servo.set_servo_ang(0)
            print(f"servo time {pyb.millis()}")
            reset = True
            print("RESET SERVOooooooooooooooooo")
        yield 0

def MLX_Cam_fcn(shares):
        # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)


    # Create the camera object and set it up in default mode
    camera = mlx.MLX_Cam(i2c_bus)
    camera.init_VCP()
    camera.send_bool = False

    start = pyb.millis()
    fired = False

    # Unpack shares
    cam_yaw, cam_pitch, cam_bool = shares
    cam_yaw.put(0)
    
    while True:
        if pyb.millis() - start > 5000 and not fired:        
            # Unpack shares
            cam_yaw, cam_pitch, cam_bool = shares

            # Get and image and see how long it takes to grab that image
            print("Click.", end='')
            begintime = time.ticks_ms()
            image = camera.get_image()
            print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
            
            if camera.send_bool:
                camera.u2.write("Data_Start\r\n")
                for line in camera.serial_send(image):
                    #print(line)
                    camera.u2.write(line)

                camera.u2.write("Data_Stop\r\n")

            angle_delta_yaw, angle_delta_pitch = camera.target(image.pix)

            cam_yaw.put(angle_delta_yaw)
            cam_pitch.put(angle_delta_pitch)

            fired = True

            #print(f"angle_delta_yaw = {cam_yaw.get()} degrees")
            #print(f"angle_delta_pitch = {cam_pitch.get()} degrees")

        yield 0

def mastermind(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    #Unpack old target angles
    yaw_set_angle, pitch_set_angle, cam_yaw, cam_pitch, cam_bool = shares

    new_yaw_target = 0
    new_pitch_target = 0
    start = pyb.millis()
    start2 = pyb.millis()
    
    last_posn = 0
    cam_bool.put(0)

    a = 120+12 # inches distance from camera to target
    l = 192 #inches; length of gun to target
    tpd = 362 #ticks/degree

    while True:
        if cam_yaw.get() == 0: #catches divide by zero error
            b = 0 
        else:
            b = a / math.tan(math.radians(cam_yaw.get()))
        print(f"CAMERA YAW: {cam_yaw.get()}")
        new_yaw_target = round(180*tpd - math.degrees(math.atan(b/l)) * tpd )
        print(f"New yaw target {new_yaw_target}")
        '''
        if last_posn == yaw_set_angle: #unverified
            cam_bool = 1
            print("CAMERA ON")
        '''
        #Update with new target angles
        yaw_set_angle.put(new_yaw_target)

        #last_posn = new_yaw_target
        #cam_bool.put(cam_bool)
        pitch_set_angle.put(new_pitch_target)
        
        yield 0

# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    yaw_set_angle = task_share.Share('l', thread_protect=False, name="yaw_set_angle")
    pitch_set_angle = task_share.Share('l', thread_protect=False, name="pitch_set_angle")
    cam_target_yaw = task_share.Share('f', thread_protect=False, name="cam_target_yaw")
    cam_target_pitch = task_share.Share('f', thread_protect=False, name="cam_target_pitch")
    cam_bool = task_share.Share('B', thread_protect=False, name="cam_bool")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    yaw_mtr_task = cotask.Task(yaw_mtr_fcn, name="yaw_mtr_task", priority=1, period=1,
                        profile=True, trace=False, shares=(yaw_set_angle))
    pitch_mtr_task = cotask.Task(pitch_mtr_fcn, name="pitch_mtr_task", priority=2, period=1,
                        profile=True, trace=False, shares=(pitch_set_angle))
    
    trigger_mtr_task = cotask.Task(trigger_mtr_fcn, name="trigger_motor_task", priority=4, period=20,
                    profile=True, trace=False)
    
    MLX_Cam_task = cotask.Task(MLX_Cam_fcn, name="MLX_Cam_task", priority=4, period=100,
                    profile=True, trace=False, shares = (cam_target_yaw, cam_target_pitch, cam_bool))
    
    task_mastermind = cotask.Task(mastermind, name="mastermind_task", priority=3, period=30,
                    profile=True, trace=False, shares=(yaw_set_angle, pitch_set_angle, cam_target_yaw, cam_target_pitch, cam_bool)) 
    
    cotask.task_list.append(yaw_mtr_task)
    #cotask.task_list.append(pitch_mtr_task)
    #cotask.task_list.append(trigger_mtr_task)
    cotask.task_list.append(MLX_Cam_task)
    cotask.task_list.append(task_mastermind)

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
    print(MLX_Cam_task.get_trace())
    print(yaw_mtr_task.get_trace())    
    print('')
