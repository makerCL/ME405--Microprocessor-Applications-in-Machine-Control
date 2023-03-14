import pyb
import time

def user_callback(line, user_flag):
    print("user_callback")
    user_flag[0] = 1

def callback2(line):
    print("CUTOFF")
    
user_flag = [0]

user_interrupt = pyb.ExtInt(pyb.Pin.board.PC2, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, lambda line: user_callback(line, user_flag))

kill_interrupt = pyb.ExtInt(pyb.Pin.board.PC3, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, callback2)

while(True):
    time.sleep(1)
    if user_flag[0]:
        print("x")
    else:
        print(".")