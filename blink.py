from pyftdi.i2c import I2cController, I2cIOError
from time import sleep


class LedSwitcher():
    _deviceUrl: str
    _switchCnt: int
    _i2c: I2cController

    def __init__(self, count: int) -> None:
        self._deviceUrl = 'ftdi:///1'
        self._i2c = I2cController()
        self._switchCnt = count

    def blink(self):
        gpio = self._i2c.get_gpio()
        gpio.set_direction(0x1800, 0x1800)
        cnt = 0
        gpio.write(0x1800)
        while cnt < self._switchCnt:
            gpio.write(0x800)
            sleep(0.5)
            gpio.write(0x1000)
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
