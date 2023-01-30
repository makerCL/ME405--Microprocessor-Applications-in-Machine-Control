import pyb
import motor_driver as md

en_pin = pyb.Pin.board.PC1
in1pin = pyb.Pin.board.PA0
in2pin = pyb.Pin.board.PA1
timer = 5
moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)
moe.set_duty_cycle (-42)
