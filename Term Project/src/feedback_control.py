
'''!
@file       feedback_control.py

@brief		Feedback Controller Class

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		Febuary 7, 2023

'''

import pyb

class FeedbackControl:
    '''!
    This class implements a porportional controller for ME405 lab kit
    DC motor with encoder.
    '''
    def __init__(self, setpoint = 0, k_p = 0, k_i = 0, k_d = 0):
        '''! Initializes the feedback controller
        @param setpoint The encoder setpoint [stepper counts]
        @param k_p Controller proportional gain [PWM/count]
        '''
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.setpoint = setpoint
        self.PWM = 0
        self.pos_data = []

        self.error_sum = 0
        self.last_error = 0
        
    def run(self, current_theta):
        '''! Calculates the PWM setpoint for porportional controller
        @param setpoint The encoder setpoint [stepper counts]
        @param k_p Controller proportional gain [PWM/count]
        @param current_theta The current encoder reading
        '''
        
        error = self.setpoint - current_theta
        self.error_sum += error

        self.PWM = self.k_p * error + self.k_i * self.error_sum + self.k_d * (error - self.last_error)
        self.last_error = error

        
    def set_setpoint(self, setpoint):
        '''! Sets the desired encoder position
        @param setpoint The encoder setpoint [stepper counts]
        '''
        self.setpoint = setpoint
        
    def set_kp(self,k_p):
        '''! Sets the proportional gain of controller
        @param k_p Controller proportional gain [PWM/count]
        '''
        self.k_p = k_p
    
    def set_ki(self,k_i):
        '''! Sets the proportional gain of controller
        @param k_i Controller integral gain 
        '''
        self.k_i = k_i
    
    def set_kd(self,k_d):
        '''! Sets the proportional gain of controller
        @param k_d Controller derivative gain 
        '''
        self.k_d = k_d
    
    def print_pos_data(self):
        '''! Prints the position and time data stored in self.pos_data
        '''
        print("Printing position data")
        for point in self.pos_data:
            print(point)
    
    def add_point(self, point):
        '''! Appends position and time data point to self.pos_data
        @param point The time and encoder position reading
        '''
        self.pos_data.append(point)
        
    def init_VCP(self):
        '''! Initializes the VCP to send data via USB
        '''
        print("Starting nucleo send")
        try:
            self.vcp = pyb.USB_VCP()
            pyb.repl_uart(None)	# Turn off the REPL on UART2
            self.u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port
        except:
            print("Problem openning VCP/UART")
            
    def data_transfer(self):
        '''! Transfers data stored in pos_data via VCP
        '''
        #data is list of lists
        #Make sure that VCP has been properly initalized
        if not self.vcp.isconnected():
            print("VCP not proeprly initialized")
            return
        else:
            self.u2.write(f"Data_Start\r\n") # Send message to start recording data
            for point in self.pos_data:
                x_val, y_val = point[0], point[1]
                self.u2.write(f"{x_val},{y_val}\r\n")   # The "\r\n" is end-of-line stuff
            self.u2.write(f"Data_End\r\n") # Send message that data has ended
    
    def data_clear(self):
        '''! Clears the data stored in position data
        '''
        self.pos_data = []
        
#### TEST CODE #############################

if __name__ == '__main__':
    import encoder_reader as er
    import motor_driver as md
    import pyb
    
    ## Create Motor Driver Obejct for 1A motor
    en_pin = pyb.Pin.board.PA10
    in1pin = pyb.Pin.board.PB4
    in2pin = pyb.Pin.board.PB5
    timer = 3
    moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)
    
    enc_pin1 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
    timer = 4
    encd = er.EncoderReader (enc_pin1, enc_pin2, timer)
    
    mc = FeedbackControl()
    mc.set_setpoint(3000)
    mc.set_kp(0.1)
    
    while True:   
        encd.read()
        mc.run(encd.position)
        moe.set_duty_cycle (mc.PWM)
        print(encd.position)
    