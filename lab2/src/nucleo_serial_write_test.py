import pyb


print("Starting nucleo send")
#ser = serial.Serial('/dev/cu.usbmodem207537B3424B2')  # open serial port
ser = pyb.USB_VCP()


pyb.repl_uart(None)

u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port

for number in range(10):               # Just some example output
    u2.write(f"Count: {number}\r\n")   # The "\r\n" is end-of-line stuff
    number += 1  

