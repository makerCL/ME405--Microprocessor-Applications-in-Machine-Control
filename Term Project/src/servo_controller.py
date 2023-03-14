    
'''!
@file       servo_controller.py

@brief		Servo Controller Class

@author		Caleb Erlenborn


@date		March 9, 2023

'''
import pyb
import utime

class servo_controller:
    """! 
    This class implements a servo controller for Miuzei 6V 20kg RC Digital Servo
    """
    def __init__ (self, PN, timer,ch):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param PN Servo controller pin
        @param timer number to use
        @param ch channel to use
        """
        ## Initialize the servo mtor pin
        self.CPN = pyb.Pin (PN, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(timer, prescaler = 79, period = 19999)
        self.time_ch = self.timer.channel (ch, pyb.Timer.PWM, pin = self.CPN)
        print ("Creating a servo driver")
        self.time_ch.pulse_width(1000) # Initialize to 0 degree position
        
    def set_servo_ang (self, angle):
        """!
        This method sets the angle of the servo motor
        
        @param angle The desired servo angle in degrees
        """
        if angle > 180 | angle < 0:
            print('Angle must between 0 and 180 degrees')
        elif angle <= 90:
            pulse = 1000 + angle*500//90  # Pulse width
            self.time_ch.pulse_width(pulse)
            #print (f"Setting angle to {angle}")
            #print(pulse)
        else:
            pulse = 1000 + angle*1500//180  # Pulse width 
            self.time_ch.pulse_width(pulse)
            #print (f"Setting angle to {angle}")
            #print(pulse)

# Block of code to test Motor
if __name__ == '__main__':
    ## Initialize the servo motor pin
    PA9 = pyb.Pin.board.PA9
    timer = 1
    ch = 2
    servo = servo_controller (PA9, timer, ch)

    while True:
        #PNA2.high()
        servo.set_servo_ang(45)
        print('45')
        utime.sleep(5)
        servo.set_servo_ang(90)
        print('90')
        utime.sleep(3)
    
