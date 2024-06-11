from machine import UART
from machine import Pin


class SteppingMotor:
    """步进电机"""
    def __init__(self, stp, en, _dir) -> None:
        """步进电机初始化
        * stp: 步进电机的步进脚
        * en: 步进电机的使能脚
        * dir: 步进电机的方向脚
        """
        self.stp = Pin(stp, Pin.OUT)
        self.en = Pin(en, Pin.OUT)
        self.dir = Pin(_dir, Pin.OUT)
        self.en.value(1)
        pass

    def rotate(self, sign, _stop=0):
        """步进电机转动
        * sign: 旋转信号
        * direction: 转动方向
        * _stop: 步进间隔
        """
        d = {"1": (0.25, 1), "2": (0.5, 1), "3":(0.25, 0)}
        circle, direction = d[sign]
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


uart = UART(1, baudrate=9600, tx=8, rx=7)

def restore():
    """还原"""
    if p5.value() == 1:
        led.value(0)        # 就绪指示灯熄灭
        for _sign in str_data_lst:
            sign1 = _sign[0]        # L or R
            sign2 = _sign[1]        # ["1", "2", "3", "O", "C"]
            if sign1 == "L":
                motor = left_motor
                cylinder = left_cylinder
                
            elif sign1 == "R":
                motor = right_motor
                cylinder = right_cylinder

            else:
                raise ValueError("Invalid sign")

            if sign2 == "O":
                cylinder.open()
            elif sign2 == "C":
                cylinder.close()
            elif sign2 in ["1", "2", "3"]:
                motor.rotate(sign2)
            else:
                raise ValueError("Invalid sign")


if __name__ == "__main__":
    # region 创建对象
    left_motor = SteppingMotor(47, 48, 38)
    right_motor = SteppingMotor(40, 39, 21)

    left_cylinder = ClampCylinder(17)
    right_cylinder = ClampCylinder(16)

    led = Pin(9, Pin.OUT)
    # endregion 

    # region 设置中断
    p6 = Pin(6, Pin.OUT, value=0) # 初始化GPIO6
    p5 = Pin(5, Pin.IN, Pin.PULL_DOWN) # 初始化GPIO5,设置拉低电阻
    p5.irq(restore, Pin.IRQ_RISING) # GPIO38设置上升沿触发中断
    # endregion

    # region 接收信号
    PACKET_HEAD = b'@'
    PACKET_TAIL = b'#'

    data = b''  # 用于存储接收到的数据

    while True:
        byte = uart.read(2)
        if byte == b'' or byte is None:
            continue
        if byte == PACKET_HEAD:
            data = b''
        data += byte
        if byte == PACKET_TAIL:
            led.value(1)        # 就绪指示灯亮起
            break
    str_data = data[1:-1].decode()
    str_data_lst = str_data.split(' ')
    # endregion

    while True:
        p6.on()
