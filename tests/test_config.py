import unittest

from rfdevices import BasebandValue, Protocol, PulseOrder, config, const


class TestConfig(unittest.TestCase):
    def setUp(self):
        config.protocols = {}
        config.codes = {}
        self.assertDictEqual(config.protocols, {})
        self.assertDictEqual(config.codes, {})

    @classmethod
    def tearDownClass(cls):
        config.protocols = {}
        config.codes = {}

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

        self.assertDictEqual(protocol.codes, config.codes['uc7070t'])
        self.assertDictEqual(protocol.codes,
                             {
                                 const.CODE_TOGGLE_SWITCH: '1{pin}0000001',
                                 const.CODE_FAN_OFF: '1{pin}0000010',
                                 const.CODE_FAN_LOW: '1{pin}0001000',
                                 const.CODE_FAN_MEDIUM: '1{pin}0010000',
                                 const.CODE_FAN_HIGH: '1{pin}0100000'
                             })

    def test_get_protocol_shared_codes(self):
        protocol = config.get_protocol('rcswitch-1')
        self.assertNotIn('rcswitch-1', config.codes)
        self.assertDictEqual(protocol.codes, config.codes['rcswitch'])
        self.assertDictEqual(protocol.codes,
                             {
                                 const.CODE_TURN_ON_SWITCH: '{group}{device}10',
                                 const.CODE_TURN_OFF_SWITCH: '{group}{device}01'
                             })
