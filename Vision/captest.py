"""
本文件是用于远程图传的调试文件
"""
import numpy as np
import cv2
import socket
import io
import struct
import time
import argparse


class VideoStreaming(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()			# 获取socket.socket()实例
        self.server_socket.bind((host, port))			# 绑定主机IP地址和端口号
        self.server_socket.listen(5)					# 设置监听数量

        print(" ")
        print("Host:", host)
        print("等待客服端连接...")
        print(" ")

        self.connection, self.client_address = self.server_socket.accept()		# 等待Client连接，返回实例和IP地址
        self.connect = self.connection.makefile('wb')							# 创建一个传输文件 写功能 写入数据时b''二进制类型数据
        self.host_name = socket.gethostname()									# 获得服务端主机名
        self.host_ip = socket.gethostbyname(self.host_name)						# 获得服务端主机IP地址
        time.sleep(3)

    def connecting(self):
        print('等待连接')
        self.connection, self.client_address = self.server_socket.accept()		# 等待Client连接，返回实例和IP地址
        self.connect = self.connection.makefile('wb')							# 创建一个传输文件 写功能 写入数据时b''二进制类型数据
        self.host_name = socket.gethostname()									# 获得服务端主机名
        self.host_ip = socket.gethostbyname(self.host_name)						# 获得服务端主机IP地址
        print('连接成功')
    
    def start(self) -> None:
        """开始传输视频流"""

        print("客服端已连接：")
        print("Client Host Name:", self.host_name)
        print("Connection from: ", self.client_address)
        print("Streaming...")
        self.stream = io.BytesIO()							# 创建一个io流，用于存放二进制数据

    def send(self, _img) -> None:
        """发送图像数据
        ----
        * _img: 传入的图像数据"""
        try:
            try:
                img_encode = cv2.imencode('.jpg', _img)[1]						# 编码
            except:
                print('没有读取到图像')
                return
            data_encode = np.array(img_encode)								# 将编码数据转换成二进制数据
            self.stream.write(data_encode)										# 将二进制数据存放到io流
            self.connect.write(struct.pack('<L', self.stream.tell()))			# struct.pack()将数据转换成什么格式    stream.tell()获得目前指针的位置，将数据写入io流后，数据指针跟着后移，
                                                                            # 也就是将数据长度转换成'<L'类型（无符号长整型），写入makefile传输文件
                                                                            # 它的作用相当于 帧头数据，单独收到这个数据表示开始传输一帧图片数据，因为图片大小确定，这个数也就定下不变
            self.connect.flush()											# 刷新，将数据长度发送出去
            self.stream.seek(0)													# 更新io流，将指针指向0
            self.connect.write(self.stream.read())								# 指针指向0后，从头开始读数据，然后写到makefile传输文件
            self.stream.seek(0)													# 更新指针
            self.stream.truncate()												# 更新io流数据，删除指针后面的数据

            self.connect.write(struct.pack('<L', 0))						# 发送0，相当于帧尾数据，单独收到这个数表示一帧图片传输结束
        except ConnectionResetError:
            print('连接已重置')
            self.connecting()


if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    # 1:上摄像头
    # 3:下摄像头
    # 0:左摄像头
    # 2:右摄像头
    arg.add_argument('--cap', type=int, help='摄像头id')
    opt = arg.parse_args()

    # host, port
    host = '192.168.1.245'        # 树莓派的ip地址
    port = 8000

    cap = cv2.VideoCapture(opt.cap)

    streamer = VideoStreaming(host, port)
    streamer.start()

    while True:
        ret, frame = cap.read()
        streamer.send(frame)
