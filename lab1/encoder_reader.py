import pyb
class EncoderReader:
    """! 
    This class implements an encoder reader for an ME405 kit. 
    """
    def __init__ (self, enc_pin1, enc_pin2, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several pin parameters)
        """
        self.time = pyb.Timer(timer, prescaler=0,period=0xFFFF)
        self.time_ch1 = self.time.channel (1, pyb.Timer.ENC_AB, pin = enc_pin1)
        self.time_ch2 = self.time.channel (2, pyb.Timer.ENC_AB, pin = enc_pin2)
        self.position = 0 # Set the current position to zero
        self.last_count = self.time.counter()
        print ("Creating a encoder driver")    
    def read (self):
        """!
        Insert Description
        @param 
        """
        self.delta = self.time.counter() - self.last_count
        AR = 65535
        if self.delta > (AR+1)/2: 	# Underflow condition
            self.delta -= AR+1
        elif self.delta < -(AR+1)/2: # Overflow condition
            self.delta += AR+1
        self.position += self.delta
        self.last_count = self.time.counter()
    def zero(self):
        self.position = 0
        self.last_count = self.time.counter()

# Block of code to test Encoder
if __name__ == '__main__':
    import time
    enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    timer = 8
    encd = EncoderReader (enc_pin1, enc_pin2, timer)
    while True:
        encd.read()
        print(encd.position)
        time.sleep(0.1)


