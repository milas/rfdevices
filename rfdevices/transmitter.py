"""
Sending RF signals with low-cost GPIO RF Modules on a Raspberry Pi.
"""

import logging
import threading
import time

from Adafruit_GPIO import GPIO

from rfdevices.protocol import BasebandValue, Protocol, PulseOrder

log = logging.getLogger(__name__)


class Transmitter:
    """Representation of a GPIO RF chip."""

    def __init__(self, gpio: int, platform: GPIO.BaseGPIO=None, **kwargs):
        """Initialize the RF device."""
        self.gpio = gpio
        self.platform = platform or GPIO.get_platform_gpio(**kwargs)

        self.tx_enabled = False
        self.lock = threading.Lock()

        log.debug("Using GPIO " + str(gpio))

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        """Disable TX and clean up GPIO."""
        with self.lock:
            if self.tx_enabled:
                self.platform.cleanup(pin=self.gpio)
                self.tx_enabled = False
                log.debug("Cleanup")

    def setup(self):
        """Enable TX, set up GPIO."""
        with self.lock:
            if not self.tx_enabled:
                self.platform.setup(pin=self.gpio, mode=GPIO.OUT)
                self.tx_enabled = True
                log.debug("TX enabled")
            return True

    def tx_code(self, code: int, tx_proto: Protocol):
        """
        Send a decimal code.
        """
        bin_code = tx_proto.prepare_code(code)
        with self.lock:
            log.debug("TX code: " + str(code))
            return self._tx_bin_locked(bin_code, tx_proto)

    def tx_bin(self, value: str, tx_proto: Protocol) -> bool:
        """Send a binary code."""
        with self.lock:
            return self._tx_bin_locked(value, tx_proto)

    def _tx_bin_locked(self, value: str, tx_proto: Protocol) -> bool:
        if len(value) != tx_proto.message_length:
            raise ValueError('Invalid value length, must be exactly {}'.format(tx_proto.message_length))

        log.debug("TX bin: " + str(value))
        for _ in range(0, tx_proto.repeat):
            for byte in range(0, tx_proto.message_length):
                if value[byte] == '0':
                    if not self._tx_zero_bit(tx_proto):
                        return False
                else:
                    if not self._tx_one_bit(tx_proto):
                        return False
            if not self._tx_sync(tx_proto):
                return False

        return True

    def _tx_zero_bit(self, tx_proto: Protocol):
        """Send a '0' bit."""
        return self._tx_waveform(tx_proto.pulse_length, tx_proto.pulse_order, tx_proto.zero)

    def _tx_one_bit(self, tx_proto: Protocol):
        """Send a '1' bit."""
        return self._tx_waveform(tx_proto.pulse_length, tx_proto.pulse_order, tx_proto.one)

    def _tx_sync(self, tx_proto: Protocol):
        """Send a sync."""
        return self._tx_waveform(tx_proto.pulse_length, tx_proto.pulse_order, tx_proto.sync)

    def _tx_waveform(self, pulse_length: int, pulse_order: PulseOrder, value: BasebandValue):
        """Send basic waveform."""
        if not self.tx_enabled:
            log.error("TX is not enabled, not sending data")
            return False

        def low():
            self.platform.output(pin=self.gpio, value=GPIO.LOW)
            time.sleep((value.low * pulse_length) / 1000000)

        def high():
            self.platform.output(pin=self.gpio, value=GPIO.HIGH)
            time.sleep((value.high * pulse_length) / 1000000)

        if pulse_order is PulseOrder.LowHigh:
            low()
            high()
            self.platform.output(pin=self.gpio, value=GPIO.LOW)
        elif pulse_order is PulseOrder.HighLow:
            high()
            low()

        return True
