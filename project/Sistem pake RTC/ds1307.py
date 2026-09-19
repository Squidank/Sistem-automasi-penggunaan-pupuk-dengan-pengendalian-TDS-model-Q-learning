from machine import I2C

class DS1307:
    DS1307_I2C_ADDRESS = 104

    def __init__(self, i2c):
        self.i2c = i2c

    def _dec2bcd(self, value):
        return (value // 10) * 16 + (value % 10)

    def _bcd2dec(self, value):
        return (value // 16) * 10 + (value % 16)

    def datetime(self, dt=None):
        if dt is None:
            # Read time
            data = self.i2c.readfrom_mem(self.DS1307_I2C_ADDRESS, 0, 7)
            second = self._bcd2dec(data[0])
            minute = self._bcd2dec(data[1])
            hour = self._bcd2dec(data[2])
            weekday = self._bcd2dec(data[3])
            day = self._bcd2dec(data[4])
            month = self._bcd2dec(data[5])
            year = self._bcd2dec(data[6]) + 2000
            return (year, month, day, weekday, hour, minute, second, 0)
        else:
            # Write time
            year, month, day, weekday, hour, minute, second, _ = dt
            data = bytearray(7)
            data[0] = self._dec2bcd(second)
            data[1] = self._dec2bcd(minute)
            data[2] = self._dec2bcd(hour)
            data[3] = self._dec2bcd(weekday)
            data[4] = self._dec2bcd(day)
            data[5] = self._dec2bcd(month)
            data[6] = self._dec2bcd(year - 2000)
            self.i2c.writeto_mem(self.DS1307_I2C_ADDRESS, 0, data)