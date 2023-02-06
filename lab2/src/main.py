import encoder_reader as er
import motor_driver as md
import feedback_control as fc
import pyb
import utime

en_pin = pyb.Pin.board.PC1
in1pin = pyb.Pin.board.PA0
in2pin = pyb.Pin.board.PA1
timer = 5
moe = md.MotorDriver (en_pin, in1pin, in2pin, timer)

enc_pin1 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
enc_pin2 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
timer = 8
encd = er.EncoderReader (enc_pin1, enc_pin2, timer)

mc = fc.FeedbackControl()
mc.init_VCP()
mc.set_setpoint(1000)


while True:
    kp = ''
    while kp == '':
        inp = input('Enter Kp ')
        try:
            kp = float(inp)
            mc.set_kp(kp)
        except:
            print("Please enter valid Kp")    
    t = 0
    start_time = pyb.millis()
    encd.zero()
    mc.data_clear()
    
    while t<1000:   
        encd.read()
        mc.run(encd.position)
        moe.set_duty_cycle (mc.PWM)
        
        #append current time and position data point
        t =pyb.millis() - start_time
        mc.add_point([t, encd.position])
        utime.sleep_ms(10)

    mc.data_transfer()
    mc.print_pos_data()
    moe.set_duty_cycle (0)

while True:
    utime.sleep_ms(10)
