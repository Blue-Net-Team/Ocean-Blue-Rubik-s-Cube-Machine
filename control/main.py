import time
from machine import UART
from machine import Pin
from machine import I2C
import ssd1306


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

    def rotate(self, sign:str, _stop=25):
        """步进电机转动
        * sign: 旋转信号
        * direction: 转动方向
        * _stop: 步进间隔
        """
        d = {"1": (0.25, 0), "2": (0.5, 0), "3":(0.25, 1)}
        circle, direction = d[sign]
        self.dir.value(direction)

        total_steps = int(3200 * circle)
        accel_steps = total_steps // 4  # 加速阶段步数
        decel_steps = total_steps // 4  # 减速阶段步数
        uniform_steps = total_steps - accel_steps - decel_steps  # 匀速阶段步数

        # 加速阶段
        for i in range(accel_steps):
            _stop = _stop - i // 5  # 假设每100步加速一次
            self.stp.value(1)
            for _ in range(_stop): pass
            self.stp.value(0)
            for _ in range(_stop): pass

        # 匀速阶段
        for i in range(uniform_steps):
            self.stp.value(1)
            for _ in range(_stop): pass
            self.stp.value(0)
            for _ in range(_stop): pass

        # 减速阶段
        for i in range(decel_steps):
            _stop = _stop + i // 50  # 假设每100步减速一次
            self.stp.value(1)
            for _ in range(_stop): pass
            self.stp.value(0)
            for _ in range(_stop): pass


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


uart = UART(1, baudrate=9600, tx=8, rx=7)       # type: ignore

def restore():
    """还原
    ----
    收到信号触发"""
    for _sign in str_data_lst:
        oled.fill(0)
        oled.text(f'{_sign}', 0, 10)
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

        if sign2 in ["O", "C"]:
            if sign2 == 'O':
                cylinder.open()
            if sign2 == "C":
                cylinder.close()
            time.sleep(0.1)        # 0.15可用 5个压    0.1 6个压测试
        elif sign2 in ['1','2','3']:
            if sign2 in ["1", "3"]:
                motor.rotate(sign2, 0)     # 5
            elif sign2 == "2":
                motor.rotate(sign2, 0)      # 5
            time.sleep(0.3)
        else:
            raise ValueError("Invalid sign")
        

if __name__ == "__main__":
    # region 创建对象
    left_motor = SteppingMotor(47, 48, 38)
    right_motor = SteppingMotor(40, 39, 21)

    left_cylinder = ClampCylinder(17)
    right_cylinder = ClampCylinder(16)

    gas_switch = Pin(15, Pin.OUT)

    led = Pin(9, Pin.OUT)

    i2c = I2C(0, scl=Pin(5), sda=Pin(4))

    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    # endregion 

    while True:
        # region 接收信号
        PACKET_HEAD = b'@'
        PACKET_TAIL = b'#'

        data = b''  # 用于存储接收到的数据

        while True:
            byte = uart.read(1)
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

        t0 = time.time()
        oled.fill(0)

        gas_switch.value(1)
        led.on()
        oled.text(f'{len(str_data_lst)} steps', 0, 0)
        restore()
        led.off()

        t1 = time.time()
        oled.fill(0)
        oled.text(f'Finish in {t1-t0}seconds', 0, 0)
        oled.show()

        left_cylinder.open()
        right_cylinder.open()

        gas_switch.value(0)

        left_cylinder.close()
        right_cylinder.close()
