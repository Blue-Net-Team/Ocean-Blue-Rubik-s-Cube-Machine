import struct
from typing import Iterable
import serial


class UART(serial.Serial):
    # FIXME: 应该通过UART类来调用send_pack_int方法，而不是通过UART的实例来调用。
    def __init__(self, port='/dev/ttyTHS1', baudrate=9600, timeout=None):
        """
        串口初始化
        * port: 串口号
        * baudrate: 波特率
        * timeout: 超时时间, 默认为None
        """
        super().__init__(port, baudrate, timeout=timeout)

    def write(self, data:str):
        """
        发送字符串数据,已经封装了包头包尾
            * 包头：@
            * 包尾：#
        """
        super().write(b'@')
        res = super().write(data.encode('ascii'))
        super().write(b'#')
        return res
    
    def read(self, head=b'@', tail=b'#'):
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