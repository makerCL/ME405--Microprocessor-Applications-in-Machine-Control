class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several pin parameters)
        """
        self.EN = pyb.Pin (pyb.Pin.board.en_pin, pyb.Pin.OUT_OD)
        self.IN_1 = pyb.Pin (pyb.Pin.board.in1pin, pyb.Pin.OUT_PP)
        self.IN_2 = pyb.Pin (pyb.Pin.board.in2pin, pyb.Pin.OUT_PP)
        self.time = pyb.Timer(timer, prescaler=0,period=0xFFFF)
        self.time_ch1 = time.channel (1, pyb.Timer.PWM, pin = IN_1B)
        self.time_ch2 = time.channel (2, pyb.Timer.PWM, pin = IN_2B)
        print ("Creating a motor driver")
        
    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        self.EN.high()
        print (f"Setting duty cycle to {level}")