"""Test module for Unit Tests of WS2801_RPI."""

import unittest
import sys
import WS2801_RPI
if sys.version_info >= (3,):
    from unittest.mock import patch
else:
    from mock import patch


@patch("WS2801_RPI.__spi")
class DataSetGetTestCase(unittest.TestCase):
    """Test the set/get methods in module WS2801_RPI."""

    def test_set_max_speed_hz(self, mock_spi):
        """Check whether one can set the speed"""
        WS2801_RPI.set_number_of_leds(5)
        with self.assertRaises(ValueError):
            WS2801_RPI.set_max_speed_hz(1000)
        WS2801_RPI.set_number_of_leds(5)
        WS2801_RPI.set_max_speed_hz(2000000)
        WS2801_RPI.flush()
        self.assertEqual(mock_spi.max_speed_hz, 2000000)

    def test_set_led_colors_buffer_list_multi_call(self, mock_spi):
        """Test set_led_colors_buffer_list_multi_call."""
        WS2801_RPI.set_number_of_leds()
        WS2801_RPI.set_led_colors_buffer_list_multi_call(1)
        WS2801_RPI.flush()
        WS2801_RPI.set_gamma(1)
        expected_result = ([255, 255, 255] + [0, 0, 0] *
                           (WS2801_RPI.get_number_of_leds() - 1))
        mock_spi.writebytes.assert_called_with(expected_result)
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call("1")
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call(1, 3)
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call(["String"])
        with self.assertRaises(ValueError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([700])
        with self.assertRaises(ValueError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call(700)
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [[255, 255, 255],
                                                             3])
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [[255, 255, 255],
                                                             [3]])
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [[255, 255, 255],
                                                             [3, 4, 6.7]])
        with self.assertRaises(ValueError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [[255, 255, 255],
                                                             [3, 4, 6700]])
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [255, 255]
                                                             )
        with self.assertRaises(TypeError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [255, 255, "String"]
                                                             )
        with self.assertRaises(ValueError):
            WS2801_RPI.set_number_of_leds()
            WS2801_RPI.set_led_colors_buffer_list_multi_call([1, 3, 5],
                                                             [255, 255, -3]
                                                             )

    @patch("WS2801_RPI.__logging")
    def test_set_get_led_colors_buffer_dict(self, mock_logger, mock_spi):
        WS2801_RPI.set_gamma(1)
        WS2801_RPI.set_number_of_leds(1)
        d = WS2801_RPI.get_led_colors_buffer_dict()
        self.assertEqual(d, {1: {"red": 0, "green": 0, "blue": 0}})
        d[1]["red"] = 27
        WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        WS2801_RPI.flush()
        mock_spi.writebytes.assert_called_with([27, 0, 0])
        with self.assertRaises(TypeError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call([1, "red"])
        d[-1] = {"green": 255}
        with self.assertRaises(ValueError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        del(d[-1])
        WS2801_RPI.set_number_of_leds(2)
        d[2] = "No dictionary"
        with self.assertRaises(TypeError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        d[2] = {"red": 256}
        with self.assertRaises(ValueError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        d[2] = {"green": 256}
        with self.assertRaises(ValueError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        d[2] = {"blue": 256}
        with self.assertRaises(ValueError):
            WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        del(d[2])
        d[4.0] = {"float": 3.14}
        WS2801_RPI.set_led_colors_buffer_dict_multi_call(d)
        self.assertTrue(mock_logger.warning.called)

    def test_set_spidev_bus_device(self, mock_spi):
        with self.assertRaises(TypeError):
            WS2801_RPI.set_spidev_bus_device("String", 0)
        WS2801_RPI.set_spidev_bus_device(0, 1)
        WS2801_RPI.flush()
        mock_spi.open.assert_called_with(bus=0, device=1)

    @patch("WS2801_RPI.time")
    def test_hello(self, mock_time, mock_spi):
        WS2801_RPI.hello()
        self.assertEqual(mock_spi.open.call_count, 6)
        self.assertEqual(mock_spi.writebytes.call_count, 6)

    @patch("WS2801_RPI.traceback")
    def test_flush(self, mock_traceback, mock_spi):
        mock_spi.open.side_effect = Exception("mock_spi raised an Excption")
        with self.assertRaises(Exception):
            WS2801_RPI.flush()

    def test_get_led_colors_buffer_list(self, mock_spi):
        WS2801_RPI.set_number_of_leds(5)
        WS2801_RPI.set_gamma(1)
        li = WS2801_RPI.get_led_colors_buffer_list()
        self.assertEqual(li, [[0, 0, 0]] * 5)


if __name__ == '__main__':
    unittest.main()
