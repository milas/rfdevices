import unittest

from unittest import mock

from Adafruit_GPIO import GPIO

from rfdevices import const, RFDevice, BasebandValue, Protocol, PulseOrder, Transmitter


test_protocol = Protocol(pulse_length=1,
                         pulse_order=PulseOrder.LowHigh,
                         sync=BasebandValue(low=1, high=2),
                         zero=BasebandValue(low=3, high=4),
                         one=BasebandValue(low=5, high=6),
                         message_length=11,
                         repeat=1,
                         codes={
                             const.CODE_TOGGLE_SWITCH: '1{pin}1{other}1'
                         })


class TestDevice(unittest.TestCase):
    def setUp(self):
        platform = mock.MagicMock(spec=GPIO.BaseGPIO)
        self.tx = Transmitter(gpio=16, platform=platform)

    def test_device_invalid_param(self):
        codes = {
            const.CODE_TOGGLE_SWITCH: '0{param}'
        }

        with self.assertRaises(ValueError):
            device = RFDevice(transmitter=self.tx, protocol=test_protocol, codes=codes, params={'param': '0'})

    def test_device_explicit_codes(self):
        codes = {
            const.CODE_TOGGLE_SWITCH: '0' * 10 + '{param}'
        }

        device = RFDevice(transmitter=self.tx, protocol=test_protocol, codes=codes, params={'param': '1'})
        self.assertEqual(device.format_code(const.CODE_TOGGLE_SWITCH), '00000000001')

    def test_device_codes_from_protocol(self):
        params = {
            'pin': '0100',
            'other': '0010'
        }
        device = RFDevice(transmitter=self.tx, protocol=test_protocol, codes=None, params=params)
        self.assertDictEqual(device.codes, test_protocol.codes)
        self.assertEqual(device.format_code(const.CODE_TOGGLE_SWITCH), '10100100101')

    def test_device_missing_param(self):
        params = {
            'pin': '0010',
            'another': '1111'
        }

        with self.assertRaises(KeyError):
            device = RFDevice(transmitter=self.tx, protocol=test_protocol, codes=None, params=params)

    def test_device_no_params_required(self):
        codes = {
            const.CODE_TOGGLE_SWITCH: '0' * 11
        }

        device = RFDevice(transmitter=self.tx, protocol=test_protocol, codes=codes, params=None)
        self.assertEqual(device.format_code(const.CODE_TOGGLE_SWITCH), '00000000000')

    def test_device_perform_action(self):
        params = {
            'pin': '0100',
            'other': '0010'
        }

        tx = mock.MagicMock(spec=Transmitter)
        device = RFDevice(transmitter=tx, protocol=test_protocol, codes=None, params=params)
        self.assertTrue(device.send(const.CODE_TOGGLE_SWITCH))
        tx.tx_bin.assert_called_once_with('10100100101', test_protocol)
