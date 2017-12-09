"""
Connect WS2801 on a Raspberry Pi (3) using the brilliant spidev lib.

spidev can be found here: https://github.com/doceme/py-spidev.
"""
import spidev
import logging

_BUS = 0
_DEVICE = 0
_MAX_SPEED_HZ = 976000
_LEDS = 128
__rgb_leds = []


# initialize SPI
# this should meet the requirements of WS2801
try:
    spi = spidev.SpiDev()
    spi.open(bus=_BUS, device=_DEVICE)
    spi.mode = 0b00
    spi.max_speed_hz = _MAX_SPEED_HZ
except:
    import traceback
    traceback.print_exc()
    raise


def set_number_of_leds(leds=128):
    """
    Define the number of leds on your strip.

    This function has to be called if different number than 128!
    """
    global _LEDS
    _LEDS = leds
    global __rgb_leds
    __rgb_leds = [0 for i in range(_LEDS*3)]


# initialize the module with 128 leds
set_number_of_leds()


def flush():
    """Send the bits to the leds. No parameters."""
    try:
        spi.writebytes(__rgb_leds)
    except:
        import traceback
        traceback.print_exc()
        raise
    return


def clear():
    "Switch all leds off. Needs a flush() to be active."
    global __rgb_leds
    __rgb_leds[:] = [0 for i in range(_LEDS*3)]


def set_leds(pixels, rgb_values=[255, 255, 255]):
    """Set a list of pixels to list of corresponding rgb_values (given as
    list of 3 values for red, green and blue).

    set_pixels([1,3,5],[[155,0,0],[0,0,0],[0,27,58]]) will set pixels
    1,3 and 5 to rgb values given.
    if length(rgb_values) < list(pixels) the last entry of rgb_values
    will count for the rest of the pixels.
    if pixel is a number only one pixel will be set.
    """
    # check input validity
    global __rgb_leds
    if not type(pixels) is int:
        if not type(pixels) is list:
            raise TypeError("WS2801_RPI.set_pixels attribute pixels must be an \
int addressing one of the available LEDs or a list of ints")
        for val in pixels:
            if (not type(val) is int) or val < 1 or val > _LEDS:
                raise TypeError("WS2801_RPI.set_pixels attribute pixels must \
be an int addressing one of the available LEDs or a list of ints")
    else:
        if pixels > _LEDS or pixels < 1:
            raise TypeError("You are addressing an LED that does not exist")
    if not type(rgb_values) is list:
        raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must be an \
list containing 3 ints between 0 and 255 or a list of lists with rgb values")
    if type(rgb_values[0]) is list:
        for rgb_value in rgb_values:
            if not type(rgb_value) is list:
                raise TypeError("WS2801_RPI.set_pixels attribute rgb_values \
must be an list containing 3 ints for rgb or alist of lists with rgb values")
            if not len(rgb_value) == 3:
                raise TypeError("WS2801_RPI.set_pixels attribute rgb_values \
must be an list containing 3 ints for rgb or a list of lists with rgb values")
            for i in rgb_value:
                if (not type(i) is int) or i < 0 or i > 255:
                    raise TypeError("WS2801_RPI.set_pixels attribute rgb_values \
must be an list containing 3 ints for rgb or a list of lists with rgb values")
    else:
        if not len(rgb_values) == 3:
            raise TypeError("WS2801_RPI.set_pixels attribute rgb_values must \
be an list containing 3 ints for rgb or a list of lists with rgb values")
        for i in rgb_values:
            if (not type(i) is int) or i < 0 or i > 255:
                raise TypeError("WS2801_RPI.set_pixels attribute rgb_values \
must be an list containing 3 ints for rgb or a list of lists with rgb values")

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
        raise RuntimeError("Something weird happend: Buffer overflow")
    if len(pixels) > len(rgb_values):
        logging.warn("WS2801_RPI.py set_leds: more leds addressed than rgb \
values given: assume last rgb for remaining leds")
    if len(pixels) < len(rgb_values):
        logging.warn("WS2801_RPI.py set_leds: too many rgb values supplied: \
skipping")


def set_max_speed_hz(hz):
    """
    Set the communication speed for SPI.

    Default: 976000HZ. There is no need to call this function if default is ok.
    Consult devspi docu https://github.com/doceme/py-spidev.
    """
    try:
        spi.max_speed_hz = hz
    except:
        import traceback
        traceback.print_exc()
        raise


# from here onwards: only invoke these if you have trouble or you want to
# connect to a different LED strip and/or you are working on a PI different
# from model 3
def set_mode(mode):
    """
    Use only in case of problems with your device.

    Check docu of spidev:
    "mode - SPI mode as two bit pattern of clock polarity and phase [CPOL|CPHA], min: 0b00 = 0, max: 0b11 = 3"
    """
    try:
        spi.mode = mode
    except:
        import traceback
        traceback.print_exc()
        raise


def set_threewire(bool):
    """
    Use only in case of panic.

    Consult devspi docu https://github.com/doceme/py-spidev.
    """
    try:
        spi.threewire = bool
    except:
        import traceback
        traceback.print_exc()
        raise


def set_lbsfirst(bool):
    """
    Use only in case of panic.

    Consult devspi docu https://github.com/doceme/py-spidev.
    """
    try:
        spi.threewire = bool
    except:
        import traceback
        traceback.print_exc()
        raise
    try:
        spi.lsbfirst = bool
    except:
        import traceback
        traceback.print_exc()
        raise
