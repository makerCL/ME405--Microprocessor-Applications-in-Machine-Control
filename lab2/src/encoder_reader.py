'''!
@file       encoder_reader.py

@brief		Encoder reader class

@author		Caleb Erlenborn
@author     Miles Alderman
@author     Yamil Silva

@date		January 31, 2023

'''


import pyb
class EncoderReader:
    """! 
    This class implements an encoder reader for an ME405 kit. 
    """
    def __init__ (self, enc_pin1, enc_pin2, timer):
        """! 
        Creates an encoder reader 
        @param timer the timer number that the 2 encoder channels are created on
        @param enc_pin1 the pin used for first encoder channel
        @param enc_pin2 the pin used for the second encoder channel
        
        """
        #create timer and 2 encoder channels
        self.time = pyb.Timer(timer, prescaler=0,period=0xFFFF)
        self.time_ch1 = self.time.channel (1, pyb.Timer.ENC_AB, pin = enc_pin1)
        self.time_ch2 = self.time.channel (2, pyb.Timer.ENC_AB, pin = enc_pin2)

        self.position = 0 # Set the current position to zero
        
        self.last_count = self.time.counter() #the most recent saved counter reading, used for time delta
        print ("Creating a encoder driver")    
    def read (self):
        """!
        Function that reads the position of the encoder while detecting under/overflow conditions. 
        Once read, the position is saved to the position property of the object
        """
        self.delta = self.time.counter() - self.last_count #current timer count - saved count from last reading
        
        #auto reload value: 2^16 - 1 since we have 16 bit counter
        AR = 65535 

        #overflow detection
        if self.delta > (AR+1)/2: 	# Underflow condition
            self.delta -= AR+1
        elif self.delta < -(AR+1)/2: # Overflow condition
            self.delta += AR+1

        self.position += self.delta # add delta, scaled with under/overflow condition, to current position
        self.last_count = self.time.counter() # update last count

    def zero (self):
        """!
        Function that zeros the encoder position at the current position.
        """
        self.position = 0 
        self.last_count = self.time.counter()

# Block of code to test Encoder
if __name__ == '__main__':
    import time
    enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
    enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
    timer = 8
    #encoder reader instantiation
    encd = EncoderReader (enc_pin1, enc_pin2, timer)

    
    while True:
        encd.read() #update the reading
        print(encd.position) # print the new position
        time.sleep(0.1) #sleep for 0.1 seconds, approximately 10Hz (slightly less due to runtime of code)

        '''
        Note: the better way to run this at 10 Hz would be through setting up an interupt, that way despite other
        operations the timing is guarenteed of the encoder reading. While not asked to for this lab, next time we would do this
        '''
