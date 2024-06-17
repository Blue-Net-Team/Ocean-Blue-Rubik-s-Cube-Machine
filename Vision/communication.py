import struct
from typing import Iterable
import serial


class UART(serial.Serial):
    # FIXME: 应该通过UART类来调用send_pack_int方法，而不是通过UART的实例来调用。
    def __init__(self, port='/dev/ttyTHS1', baudrate=9600, timeout:float|None=None):
        """
        串口初始化
        * port: 串口号
        * baudrate: 波特率
        * timeout: 超时时间, 默认为None
        """
        super().__init__(port, baudrate, timeout=timeout)

    @staticmethod
    def send_pack_int(func):
        """
        包头包尾修饰器
            * 包头：0xff
            * 包尾：0xfe
        """
        head = 255
        tail = 254
        def wrapper(self, *args, **kwargs):
            super().write(head.to_bytes(1, 'big'))     # 包头
            func(self, *args, **kwargs)
            super().write(tail.to_bytes(1, 'big'))     # 包尾
        return wrapper

    @staticmethod
    def send_pack_str(func):
        """
        包头包尾修饰器
            * 包头：@
            * 包尾：#
        """
        def wrapper(self, *args, **kwargs):
            super().write(b'@')     # 包头
            func(self, *args, **kwargs)
            super().write(b'#')     # 包尾
        return wrapper
    
    @staticmethod
    def read_pack(func):
        """
        包头包尾修饰器
            * 包头：0xff
            * 包尾：0xfe
        """
        head = 255
        HEAD = head.to_bytes(1, 'big')

        tail = 254
        TAIL = tail.to_bytes(1, 'big')

        def wrapper(self, _size:int):
            while True:
                if super().read(1) == HEAD:
                    break
            res = func(self, _size)
            while True:
                if super().read(1) == TAIL:
                    break
            return res
        return wrapper
    
    @send_pack_int
    def send_arr(self, args:Iterable):
        """发送数组"""
        for i in args:
            data = struct.pack('<i', i)     # 发送四个字节，端小字节序
            super().write(data)

    @send_pack_int
    def send(self, data:int):
        """发送整型数据"""
        newdata = struct.pack('<i', data)
        super().write(newdata)
    
    @send_pack_str
    def write(self, data:str) -> int | None:
        """
        发送字符串数据,已经封装了包头包尾
            * 包头：@
            * 包尾：#
        """
        return super().write(data.encode('ascii'))
    
    def read(self, head=b'@', tail=b'#') -> str|None:
        PACKET_HEAD = head
        PACKET_TAIL = tail

        data = b''  # 用于存储接收到的数据

        while True:
            byte = super().read()
            if byte == PACKET_HEAD:
                data = b''
                continue
            if byte == PACKET_TAIL:
                break
            data += byte
        res = data.decode('ascii')
        return res if res else None
    
    def __del__(self) -> None:
        return self.close()