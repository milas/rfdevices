import unittest

from unittest import mock

from Adafruit_GPIO import GPIO

from rfdevices import BasebandValue, Protocol, PulseOrder, RFDevice


test_protocol = Protocol(pulse_length=1,
                         pulse_order=PulseOrder.LowHigh,
                         sync=BasebandValue(low=1, high=2),
                         zero=BasebandValue(low=3, high=4),
                         one=BasebandValue(low=5, high=6),
                         message_length=16,
                         repeat=1)


class TestDevice(unittest.TestCase):
    @mock.patch('rfdevices.device.GPIO.get_platform_gpio', return_value=mock.MagicMock(spec=GPIO.BaseGPIO))
    def test_auto_gpio(self, platform_mock):
        device = RFDevice(pin=16)

        self.assertEqual(device.pin, 16)
        self.assertIsInstance(device.gpio, GPIO.BaseGPIO)
        self.assertIsInstance(device.gpio, mock.MagicMock)

    def test_ctx_manager(self):
        gpio = mock.MagicMock(spec=GPIO.BaseGPIO)
        device = RFDevice(pin=8, gpio=gpio)

        self.assertFalse(gpio.setup.called)
        self.assertFalse(gpio.cleanup.called)
        self.assertFalse(device.tx_enabled)

        with device:
            self.assertEqual(gpio.setup.call_count, 1)
            self.assertFalse(gpio.cleanup.called)
            self.assertTrue(device.tx_enabled)

        self.assertEqual(gpio.setup.call_count, 1)
        self.assertEqual(gpio.cleanup.call_count, 1)
