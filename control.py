from machine import Pin


class SteppingMotor:
    """步进电机"""
    def __init__(self, stp, en, dir) -> None:
        """步进电机初始化
        * stp: 步进电机的步进脚
        * en: 步进电机的使能脚
        * dir: 步进电机的方向脚
        """
        self.stp = Pin(stp, Pin.OUT)
        self.en = Pin(en, Pin.OUT)
        self.dir = Pin(dir, Pin.OUT)
        self.en.value(1)
        pass

    def rotate(self, circle, direction=1, _stop=0):
        """步进电机转动
        * circle: 转动圈数
        * direction: 转动方向
        * _stop: 步进间隔
        """
        self.dir.value(direction)
        for i in range(3200 * circle):
            self.stp.value(1)
            for _ in range(_stop):pass
            self.stp.value(0)
            for _ in range(_stop):pass
        pass


class ClampCylinder:
    """气缸夹爪"""
    def __init__(self,_pin) -> None:
        self.pin = Pin(_pin, Pin.OUT)
        pass

    def open(self):
        self.pin.value(1)
        pass

    def close(self):
        self.pin.value(0)
        pass


class Control:
    def __init__(self, _motor:SteppingMotor, _cylinder:ClampCylinder) -> None:
        self.motor = _motor
        self.cylinder = _cylinder
        pass

    def rotate(self, circle, direction=1, _stop=0):
        self.motor.rotate(circle, direction, _stop)
        pass

    def open(self):
        self.cylinder.open()
        pass

    def close(self):
        self.cylinder.close()
        pass
    

if __name__ == "__main__":
    #region 电机测试
    motor = SteppingMotor(13, 12, 14)
    motor.rotate(1, 1, 0)
    #endregion

    # #region 气缸测试
    # cylinder = ClampCylinder(15)
    # cylinder.open()
    # cylinder.close()
    # #endregion