# WS2801python_rpi
## A python module connecting RPI with WS2801

__This is version 1.0.0 (Interface will stay stable now)

It is based on the spidev module you can find [here](https://github.com/doceme/py-spidev).

You can use it like this:

```python
import WS2801_RPI as w
s=w.set_led_colors_buffer_list_multi_call

w.set_number_of_leds(100)                      # adjust to the number of leds in your project
w.hello()
w.s(1)                                         # to let led number 1 shine in white
w.flush()                                      # to communicate your settings to the led strip via spi
```

You can call set_leds as often as you like before flushing it out. And of course you can flush as often
as you need to create effects.

## Other convenience functions are:

* `set_number_of_leds(leds=128)`: Call this to set the number of LEDs on your strip for WS2801_RPI.
* `hello()`: I had many issues before I started to do a flush() with all LEDs white. This is a convenience function to let all LEDs shine 3 times for one second.
If you call it and nothing happens: There must be an issue either in program (Check `set_number_of_leds` and `set_spidev_bus_device`) or in your wiring
* `clear()`: turn off all leds. Remember you need to call `flush()` to see the effect.
* `get_led_colors_buffer_dict()`: Get all rgb values currently in the buffer as dictionary. This might differ from what you see on your LED strip.
* `set_led_colors_buffer_dict_multi_call()`: After you adjusted the dict of the function above: Write it back to the buffer. Don't forget `flush()`.
* `get_led_colors_buffer_list()`: Get back two lists. First is a list with integers for all of your LEDs (boring but needed for the set function) and a list of lists each with the three
values for rgb
* `set_led_colors_buffer_list_multi_call(pixels, rgb_values=[255, 255, 255])`: Set the colors for a list of LEDs (pixels). If you give less lists for RGB values than numbers for LEDs the last RGB value is assumed for the remaining LEDs. If you give only a list for rgb_values (like in the default) all LEDs in pixels are set to these values. If pixel is an int you are adressing one LED with this int. I know that this kind of multi is not for production but with this setup my daughter was happy and could play arround before doing all the python list topics.
* `set_max_speed_hz(hz)`: Default is 1MHz. You may change this but not below 1,5KHz.
* `flush()`: Send the data out to the LED strip via SPI
* `set_gamma()`: Set the gamma value. Formula is: `int(((rgb/255)**gamma)*255)`. Default is 2.1 which reduces the number of rgb values to approx. 187.
Set it to `1` you will have 255 values per color but you won't be able to see them. Your eye will turn many into white.
* `set_spidev_bus_device(bus=0, device=0)`: Change the default bus and device for WS2801_RPI
* `get_number_of_leds()`: You should know anyhow. But if you want to check how many LEDs WS2801_RPI is assuming call this function.

## Installation
`pip install WS2801_RPI`.

## Hint
You can raise the log level if you like to suppress warnings:
```python
import logging
logging.getLogger().setLevel(31)
```

## Testing
You can call `python setup.py test` to run the tests (if you clone the git repo onto your machine). I will update as soon as I have more understanding on the test infrastructure.

## Acknowledgement

* [Atom](https://atom.io/) was my editor of choice
* Formatting was done with [linter-pylama](https://atom.io/packages/linter-pylama)

## General remarks on WS2801:
* In the Data [Sheet](https://cdn-shop.adafruit.com/datasheets/WS2801.pdf) of WS2801 I found the following passage I didn't fully understand: `When the WS2801 receives total 24
clock rising edges, the WS2801 enters relay mode ...`. In addition one can read [this](https://electronics.stackexchange.com/a/307117) explanation. I found it helpful.
* WS2801 is using the raising flag of the clock to retrieve the data and expects clock being low for 500 microseconds between data transmissions. Hence there is no need to change
the mode of spidev.

## Would be glad if this code was used often in your projects. Feedback and pull requests are more than welcome.
