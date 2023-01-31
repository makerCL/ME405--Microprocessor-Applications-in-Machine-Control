import pyb
import motor_driver as md
import encoder_reader as er
import time

en_pin = pyb.Pin.board.PC1
in1pin = pyb.Pin.board.PA0
in2pin = pyb.Pin.board.PA1
timer = 5
moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)


enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
timer = 8
encd = er.EncoderReader (enc_pin1, enc_pin2, timer)


moe.set_duty_cycle (0)

start_time = pyb.millis()
test_time = 0

#Testing constant duty cycle
while test_time < 5:
    test_time = (pyb.millis() - start_time)/1000
    encd.read()
    print(encd.position)
    time.sleep(0.1)
 
print("Done testing!")

    
    

