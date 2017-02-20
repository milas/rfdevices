import unittest

from mock_import import mock_import

with mock_import():
    from rfdevices.protocol import BasebandValue, Protocol, PulseOrder


class TestProtocol(unittest.TestCase):
    @staticmethod
    def get_test_protocol(repeat: int=None):
        kwargs = {}
        if repeat is not None:
            kwargs['repeat'] = repeat

        return Protocol(pulse_length=1,
                        pulse_order=PulseOrder.LowHigh,
                        sync=BasebandValue(low=1, high=2),
                        zero=BasebandValue(low=3, high=4),
                        one=BasebandValue(low=5, high=6),
                        message_length=16,
                        **kwargs)

    def test_init_no_repeat_specified(self):
        protocol = self.get_test_protocol()
        self.assertEqual(protocol.pulse_length, 1)
        self.assertIs(protocol.pulse_order, PulseOrder.LowHigh)
        self.assertEqual(protocol.sync.low, 1)
        self.assertEqual(protocol.sync.high, 2)
        self.assertEqual(protocol.zero.low, 3)
        self.assertEqual(protocol.zero.high, 4)
        self.assertEqual(protocol.one.low, 5)
        self.assertEqual(protocol.one.high, 6)
        self.assertEqual(protocol.message_length, 16)
        self.assertEqual(protocol.repeat, 1)

    def test_init_custom_repeat(self):
        protocol = self.get_test_protocol(101)
        self.assertEqual(protocol.repeat, 101)

    def test_prepare_code(self):
        test_protocol = self.get_test_protocol()
        code = 100

        binary = test_protocol.prepare_code(code)

        self.assertEqual(len(binary), test_protocol.message_length)
        self.assertEqual(binary, '0000000001100100')
