"""!
@file mlx_cam.py
This file contains a wrapper that facilitates the use of a Melexis MLX90640
thermal infrared camera for general use. The wrapper contains a class MLX_Cam
whose use is greatly simplified in comparison to that of the base class,
@c class @c MLX90640, by mwerezak, who has a cool fox avatar, at
@c https://github.com/mwerezak/micropython-mlx90640

To use this code, upload the directory @c mlx90640 from mwerezak with all its
contents to the root directory of your MicroPython device, then copy this file
to the root directory of the MicroPython device.

There's some test code at the bottom of this file which serves as a beginning
example.

@author mwerezak Original files, Summer 2022
@author JR Ridgely Added simplified wrapper class @c MLX_Cam, January 2023
@copyright (c) 2022 by the authors and released under the GNU Public License,
    version 3.
"""

import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from ulab import numpy as np
import pyb

class MLX_Cam:
    """!
    @brief   Class which wraps an MLX90640 thermal infrared camera driver to
             make it easier to grab and use an image.
    """

    def __init__(self, i2c, address=0x33, pattern=ChessPattern,
                 width=NUM_COLS, height=NUM_ROWS):
        """!
        @brief   Set up an MLX90640 camera.
        @param   i2c An I2C bus which has been set up to talk to the camera;
                 this must be a bus object which has already been set up
        @param   address The address of the camera on the I2C bus (default 0x33)
        @param   pattern The way frames are interleaved, as we read only half
                 the pixels at a time (default ChessPattern)
        @param   width The width of the image in pixels; leave it at default
        @param   height The height of the image in pixels; leave it at default
        """
        ## The I2C bus to which the camera is attached
        self._i2c = i2c
        ## The address of the camera on the I2C bus
        self._addr = address
        ## The pattern for reading the camera, usually ChessPattern
        self._pattern = pattern
        ## The width of the image in pixels, which should be 32
        self._width = width
        ## The height of the image in pixels, which should be 24
        self._height = height

        # The MLX90640 object that does the work
        self._camera = MLX90640(i2c, address)
        self._camera.set_pattern(pattern)
        self._camera.setup()

        ## A local reference to the image object within the camera driver
        self._image = self._camera

        #initialize image data array
        self.target_arr = np.empty((24, 32), dtype=np.uint8)

    def get_image(self):
        """!
        @brief   Get one image from a MLX90640 camera.
        @details Grab one image from the given camera and return it. Both
                 subframes (the odd checkerboard portions of the image) are
                 grabbed and combined (maybe; this is the raw version, so the
                 combination is sketchy and not fully tested). It is assumed
                 that the camera is in the ChessPattern (default) mode as it
                 probably should be.
        @returns A reference to the image object we've just filled with data
        """
        for subpage in (0, 1):
            while not self._camera.has_data:
                time.sleep_ms(50)
                print('.', end='')
            image = self._camera.read_image(subpage)

        return image

    def serial_send(self, array):
        """!
        @brief   Send thermal image via serial to computer for heatmap display 

        """
        print(array)
        for row in range(self._height):
            line = ""
            for col in range(self._width):
                pix = int(array[row * self._width + col])
                if col:
                    line += ","
                line += f"{pix}"
            line += "\r\n"
            yield line


    def target(self, array):
        print("TARGET (array)")

        print(array)
        if len(array) != self._height * self._width:
            print("Invalid Array size")
            return

        self.target_arr = np.array(array, dtype=np.int16).reshape((self._height, self._width))
 
        print(f"np_arr[0][0] = {self.target_arr[0][0]}")
        print(f"np_arr[1][4] = {self.target_arr[1][4]}")
        print(f"np_arr[23][32] = {self.target_arr[23][31]}")
        print(f"np_arr[12][12] = {self.target_arr[12][12]}")
        print(f"np_arr[5][6] = {self.target_arr[5][6]}")

        max_temp = np.max(self.target_arr)
        min_temp = np.min(self.target_arr)

        #Create mask where the heat is higher than a certain value
        #TODO: future iteration the mask would make more sense as absolute temperature.
        spread = max_temp - min_temp
        threshold = 0.8

        mask = (self.target_arr > min_temp + threshold *spread)
        #Find centroid of target by averaging the indexes of filtered points
        print(mask)
        # find the indices of true values in the array
        indices = np.nonzero(mask)

        # calculate the average indices of true values
        avg_index = np.mean(indices, axis=1)
        print(avg_index)
        centr_y, centr_x = np.array(np.where(mask,1,0)).mean(axis=1)

        # Ideal Setpoint as seen on thermal camera
        yaw_center = self._width / 2 #centered, pixels from left
        pitch_center = self._height / 2 #cetnered, pixels top; may change with distance/velocity
        
    def init_VCP(self):
        print("Starting nucleo send")
        try:
            self.vcp = pyb.USB_VCP()
            pyb.repl_uart(None)	# Turn off the REPL on UART2
            self.u2 = pyb.UART(2, baudrate=115200)      # Set up the second USB-serial port
        except:
            print("Problem openning VCP/UART")
        else:
            if self.vcp.isconnected():
                print("VCP connected")
            else:
                print("VCP ERROR")
        



# The test code sets up the sensor, then grabs and shows an image in a terminal
# every ten and a half seconds or so.
## @cond NO_DOXY don't document the test code in the driver documentation
if __name__ == "__main__":

    # The following import is only used to check if we have an STM32 board such
    # as a Pyboard or Nucleo; if not, use a different library
    try:
        from pyb import info

    # Oops, it's not an STM32; assume generic machine.I2C for ESP32 and others
    except ImportError:
        # For ESP32 38-pin cheapo board from NodeMCU, KeeYees, etc.
        i2c_bus = I2C(1, scl=Pin(22), sda=Pin(21))

    # OK, we do have an STM32, so just use the default pin assignments for I2C1
    else:
        i2c_bus = I2C(1)

    print("MXL90640 Easy(ish) Driver Test")

    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    print(f"I2C Scan: {scanhex}")

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)


    camera.init_VCP()
    

    while True:
        try:
            # Get and image and see how long it takes to grab that image
            print("Click.", end='')
            begintime = time.ticks_ms()
            image = camera.get_image()
            print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
            
            serial_send = True
            
            if serial_send:
                camera.u2.write("Data_Start\r\n")
                for line in camera.serial_send(image):
                    #print(line)
                    camera.u2.write(line)

                camera.u2.write("Data_Stop\r\n")

            camera.target(image.pix)

            time.sleep_ms(5000)

        except KeyboardInterrupt:
            break

    print ("Done.")

## @endcond End the block which Doxygen should ignore


