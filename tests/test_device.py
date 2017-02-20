import unittest

from unittest import mock

from mock_import import mock_import

with mock_import():
    from rfdevices import BasebandValue, Protocol, PulseOrder, RFDevice

test_protocol = Protocol(pulse_length=1,
                         pulse_order=PulseOrder.LowHigh,
                         sync=BasebandValue(low=1, high=2),
                         zero=BasebandValue(low=3, high=4),
                         one=BasebandValue(low=5, high=6),
                         message_length=16,
                         repeat=1)


class TestDevice(unittest.TestCase):
    @mock.patch.object(RFDevice, 'cleanup')
    def test_ctx_manager(self, cleanup_mock):
        device = RFDevice(gpio=mock.MagicMock())
        self.assertFalse(device.tx_enabled)

        with device:
            self.assertTrue(device.tx_enabled)

        self.assertEqual(cleanup_mock.call_count, 1)
