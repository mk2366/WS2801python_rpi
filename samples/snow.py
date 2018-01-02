import WS2801_RPI as led
from random import randint

led.clear()
led.flush()
while True:
    n = randint(1, 128)
    h = randint(0, 255)
    led.set_led_colors_buffer_list_multi_call(n, [h, h, h])
    led.flush()
