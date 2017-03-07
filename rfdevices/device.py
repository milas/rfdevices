from .protocol import Protocol
from .transmitter import Transmitter


class RFDevice(object):
    def __init__(self, transmitter: Transmitter, protocol: Protocol, codes: dict=None, params: dict=None):
        self.tx = transmitter
        self.protocol = protocol
        self.codes = codes or self.protocol.codes
        self.params = params or {}

        self._validate()

    def format_code(self, action: str) -> str:
        return self.codes[action].format(**self.params)

    def send(self, action: str) -> bool:
        code = self.format_code(action)
        return self.tx.tx_bin(code, self.protocol)

    def _validate(self):
        for code, value in self.codes.items():
            formatted = self.format_code(code)
            if len(formatted) != self.protocol.message_length:
                raise ValueError('Code %s with value=%s has incorrect length (%d), length must be exactly %d ('
                                 'params=%d)',
                                 code, formatted, len(formatted), self.protocol.message_length, self.params)
