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
@author Miles Alderman Implemented new functionality for use with in Nerf Sentry, targetting
    algorithm, and serial send capabilities

@date 3/20/23
"""

import utime as time
from machine import Pin, I2C
from mlx90640 import MLX90640
from mlx90640.calibration import NUM_ROWS, NUM_COLS, IMAGE_SIZE, TEMP_K
from mlx90640.image import ChessPattern, InterleavedPattern
from array import array

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

        #Field of view of camera
        self.FOV_yaw = 55 # Degrees
        self.FOV_pitch  = 35 #Degrees #TODO: FIX THESE. PLACEHOLDER

        #Serial sending boolean
        self.send_bool = False

        #Calibration array
        self.calib_arr = array('h', [0]*self._height * self._width)

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
        @param   array array of camera data, 1x32*24 elements of type array
        """
        #print(array)
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
        """!
        @brief Given array of target data, determine the angle difference between the camera and target
        @param array array of camera data, 1x32*24 elements of type array
        """

        # Ideal Setpoint as seen on thermal camera
        yaw_center = self._width / 2 #centered, pixels from left
        pitch_center = self._height / 2 #cetnered, pixels top; may change with distance/velocity

        # list of column average heats
        col_avgs = []

        # Add to list
        for column in range(self._width):
            col = []
            for i in range(0, self._width * self._height, self._width):
                col.append(array[i + column])

            col_avgs.append(sum(col) / len(col))

        # Index of column that has max avg value
        max_col_idx = col_avgs.index(max(col_avgs))

        # Column that has maximum average heat
        max_col = []

        # Extract column
        for i in range(0, self._height*self._width, self._width):
            max_col.append(array[i])

        #Find max value from the top of the row
        vert_max = max_col.index(max(max_col))

        #pixels right of center
        delta_yaw_pix = max_col_idx - yaw_center

        #pixels below center
        delta_pitch_pix = vert_max - pitch_center 

        # Calculate angle delta
        angle_delta_yaw = delta_yaw_pix / self._width * self.FOV_yaw
        angle_delta_pitch = delta_pitch_pix / self._height * self.FOV_pitch

        #NOTE: Pitch is kinda sketchy. Consider averaging indexes of top 3 points, or have fixed aim point
        return angle_delta_yaw, angle_delta_pitch

        
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


    # Select MLX90640 camera I2C address, normally 0x33, and check the bus
    i2c_address = 0x33
    scanhex = [f"0x{addr:X}" for addr in i2c_bus.scan()]
    #print(f"I2C Scan: {scanhex}")

    # Create the camera object and set it up in default mode
    camera = MLX_Cam(i2c_bus)


    camera.init_VCP()
    camera.send_bool = True

    while True:
        try:
            # Get and image and see how long it takes to grab that image
            print("Click.", end='')
            begintime = time.ticks_ms()
            image = camera.get_image()
            print(f" {time.ticks_diff(time.ticks_ms(), begintime)} ms")
            
            if camera.send_bool:
                camera.u2.write("Data_Start\r\n")
                for line in camera.serial_send(image):
                    #print(line)
                    camera.u2.write(line)

                camera.u2.write("Data_Stop\r\n")

            angle_delta_yaw, angle_delta_pitch = camera.target(image.pix)
            #print(f"angle_delta_yaw = {angle_delta_yaw} degrees")
            #print(f"angle_delta_pitch = {angle_delta_pitch} degrees")
            time.sleep_ms(5000)

        except KeyboardInterrupt:
            break

## @endcond End the block which Doxygen should ignore


