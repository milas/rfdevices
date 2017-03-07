import collections
import enum


class PulseOrder(enum.Enum):
    LowHigh = 'LOW_HIGH'
    HighLow = 'HIGH_LOW'


BasebandValue = collections.namedtuple('BasebandValue', ['low', 'high'])


class Protocol(object):
    def __init__(self, pulse_length: int, pulse_order: PulseOrder, sync: BasebandValue, zero: BasebandValue,
                 one: BasebandValue, message_length: int, repeat: int=1, codes: dict=None):
        self.pulse_length = pulse_length
        self.pulse_order = pulse_order
        self.sync = sync
        self.zero = zero
        self.one = one
        self.message_length = message_length
        self.repeat = repeat
        self.codes = codes or {}

    def prepare_code(self, code: int):
        return format(code, '#0{}b'.format(self.message_length + 2))[2:]

    @staticmethod
    def from_template(name: str) -> 'Protocol':
        import rfdevices.config
        return rfdevices.config.get_protocol(name)
