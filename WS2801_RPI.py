import spidev
import logging

_BUS = 0
_DEVICE = 0
_MAX_SPEED_HZ = 1000000
_LEDS = 128
__rgb_leds =  [0 for i in range(_LEDS*3)]

# initialize SPI
# this should meet the requirements of WS2801
spi = spidev.SpiDev()

def flush():
   spi.open(_BUS, _DEVICE)
   spi.mode = 0
   spi.max_speed_hz =_MAX_SPEED_HZ
   spi.lsbfirst = True
#   logging.info(str.format("WS2801_RPI.py: SPI successfully initialized with speed: {}", _MAX_SPEED_HZ))
   spi.writebytes(__rgb_leds)
   spi.close()
   return

def clear():
   __rgb_leds[:] =  [0 for i in range(_LEDS*3)]

def set_leds(pixels, rgb_values=[255,255,255]):
   """ set list pixels to list of list of rgb_values
   set_pixels([1,3,5],[[155,0,0],[0,0,0],[0,27,58]]) will set pixels 1,3 and 5 to rgb values given
   if length(rgb_values) < list(pixels) the last entry of rgb_values will count for the rest of the pixels
   if pixel is a number only one pixel will be set"""

# check input validity
   if not type(pixels) is int:
       if not type(pixels) is list:
           raise TypeError("WS2801_RPI.set_pixels attribute pixels must be an int addressing one of the available LEDs or a list of ints")
       for val in pixels:
           if (not type(val) is int) or val < 1 or val > _LEDS:
               raise TypeError("WS2801_RPI.set_pixels attribute pixels must be an int addressing one of the available LEDs or a list of ints")
   if not type(rgb_values) is list:
       raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints between 0 and 255 or a list of lists with rgb values")
   if type(rgb_values[0]) is list:
       for rgb_value in rgb_values:
           if not type(rgb_value) is list:
               raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints for rgb or a list of lists with rgb values")
           if not len(rgb_value) == 3:
               raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints for rgb or a list of lists with rgb values")
           for i in rgb_value:
               if (not type(i) is int) or i < 0 or i > 255:
                   raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints for rgb or a list of lists with rgb values")
   else:
       if not len(rgb_values) == 3:
           raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints for rgb or a list of lists with rgb values")
       for i in rgb_values:
           if (not type(i) is int) or i < 0 or i > 255:
               raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an list containing 3 ints for rgb or a list of lists with rgb values")

# write into __rgb_leds
   if type(pixels) is int:
      pixels = [pixels]
   if type(rgb_values[0]) is int:
       tmp = []
       tmp.append(rgb_values)
       rgb_values = tmp
   for i, val in enumerate(pixels):
       if i < len(rgb_values):
           rgb = rgb_values[i]
       __rgb_leds[(val-1)*3:(val)*3] = rgb

# some final sanity checks
   if len(__rgb_leds) != _LEDS*3:
       raise RuntimeException("Something weired happend: Buffer overflow");
   if len(pixels) > len(rgb_values):
       logging.warn("WS2801_RPI.py set_leds: more leds addressed than rgb values given: assume last rgb for remaining leds")
   if len(pixels) < len(rgb_values):
       logging.warn("WS2801_RPI.py set_leds: too many rgb values supplied: skipping")
