
'''!


'''
import pyb

class FeedbackControl:
    '''!
    @param k_p The controller proportional gain [PWM/count]
    @param setpoint	The motor setpoint in [stepper counts]
    @param PWM 
    '''
    def __init__(self, setpoint = 0, k_p = 0):
        self.k_p = k_p
        self.setpoint = setpoint
        self.PWM = 0
        self.pos_data = []
        
    def run(self, current_theta):
        self.PWM = self.k_p*(self.setpoint - current_theta)
        
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
        
    def set_kp(self,k_p):
        self.k_p = k_p
    
    def print_pos_data(self):
        print("Printing position data")
        for point in self.pos_data:
            print(point)
    
    def add_point(self, point):
        self.pos_data.append(point)
        
    def init_VCP(self):
        print("Starting nucleo send")
        #ser = serial.Serial('/dev/cu.usbmodem207537B3424B2')  # open serial port
        try:
            self.vcp = pyb.USB_VCP()
            pyb.repl_uart(None)
            self.u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port
        except:
            print("Problem openning VCP/UART")

        #TODO lots of possible errors/edge cases here that we should try to catch
            
    def data_transfer(self):
        #data is list of lists, each list is 
        #Make sure that VCP has been properly initalized
        if not self.vcp.isconnected():
            print("VCP not proeprly initialized")
            return
        else:
            for point in self.pos_data:
                x_val, y_val = point[0], point[1]
                self.u2.write(f"{x_val},{y_val}\r\n")   # The "\r\n" is end-of-line stuff

    def data_clear(self):
        self.pos_data = []
        
           
#### TEST CODE #############################

if __name__ == '__main__':
    import encoder_reader as er
    import motor_driver as md
    import pyb
    
    en_pin = pyb.Pin.board.PC1
    in1pin = pyb.Pin.board.PA0
    in2pin = pyb.Pin.board.PA1
    timer = 5
    moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)
    
    enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    timer = 8
    encd = er.EncoderReader (enc_pin1, enc_pin2, timer)
    
    mc = FeedbackControl()
    mc.set_setpoint(8000)
    mc.set_kp(0.5)
    
    while True:   
        encd.read()
        mc.run(encd.position)
        moe.set_duty_cycle (mc.PWM)
    