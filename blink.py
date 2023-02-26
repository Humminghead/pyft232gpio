# https: // ftdichip.com/wp-content/uploads/2020/07/DS_FT232H.pdf
# https: // www.ftdichip.com/Support/Documents/AppNotes/AN_108_Command_Processor_for_MPSSE_and_MCU_Host_Bus_Emulation_Modes.pdf

from pyftdi.i2c import I2cController, I2cIOError
from time import sleep


class LedSwitcher():
    _deviceUrl: str
    _switchCnt: int
    _i2c: I2cController
    _ACBUS3: int = 0x1800

    def __init__(self, count: int) -> None:
        self._deviceUrl = 'ftdi:///1'
        self._i2c = I2cController()
        self._switchCnt = count

    def blink(self):
        gpio = self._i2c.get_gpio()
        gpio.set_direction(self._ACBUS3, self._ACBUS3)
        cnt = 0
        gpio.write(self._ACBUS3)
        while cnt < self._switchCnt:
            gpio.write(self._ACBUS3 & 0x800)
            sleep(0.5)
            gpio.write(self._ACBUS3 & 0x1000)
            sleep(0.5)
            cnt += 1

    def open(self):
        self._i2c.configure(self._deviceUrl)

    def close(self):
        self._i2c.close()

    def doBlink(self):
        self.open()
        self.blink()
        self.close()


def run():
    LedSwitcher(100).doBlink()


if __name__ == '__main__':
    run()

