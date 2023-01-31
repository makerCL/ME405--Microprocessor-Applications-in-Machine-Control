'''!
@file       motor_driver.py

@brief		Motor driver class

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		January 31, 2023

'''


import pyb

class MotorDriver:
    """! 
    This class implements a DC motor driver for an ME405 kit
    """
    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin enable pin for H-bridge
        @param in1pin first control pin of H bridge
        @param in2pin second control pin of H bridge
        @param timer number to use
        """
        #setup H bridge- open drain with pullups enabled
        self.EN = pyb.Pin (en_pin, pyb.Pin.OUT_OD, pull = pyb.Pin.PULL_UP) 

        # PWM h bridge pins setup
        self.IN_1 = pyb.Pin (in1pin, pyb.Pin.OUT_PP)
        self.IN_2 = pyb.Pin (in2pin, pyb.Pin.OUT_PP)

        #create timer
        self.time = pyb.Timer(timer, prescaler=0,period=0xFFFF)
        self.time_ch1 = self.time.channel (1, pyb.Timer.PWM, pin = self.IN_1)
        self.time_ch2 = self.time.channel (2, pyb.Timer.PWM, pin = self.IN_2)
        print ("Creating a motor driver")
        
    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor. 
               (+) for clockwise
               (-) for anticlockwise
        """
        self.EN.value([True]) #enable motor

        if level < 0: # conditional logic determines directionality motor
            # which channel the pwm is sent on determines direction in H bridge
            self.time_ch1.pulse_width_percent(abs(level)) 
            self.time_ch2.pulse_width_percent(0)
        elif level > 0:
            self.time_ch1.pulse_width_percent(0)
            self.time_ch2.pulse_width_percent(abs(level))
        print (f"Setting duty cycle to {level}")

# Block of code to test Motor
if __name__ == '__main__':
    en_pin = pyb.Pin.board.PC1
    in1pin = pyb.Pin.board.PA0
    in2pin = pyb.Pin.board.PA1
    timer = 5
    moe = MotorDriver (en_pin, in1pin, in2pin, timer)
    moe.set_duty_cycle (-42)        
