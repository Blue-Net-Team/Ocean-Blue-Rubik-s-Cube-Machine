import time
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

        if _id:
            # [tx,rx]
            pin_d = {1:[16, 15], 2:[18, 17]}
            if _id not in [1,2]:
                raise ValueError("Invalid id, id must be 1 or 2")
            self.serial = UART(_id, baudrate=115200, tx=pin_d[_id][0], rx=pin_d[_id][1])       # type: ignore
            self._id = _id
            self.ID = self._id.to_bytes(1, 'big')               # 地址位

        if self.ifpul:
            if stp is None or en is None or _dir is None:
                raise ValueError("stp, en and _dir must be specified")
            self.stp = Pin(stp, Pin.OUT)
            self.en = Pin(en, Pin.OUT)
            self.dir = Pin(_dir, Pin.OUT)
            self.en.value(1)

        else:
            self.go_zero()
            # print(msg)
            # res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
            # print(res)
        

    def set_zero(self):
        """设置回零"""
        self.serial.write(self.ID + b'\x93\x88\x01\x6b')        # type:ignore

    def go_zero(self):
        msg = self.ID + b'\x9a\x00\x00\x6b'        # 回零指令
        self.serial.write(msg)      # type:ignore 回零
        # res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
        # print(res)

    def check_zero(self):
        """校准编码器"""
        msg = self.ID + b'\x06\x45\x6b'        # 检查回零
        self.serial.write(msg)      # type:ignore

    def rotate(self, sign:str, _stop0=25):
        """使用脉冲的方式控制步进电机转动
        * sign: 旋转信号
        * _stop: 步进间隔
        """
        if not self.ifpul:
            d = {"1": (800 , b'\x00'),              # 1 means clockwise 90 degree
                 "2": (1600, b'\x00'),              # 2 means 180 degree
                 "3": (800 , b'\x01')}              # 3 means anticlockwise 90 degree       
            
            FD = b'\xfd'                                            # 0xfd
            direction = d[sign][1]                                  # 方向
            v= b'\xff\xff'                                          # 速度
            a = b'\xf1'                                             # 加速度
            pul_nums = d[sign][0].to_bytes(4, 'big')                # 脉冲数
            MODE = b'\x00'                                          # 模式
            MORE = b'\x00'                                          # 多机同步
            CHECK = b'\x6b'                                         # 校验位

            msg_send = self.ID + FD + direction + v + a + pul_nums + MODE + MORE + CHECK        # 发送的消息
            # 完成旋转之后返回的消息
            msg_read_t = b'\xfd\x02'
            msg_read_f = b'\xfd\xe2'
            # endregion

            # 发送消息
            self.serial.write(msg_send)
            # print(msg_send)

            # region 等待旋转完成(接收消息)
            res = read(self.serial, HEAD=self.ID, TAIL=b'\x6b')
            print(res)
            if res == msg_read_t:
                print("suceess")
            elif res == msg_read_f:
                print("fail")
            elif res == b'\x00\xee':
                print("error")
            # endregion
        else:
            d = {"1": (0.25, 0), "2": (0.5, 0), "3":(0.25, 1)}
            pul0, direction = d[sign]
            self.dir.value(direction)

            pul1 = (pul0 / 3200)           # 加速
            pul3 = (pul0 / 32)           # 减速
            pul2 = pul0-pul1-pul3       # 匀速

            for i in range(3200 * pul1, 0, -1):
                self.stp.value(1)
                for _ in range(i):pass
                self.stp.value(0)
                for _ in range(i):pass

            # 匀速
            for i in range(3200 * pul2):
                self.stp.value(1)
                for _ in range(_stop0):pass
                self.stp.value(0)
                for _ in range(_stop0):pass

            # 减速
            for i in range(3200 * pul3):
                self.stp.value(1)
                for _ in range(i):pass
                self.stp.value(0)
                for _ in range(i):pass

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