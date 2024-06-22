from machine import UART
from machine import Pin


def read(ser:UART, HEAD, TAIL) -> bytes:
    data = b''  # 用于存储接收到的数据

    while True:
        byte = ser.read(1)
        # if byte:print(byte)
        if byte == b'' or byte is None:
            continue
        if byte == HEAD:
            data = b''
            continue
        if byte == TAIL:
            break
        data += byte
    return data

class SteppingMotor:
    """步进电机"""
    def __init__(self, stp:int|None=None, en:int|None=None, _dir:int|None=None, ifpul=True, _id:int|None=None) -> None:
        """步进电机初始化
        * stp: 步进电机的步进脚
        * en: 步进电机的使能脚
        * _dir: 步进电机的方向脚
        * ifpul: 是否使用脉冲控制步进电机, 默认为True, 如果为False, 则使用串口控制步进电机
        * _id: 串口id, 默认为None, 如果ifpul为False, 则必须指定id(左手1 or 右手2)
        """
        self.ifpul = ifpul

        if self.ifpul:
            if stp is None or en is None or _dir is None:
                raise ValueError("stp, en and _dir must be specified")
            self.stp = Pin(stp, Pin.OUT)
            self.en = Pin(en, Pin.OUT)
            self.dir = Pin(_dir, Pin.OUT)
            self.en.value(1)

        else:
            # [tx,rx]
            pin_d = {1:[16, 15], 2:[18, 17]}
            if _id not in [1,2]:
                raise ValueError("Invalid id, id must be 1 or 2")
            self.serial = UART(_id, baudrate=9600, tx=pin_d[_id][0], rx=pin_d[_id][1])       # type: ignore
            self._id = _id
            self.ID = self._id.to_bytes(1, 'big')               # 地址位
            msg = self.ID + b'\x9a\x00\x00\x6b'        # 用于回零
            self.serial.write(msg)      # 回零
            # print(msg)
            res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
            print(res)
        

    def set_zero(self):
        """设置回零"""
        self.serial.write(self.ID + b'\x93\x88\x01\x6b')


    def rotate(self, sign:str, _stop=25):
        """使用脉冲的方式控制步进电机转动
        * sign: 旋转信号
        * _stop: 步进间隔
        """
        if not self.ifpul:
            d = {"1": (800, b'\x00'), "2": (1600, b'\x00'), "3":(800, b'\x01')}          # 1 means clockwise 90 degree
                                                                    # 2 means 180 degree
                                                                    # 3 means anticlockwise 90 degree
            
            FD = b'\xfd'                                            # 0xfd
            direction = d[sign][1]     # 方向
            v= b'\x00\xff'                                                # 速度
            a = b'\xf1'                      # 加速度
            pul_nums = d[sign][0].to_bytes(4, 'big')      # 脉冲数
            MODE = b'\x00'                                          # 模式
            MORE = b'\x00'                                          # 多机同步
            CHECK = b'\x6b'                                         # 校验位

            msg_send = self.ID + FD + direction + v + a + pul_nums + MODE + MORE + CHECK        # 发送的消息
            msg_read_t = b'\xfd\x02'                                     # 完成旋转之后返回的消息
            msg_read_f = b'\xfd\xe2'
            # endregion

            # 发送消息
            self.serial.write(msg_send)
            print(msg_send)
            # res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
            # print(res)

            # region 等待旋转完成(接收消息)
            res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
            if res == msg_read_t:
                print("suceess")
            elif res == msg_read_f:
                print("fail")
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


if __name__ == "__main__":
    left_motor = SteppingMotor(ifpul=False,_id=1)
    right_motor = SteppingMotor(ifpul=False,_id=2)

    # left_motor.rotate("1", 0)
    # left_motor.set_zero()