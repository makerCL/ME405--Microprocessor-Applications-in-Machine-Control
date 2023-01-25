"""	!@file		Lab0Main
    @brief		Increases the brightness of an LED over 5 seconds and resets it when it hits 5 seconds.
    
    @author		Caleb Erlenborn
    @author     Miles Alderman
    @author     Yamil Silva
    @date		January 24 2023


"""

import pyb


def led_setup ():
    """!@brief Sets up the LED pin and timers
        @return Returns the timmer channel object

    """
    ## Pin that the LED is feeding into
    pinA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    
    ## Timer created to run the LED change of time
    tim2 = pyb.Timer (2, freq=20000)
    
    ## The PWM channel that controls the LED brightness
    ch1 = tim2.channel (1, pyb.Timer.PWM_INVERTED, pin = pinA0) #inverted since LED ON is logic 0
    return ch1

def led_brightness (t):
    """!@brief Calculates the brightness in % that the LED should be set to
        @return LED brightness in percent"""
    ## LED brightness in %
    ledb = t/50     #5000 millies / 50 = 100
    return ledb

if __name__ == "__main__":
    
    ##A returned copy of the PWM object to change LED brightness
    
    ch1m = led_setup()
    ##initial relative time for system countup
    
    tInit = pyb.millis()
    while True:
        ## Current time difference between refrence time and present time
        cTime = pyb.millis() - tInit
        ch1m.pulse_width_percent(led_brightness(cTime%5000))
           