# WS2801python_rpi
## A python module connecting RPI with WS2801

__This is version 1.0.0.dev3. It is in development. Code may change without notice.__

It is based on the spidev module you can find [here](https://github.com/doceme/py-spidev).

You can use it like this:

```python
import WS2801_RPI as w
s=w.set_led_colors_buffer_list_multi_call
w.set_number_of_leds(100)                      # adjust to the number of leds in your project
w.s(1)                                         # to let led number 1 shine in white
w.flush()                                      # to communicate your settings to the led strip via spi
```

You can call set_leds as often as you like before flushing it out. And of course you can flush as often
as you need to create effects.

## Other convenience functions are:

* `clear()`: turn off all leds. Remember you need to call `flush()` to see the effect.
* `get_led_colors_buffer_dict()`: Get all rgb values currently in the buffer as dictionary. This might differ from what you see on your LED strip.
* `set_led_colors_buffer_dict_multi_call()`: After you adjusted the dict of the function above: Write it back to the buffer. Don't forget `flush()`.
* `set_max_speed_hz(hz)`: Default is 1MHz. You may change this but not below 1,5KHz.
* `set_gamma()`: Set the gamma value. Formula is: `int(((rgb/255)**gamma)*255)`. Default is 2.1 which reduces the number of rgb values to approx. 187.
Set it to `1` you will have 255 values per color but you won't be able to see them. Your eye will turn many into white.

## Installation
`pip install WS2801_RPI`.

## Hint
You can raise the log level if you like to suppress warnings:
```python
import logging
logging.getLogger().setLevel(31)
```

## General remarks on WS2801:
* In the Data [Sheet](https://cdn-shop.adafruit.com/datasheets/WS2801.pdf) of WS2801 I found the following passage I didn't fully understand: `When the WS2801 receives total 24
clock rising edges, the WS2801 enters relay mode ...`. In addition one can read [this](https://electronics.stackexchange.com/a/307117) explanation. I found it helpful.
* WS2801 is using the raising flag of the clock to retrieve the data and expects clock being low for 500 microseconds between data transmissions. Hence there is no need to chance
the mode of spidev. It must be zero, regardless which effects you see.

## Would be glad if this code was used often in your projects. Feedback and pull requests are more than welcome.
