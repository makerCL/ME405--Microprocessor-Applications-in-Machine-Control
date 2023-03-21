"""!
@file main.py

@brief Main file for Nerf Sentry gun that handles multi-tasking.

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
    """!
    @brief Yaw motor task; motor position control tuned with P controller
    @param Shares share variables for task; set point for yaw motor to rotate to
    """

    ## Initialization state 0 
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
    
    # After initialization, the task unpacks the set point and runs the motor controller.
    while True:
        #unpack shares
        yaw_target = shares
        #Update Target
        mc.set_setpoint(yaw_target.get()) 
        encd.read() #runs encoder reader, updating object property
        mc.run(encd.position) #runs controller based on latest position reading     
        moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result
        yield 0   

def pitch_mtr_fcn(shares):
    """!
    @brief pitch motor task; motor position control tuned with PI controller
    @param Shares share variables for task; set point for pitch motor to rotate to
    """

    ## Initialization State 0
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
    mc.set_ki(0.005)    # Integral control needed to achieve zero steady state error.
    encd.zero() #zeroes encoder posn

    # After initialization, the task unpacks the set point and runs the motor controller.
    while True:
        #unpack shares
        pitch_target = shares
        #Update Target
        mc.set_setpoint(pitch_target.get()) 
        encd.read() #runs encoder reader, updating object property
        mc.run(encd.position) #runs controller based on latest position reading
        moe.set_duty_cycle (mc.PWM) #set new duty cycle based on controller result
        yield 0 


def trigger_mtr_fcn(shares):
    """!
    @brief task to control actuation of the trigger
    @param shares share variables for task; fire flag set in mastermind
        fire = 0 indicates "do not fire"
        fire = 1 indicates "fire"
    """
    ## Initialization State 0
    ## Initialize the servo motor pin
    PA9 = pyb.Pin.board.PA9
    timer = 1
    ch = 2
    servo = sc.servo_controller(PA9, timer, ch)
    servo.set_servo_ang(45)
    fire = shares
    fire.put(0)	# Initialize fire flag to "dont fire"
    fire_t = pyb.millis()
    
    # After initalization set the servo position to actuate the trigger when the share 'fire' is 1.
    # One second after fireing, reset the servo position
    while True:
        fire = shares
        if fire.get() == 1:
            servo.set_servo_ang(90)
            print("FIREDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            fire_t = pyb.millis() # time at fire
            fire.put(0)	# clear fire command
        elif fire.get() == 0 and pyb.millis() - fire_t > 1000:
            servo.set_servo_ang(45) # Reset servo position     
        yield 0

def MLX_Cam_fcn(shares):
    """!
    @brief Thermal Camera Task
    @param Shares share variables; cam_target_yaw and cam_target_pitch for angles for angle
        deltas to center; take_pic is flag to indicate should take image when told by mastermind task
    """
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

    camera.send_bool = True
    
    ## After initialization, take a photo when take_pic == 1
    ## Store the desired yaw and pitch angle from the camera field of view in the shared variable with mastermind
    while True:
        # Unpack shares
        cam_target_yaw, cam_target_pitch, take_pic = shares
        if take_pic.get() == 1:        
            # Get and image and see how long it takes to grab that image
            print("Click.", end='')
            begintime = time.ticks_ms()
            image = camera.get_image()
            print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
            
            if camera.send_bool:
                camera.u2.write("Data_Start\r\n")
                for line in camera.serial_send(image):
                    camera.u2.write(line)

                camera.u2.write("Data_Stop\r\n")

            angle_delta_yaw, angle_delta_pitch = camera.target(image.pix)

            cam_target_yaw.put(angle_delta_yaw)
            cam_target_pitch.put(angle_delta_pitch)
            take_pic.put(2)         # Tell mastermind that a picture has been taken
        yield 0

def mastermind(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares has access to and sets/reads all variables between tasks. Mastermind handles all
        major program flow and logic; other tasks contain only functionality for their own functions
    """
    def user_callback(line, user_flag):
        print("user_callback")
        user_flag[0] = 1
        
    #Configure Interrupt for "start button"
    user_flag = [0] # user input flag
    user_interrupt = pyb.ExtInt(pyb.Pin.board.PC2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, lambda line: user_callback(line, user_flag))

    #Unpack old target angles
    yaw_set_angle, pitch_set_angle, cam_target_yaw, cam_target_pitch, take_pic,fire = shares

    new_yaw_target = 0
    new_pitch_target = 0
    start = pyb.millis()
    start2 = pyb.millis()

    #Trigonometry information based on table length and camera positioning to convert camera field of view to gun field of view
    a = 192-51 # inches distance from camera to target
    l = 192 #inches; length of gun to target
    tpd = 362 #ticks/degree
    scale_factor = 0.95

    # Holding pattern until user start button is pressed
    while not user_flag[0]:
        yield 0
        
    t_init = pyb.millis()   # After the button has been pressed record the start time
    wait = 1


    while True:
        #Rotation and movement delay, per game rules
        if pyb.millis() - t_init > 1000 and wait == 1:
            new_yaw_target = 180*tpd
            wait = 0

        if pyb.millis() - t_init > 5500 and take_pic.get() in {0, 1}:
            take_pic.put(1)

        elif take_pic.get() == 2: # Once the picture has been taken update position     
            #Camera trig functions
            b = a * math.tan(math.radians(cam_target_yaw.get()))
            print(f"CAMERA YAW: {cam_target_yaw.get()}")
            tick_delta = math.degrees(math.atan(b/l)) * tpd
            new_yaw_target = round(180*tpd +  scale_factor * tick_delta)
           ## Hard stops that describe the encoder position at each side of the table
            if new_yaw_target > 67700:
                new_yaw_target = 67700
                print('yaw = max left')
            elif new_yaw_target < 63000:
                new_yaw_target = 63000
                print('yaw = max right')

            print(f"New yaw target {new_yaw_target}")
            #Update with new target angles
            yaw_set_angle.put(new_yaw_target)
            pitch_set_angle.put(0) #does not implement pitch data from camera at this time
       
        if pyb.millis() - t_init > 9000 and take_pic.get() in {2}: # After 9 seconds and when camera task has indicated that a picture has been taken
            print('mastermind fire')
            fire.put(1) # send signal to pull trigger
            take_pic.put(0) # allow new picture to be taken
            t_init = pyb.millis()
        yaw_set_angle.put(new_yaw_target)
        pitch_set_angle.put(0) 
        yield 0


if __name__ == "__main__":
    print("SENTRY ENGAGED!")

    # Create a share and a queue to test function and diagnostic printouts
    yaw_set_angle = task_share.Share('l', thread_protect=False, name="yaw_set_angle")
    pitch_set_angle = task_share.Share('l', thread_protect=False, name="pitch_set_angle")
    cam_target_yaw = task_share.Share('f', thread_protect=False, name="cam_target_yaw")
    cam_target_pitch = task_share.Share('f', thread_protect=False, name="cam_target_pitch")
    take_pic = task_share.Share('b', thread_protect=False, name="take_pic")
    fire = task_share.Share('b', thread_protect=False, name="fire")


    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    yaw_mtr_task = cotask.Task(yaw_mtr_fcn, name="yaw_mtr_task", priority=1, period=20,
                        profile=True, trace=False, shares=(yaw_set_angle))
    pitch_mtr_task = cotask.Task(pitch_mtr_fcn, name="pitch_mtr_task", priority=2, period=50,
                        profile=True, trace=False, shares=(pitch_set_angle))
    
    trigger_mtr_task = cotask.Task(trigger_mtr_fcn, name="trigger_motor_task", priority=4, period=20,
                    profile=True, trace=False,shares = (fire))
    
    MLX_Cam_task = cotask.Task(MLX_Cam_fcn, name="MLX_Cam_task", priority=5, period=100,
                    profile=True, trace=False, shares = (cam_target_yaw, cam_target_pitch, take_pic))
    
    task_mastermind = cotask.Task(mastermind, name="mastermind_task", priority=3, period=50,
                    profile=True, trace=False, shares=(yaw_set_angle, pitch_set_angle, cam_target_yaw, cam_target_pitch, take_pic,fire)) 
    
    cotask.task_list.append(yaw_mtr_task)
    cotask.task_list.append(pitch_mtr_task)
    cotask.task_list.append(trigger_mtr_task)
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
    #print(MLX_Cam_task.get_trace())
    #print(yaw_mtr_task.get_trace())    
    print('')
