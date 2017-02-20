import unittest

from mock_import import mock_import

with mock_import():
    from rfdevices import BasebandValue, Protocol, PulseOrder, config


class TestConfig(unittest.TestCase):
    def setUp(self):
        config.protocols = {}
        self.assertDictEqual(config.protocols, {})

    @classmethod
    def tearDownClass(cls):
        config.protocols = {}

    def test_load_config(self):
        config.load_config()

        self.assertNotEqual(len(config.protocols), 0, 'No protocols loaded')
        self.assertIn('uc7070t', config.protocols, 'Missing UC7070T config')

    def test_get_protocol_invalid(self):
        protocol = config.get_protocol('foobar')
        self.assertIsNone(protocol, 'Configuration returned for invalid protocol')

    def test_get_protocol(self):
        protocol = config.get_protocol('UC7070T')
        self.assertIsNotNone(protocol, 'Missing UC7070T config')
        self.assertIsInstance(protocol, Protocol)

        self.assertEqual(protocol.pulse_length, 311)

        self.assertIsInstance(protocol.pulse_order, PulseOrder)
        self.assertIs(protocol.pulse_order, PulseOrder.LowHigh)

        self.assertIsInstance(protocol.sync, BasebandValue)
        self.assertEqual(protocol.sync.low, 37)
        self.assertEqual(protocol.sync.high, 1)

        self.assertIsInstance(protocol.zero, BasebandValue)
        self.assertEqual(protocol.zero.low, 2)
        self.assertEqual(protocol.zero.high, 1)

        self.assertIsInstance(protocol.one, BasebandValue)
        self.assertEqual(protocol.one.low, 1)
        self.assertEqual(protocol.one.high, 2)

        self.assertEqual(protocol.message_length, 12)
        self.assertEqual(protocol.repeat, 10)
