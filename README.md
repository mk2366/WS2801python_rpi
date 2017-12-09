# WS2801python_rpi
A python module connecting RPI with WS2801

It is based on the spidev module you can find [here](https://github.com/doceme/py-spidev).

You can use it like this:

``
import WS2801_RPI as w
w.set_number_of_leds(100)   #adjust to the number of leds in your project
w.set_leds(1)               #to let led number 1 shine in white
w.flush()                   #to communicate your settings to the led strip via spi


You can call set_leds as often as you like before flushing it out. And of course you can flush as often
as you need to create effects.
