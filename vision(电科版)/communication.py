from email import message
import serial
import time

# 串口打开函数
def open_ser():
    port = '/dev/ttyUSB0'  # 串口号
    baudrate = 115200  # 波特率
    try:
        global ser
        ser = serial.Serial(port, baudrate, timeout=2)
        if(ser.isOpen() == True):
            print("串口打开成功")
    except Exception as exc:
        print("串口打开异常", exc)

# 数据发送
def send_msg(send_data):
    try:
        ser.write(str(send_data).encode("gbk"))
        print("已发送数据:", send_data)
    except Exception as exc:
        print("发送异常", exc)

# 接收数据
def read_msg():
    try:
        print("等待接收数据")
        while True:
            data = ser.read(ser.in_waiting).decode('gbk')
            if data != '':
                break
        print("已接受到数据:", data)
    except Exception as exc:
        print("读取异常", exc)

# 关闭串口
def close_ser():
    try:
        ser.close()
        if ser.isOpen():
            print("串口未关闭")
        else:
            print("串口已关闭")
    except Exception as exc:
        print("串口关闭异常", exc)


if __name__ == '__main__':
    open_ser()   # 打开串口
    read_msg()
    send_msg('LC RC\r\n')
    time.sleep(0.25)
    send_msg('LC RC\r\n')
    time.sleep(0.25)
    send_msg('L1\r\n')
    time.sleep(0.5)
    send_msg('L3\r\n')
    time.sleep(0.5)
    send_msg('L2\r\n')
    time.sleep(0.5)
    send_msg('L2\r\n')
    time.sleep(0.5)
    send_msg('R1\r\n')
    time.sleep(0.5)
    send_msg('R3\r\n')
    time.sleep(0.5)
    send_msg('R2\r\n')
    time.sleep(0.5)
    send_msg('R2\r\n')
    time.sleep(0.5)
    send_msg('LO RO\r\n')
    while True:
        _message = input()
        if _message == 'q':
            break
        _message = _message + '\r\n'
        send_msg(_message)
    close_ser()  # 关闭串口
