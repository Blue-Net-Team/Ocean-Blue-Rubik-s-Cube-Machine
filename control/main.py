import time
from machine import UART
from machine import Pin
from machine import I2C
import ssd1306


class SteppingMotor:
    """步进电机"""
    def __init__(self, stp, en, _dir, ifpul=True, tx:int|None=None, rx:int|None=None, _id:int|None=None) -> None:
        """步进电机初始化
        * stp: 步进电机的步进脚
        * en: 步进电机的使能脚
        * dir: 步进电机的方向脚
        * ifpul: 是否使用脉冲控制步进电机, 默认为True, 如果为False, 则使用串口控制步进电机
        * tx: 串口发送引脚
        * rx: 串口接收引脚
        * id: 串口id, 默认为None, 如果ifpul为False, 则必须指定id(左手1 or 右手2)
        """
        self.stp = Pin(stp, Pin.OUT)
        self.en = Pin(en, Pin.OUT)
        self.dir = Pin(_dir, Pin.OUT)
        self.en.value(1)

        self.ifpul = ifpul
        if self.ifpul:
            if _id not in [1,2]:
                raise ValueError("Invalid id, id must be 1 or 2")
            self.serial = UART(_id, baudrate=9600, tx=tx, rx=rx)       # type: ignore
            self._id = _id
        

    def rotate(self, sign:str, _stop=25):
        """使用脉冲的方式控制步进电机转动
        * sign: 旋转信号
        * _stop: 步进间隔
        """
        if not self.ifpul:
            d = {"1": (800, 0x00), "2": (1600, 0x00), "3":(800, 0x01)}          # 1 means clockwise 90 degree
                                                                                # 2 means 180 degree
                                                                                # 3 means anticlockwise 90 degree
            # region 命令处理
            ID = self._id.to_bytes(1, byteorder='big')               # 地址位
            FD = b'\xfd'                                            # 0xfd
            direction = d[sign][1].to_bytes(1, byteorder='big')     # 方向
            direction = int.from_bytes(direction, byteorder='big')
            v= 0x4ff                                                # 0x4ff(最大速度)
            d_v = (v&0x4ff)|(direction<<8)                           # 方向和速度
            d_v = d_v.to_bytes(2, byteorder='big')
            a = 208
            a = a.to_bytes(1, byteorder='big')                      # 加速度
            pul_nums = d[sign][0].to_bytes(3, byteorder='big')      # 脉冲数
            CHECK = b'\x6b'                                         # 校验位

            msg_send = ID + FD + d_v + a + pul_nums + CHECK        # 发送的消息
            msg_read = b'\x9f'                                     # 完成旋转之后返回的消息
            # endregion

            # 发送消息
            self.serial.write(msg_send)

            # region 等待旋转完成(接收消息)
            data = b''  # 用于存储接收到的数据
            while True:
                byte = uart.read(1)
                if byte == b'' or byte is None:
                    continue
                if byte == ID:
                    data = b''
                data += byte
                if byte == CHECK:
                    if data == msg_read:
                        break
            # endregion
        else:
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

# 与Jetson Nano通信的串口对象
uart = UART(0, baudrate=9600, tx=8, rx=7)       # type: ignore

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
        

def read(HEAD:str='@', TAIL:str='#') -> bytes:
    # region 接收信号
    PACKET_HEAD = HEAD.encode('ASCII')
    PACKET_TAIL = TAIL.encode('ASCII')

    data = b''  # 用于存储接收到的数据

    while True:
        byte = uart.read(1)
        if byte == b'' or byte is None:
            continue
        if byte == PACKET_HEAD:
            data = b''
            continue
        if byte == PACKET_TAIL:
            break
        data += byte
    return data

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
        led.value(1)        # 就绪指示灯亮起
        data = read()
        str_data = data.decode()
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
