from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
   # package is not installed
   pass

__doc__ = """
WS2801python_rpi: A python program to connect WS2801 driven LED strips.

Copyright (C) 2017  Markus Kupke <kupkemarkus@gmail.com>
Version: /version/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/>.
""".replace("/version/", __version__)
import spidev as __spidev
import logging as __logging
import time
from timeit import default_timer as __timer
import traceback


__logging.warning(__doc__)

__BUS = 0
__DEVICE = 0
__MAX_SPEED_HZ = 976000
__NUMBER_LEDS = 0
__rgb_leds = []
__mode = 0b01
__last_flush = 0
# only for initialization. Is set to reasonable values at end of file
__gamma = [255]*256

# texts to separate into resources once I do a package (if ever)
__string_type_error_1 = "Attribute pixels must be an \
int addressing one of the available LEDs or a list of ints"
__string_type_error_2 = "Attribute rgb_values must be an \
list containing 3 ints between 0 and 255 or a list of lists with rgb values"
__string_type_error_3 = "Attribute must be a dictionary"
__string_type_error_4 = "Value must be a dictionary as well"
__string_type_error_6 = "bus and device must be either 0 or 1 each"
__string_value_error_1 = "You are addressing an LED that does not exist"
__string_value_error_2 = "rgb values must be between 0 and 255"
__string_runtime_error_2 = "Something weird happend: Buffer overflow"
__string_runtime_error_3 = "SPI Bus must be driven with clock speed > 1500HZ \
for WS2801"
__string_runtime_error_4 = "Mode must be between 0 and 3."
__string_warning_1 = "more leds addressed than rgb \
values given: assume last rgb for remaining leds"
__string_warning_3 = "Your dict contains floats as keys. \
These are not taken into account when adressing LEDs."
__string_warning_2 = "too many rgb values supplied: \
skipping"

# initialize SPI
# this should meet the requirements of WS2801
try:
    __spi = __spidev.SpiDev()
except:
    traceback.print_exc()
    raise


def set_spidev_bus_device(bus=0, device=0):
    """
    RASPBERRY PI Model 3 is normally connected via /dev/spidev0.0.

    If your model connects differently: adapt with this function.
    """
    if (not type(bus) is int or
            not type(device) is int or
            bus < 0 or
            bus > 1 or
            device < 0 or
            device > 1):
        raise TypeError(__string_type_error_6)
    global __BUS
    __BUS = bus
    global __DEVICE
    __DEVICE = device


def set_number_of_leds(leds=128):
    """
    Define the number of leds on your strip.

    This function has to be called if different number than 128!
    """
    global __NUMBER_LEDS
    __NUMBER_LEDS = leds
    global __rgb_leds
    __rgb_leds = [0] * __NUMBER_LEDS * 3


def get_number_of_leds():
    """Retrieve the number of LEDs set in the module."""
    return __NUMBER_LEDS


def hello():
    """Call one time to check LEDs."""
    for j in range(3):
        set_led_colors_buffer_list_multi_call(
                [i+1 for i in range(__NUMBER_LEDS)],
                [[255, 255, 255]] * __NUMBER_LEDS)
        flush()
        time.sleep(1)
        clear()
        flush()
        time.sleep(1)


def flush():
    """Send the bits to the leds. No parameters."""
    # WS2801 needs 500 micro seconds between flushes
    global __last_flush
    while (__timer() - __last_flush) <= 0.0005:
        pass
    try:
        __spi.open(bus=__BUS, device=__DEVICE)
        __spi.mode = __mode
        __spi.max_speed_hz = __MAX_SPEED_HZ
        __spi.writebytes(list(map(lambda rgb: __gamma[rgb], __rgb_leds)))
        __spi.close()
    except:
        traceback.print_exc()
        raise
    __last_flush = __timer()


def clear():
    """Switch all leds off. Needs a flush() to be active."""
    global __rgb_leds
    __rgb_leds[:] = [0 for i in range(__NUMBER_LEDS*3)]


def get_led_colors_buffer_dict():
    """
    Get the buffer for leds colors as dict.

    The leds are indexed with ints starting with 1 and values are dicts with
    rgb indexed with "red","green" and "blue"
    """
    global __NUMBER_LEDS
    leds_dict = {}
    rgb_dict = {"red": 0, "green": 0, "blue": 0}
    for index in range(0, __NUMBER_LEDS * 3, 3):
        rgb_dict = {"red": __rgb_leds[index],
                    "green": __rgb_leds[index+1],
                    "blue": __rgb_leds[index+2]}
        leds_dict[int((index+3)/3)] = rgb_dict
    return leds_dict


def set_led_colors_buffer_dict_multi_call(leds_dict):
    """
    Set the buffer for the leds via a dictionary.

    Key of dictionary is an int adressing the number of the led,
    all other keys are ignored.
    Value is a dictionary with the keys "red", "green" and "blue".
    Other values are ignored. If a color key is not found it defaults to 0.
    Values in the second dictinary can be ints between 0 and 255
    """
    if not type(leds_dict) is dict:
        raise TypeError(__string_type_error_3)
    for led, rgb_dict in leds_dict.items():
        rgb_list = [0, 0, 0]
        if type(led) is float:
            __logging.warning(__string_warning_3)
        if type(led) is int:
            if led < 1 or led > __NUMBER_LEDS:
                raise ValueError(__string_value_error_1)
            if not type(rgb_dict) is dict:
                raise TypeError(__string_type_error_4)
            for color, rgb_value in rgb_dict.items():
                if color == "red":
                    if (not type(rgb_value) is int or
                            rgb_value < 0 or
                            rgb_value > 255):
                        raise ValueError(__string_value_error_2)
                    rgb_list[0] = rgb_value
                if color == "green":
                    if (not type(rgb_value) is int or
                            rgb_value < 0 or
                            rgb_value > 255):
                        raise ValueError(__string_value_error_2)
                    rgb_list[1] = rgb_value
                if color == "blue":
                    if (not type(rgb_value) is int or
                            rgb_value < 0 or
                            rgb_value > 255):
                        raise ValueError(__string_value_error_2)
                    rgb_list[2] = rgb_value
            set_led_colors_buffer_list_multi_call(led, rgb_list)


def get_led_colors_buffer_list():
    """Get the list of rgb values for all LEDs."""
    return [[__rgb_leds[i], __rgb_leds[i+1],
             __rgb_leds[i+2]] for i in range(0, 3 * __NUMBER_LEDS, 3)]


def set_led_colors_buffer_list_multi_call(pixels, rgb_values=[255, 255, 255]):
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
            raise TypeError(__string_type_error_1)
        for val in pixels:
            if (not type(val) is int):
                raise TypeError(__string_type_error_1)
            if val < 1 or val > __NUMBER_LEDS:
                raise ValueError(__string_value_error_1)
    else:
        if pixels > __NUMBER_LEDS or pixels < 1:
            raise ValueError(__string_value_error_1)
    if not type(rgb_values) is list:
        raise TypeError(__string_type_error_2)
    if type(rgb_values[0]) is list:
        for rgb_value in rgb_values:
            if not type(rgb_value) is list:
                raise TypeError(__string_type_error_2)
            if not len(rgb_value) == 3:
                raise TypeError(__string_type_error_2)
            for i in rgb_value:
                if (not type(i) is int):
                    raise TypeError(__string_type_error_2)
                if i < 0 or i > 255:
                    raise ValueError(__string_value_error_2)
    else:
        if not len(rgb_values) == 3:
            raise TypeError(__string_type_error_2)
        for i in rgb_values:
            if (not type(i) is int):
                raise TypeError(__string_type_error_2)
            if i < 0 or i > 255:
                raise ValueError(__string_value_error_2)

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
    if len(__rgb_leds) != __NUMBER_LEDS*3:
        raise RuntimeError(__string_runtime_error_2)
    if len(pixels) > len(rgb_values):
        __logging.warning(__string_warning_1)
    if len(pixels) < len(rgb_values):
        __logging.warning(__string_warning_2)


def set_max_speed_hz(hz):
    """
    Set the communication speed for SPI.

    Default: 976000HZ. There is no need to call this function if default is ok.
    Consult devspi docu https://github.com/doceme/py-spidev.
    """
    if hz <= 1500:
        # 500 micro sec clock low is the time WS2801 needs to reset. hence
        # it must be driven with a clock higher than 1000hz otherwise it will
        # reset all the time :-)
        raise ValueError(__string_runtime_error_3)
    global __MAX_SPEED_HZ
    __MAX_SPEED_HZ = hz


def set_gamma(gamma=2.1):
    """Set the gamma correction."""
    for i in range(256):
        __gamma[i] = int(((i/255.0)**gamma) * 255.0)


# initialize the module with 128 leds
set_gamma()
set_number_of_leds()
