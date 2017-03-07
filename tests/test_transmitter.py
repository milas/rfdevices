import unittest

from unittest import mock

from Adafruit_GPIO import GPIO

from rfdevices import BasebandValue, Protocol, PulseOrder, Transmitter


test_protocol = Protocol(pulse_length=1,
                         pulse_order=PulseOrder.LowHigh,
                         sync=BasebandValue(low=1, high=2),
                         zero=BasebandValue(low=3, high=4),
                         one=BasebandValue(low=5, high=6),
                         message_length=16,
                         repeat=1)


class TestTransmitter(unittest.TestCase):
    @mock.patch('rfdevices.transmitter.GPIO.get_platform_gpio', return_value=mock.MagicMock(spec=GPIO.BaseGPIO))
    def test_auto_gpio(self, platform_mock):
        tx = Transmitter(gpio=16)

        self.assertEqual(tx.gpio, 16)
        self.assertIsInstance(tx.platform, GPIO.BaseGPIO)
        self.assertIsInstance(tx.platform, mock.MagicMock)

    def test_ctx_manager(self):
        platform = mock.MagicMock(spec=GPIO.BaseGPIO)
        tx = Transmitter(gpio=8, platform=platform)

        self.assertFalse(platform.setup.called)
        self.assertFalse(platform.cleanup.called)
        self.assertFalse(tx.tx_enabled)

        with tx:
            self.assertEqual(platform.setup.call_count, 1)
            self.assertFalse(platform.cleanup.called)
            self.assertTrue(tx.tx_enabled)

        self.assertEqual(platform.setup.call_count, 1)
        self.assertEqual(platform.cleanup.call_count, 1)
