"""This is an example on how to use WS2801_RPI."""

import WS2801_RPI as Leds
import time
import logging
import colorsys

granularity = 180.0


logging.getLogger().setLevel(31)
velocity = 300
Leds.set_gamma(3)
s = Leds.set_led_colors_buffer_list_multi_call

i = 0
while True:
    i = (i + 1) % int(granularity)
    rgb = Leds.get_led_colors_buffer_list()
    red, green, blue = colorsys.hsv_to_rgb(i/granularity, 1, 1)
    rgb.insert(0, [int(red * 255), int(green * 255), int(blue * 255)])
    rgb.pop()
    s([(j+1) for j in range(128)], rgb)
    Leds.flush()
    time.sleep(1.0/velocity)
