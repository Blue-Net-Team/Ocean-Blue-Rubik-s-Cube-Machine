"""
用于调整ROI的文件
----
* 封装了远程图传的用法
* 封装了调整ROI的类，可以用鼠标来直接点击ROI的位置
在滑块中调整ROI的编号，然后直接用鼠标点击色块的位置，就可以记录ROI的位置，会自动保存到对应的json文件中
json文件的保存路径位于211行中传参的位置，可以自行修改，在json文件中会记录每个ID ROI的位置信息和大小(宽和高)
才颜色识别的文件中需要忽略大小信息
"""
import cv2
import json
import socket
import numpy as np

class ReceiveImg(object):
    def __init__(self, host, port):
        """初始化
        * host: 树莓派的IP地址
        * port: 端口号，与树莓派设置的端口号一致"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)					# 设置创建socket服务的Client客服务的参数
        self.client_socket.connect((host, port))												# 连接的主机IP地址和端口
        self.connection = self.client_socket.makefile('rb')										# 创建一个makefile传输文件，读功能，读数据是b''二进制类型
        # need bytes here
        self.stream_bytes = b' '											# 创建一个变量，存放的数据类型是b''二进制类型数据
        
        print(" ")
        print("已连接到服务端：")
        print("Host : ", host)
        print("请按‘q’退出图像传输!")

    def read(self):
        try:
            msg = self.connection.read(1024)						# 读makefile传输文件，一次读1024个字节
            self.stream_bytes += msg
            first = self.stream_bytes.find(b'\xff\xd8')					# 检测帧头位置
            last = self.stream_bytes.find(b'\xff\xd9')					# 检测帧尾位置

            if first != -1 and last != -1:
                jpg = self.stream_bytes[first:last + 2]					# 帧头和帧尾中间的数据就是二进制图片数据（编码后的二进制图片数据，需要解码后使用）
                self.stream_bytes = self.stream_bytes[last + 2:]				# 更新stream_bytes数据
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)			# 将二进制图片数据转换成numpy.uint8格式（也就是图片格式）数据，然后解码获得图片数据
                return True, image
            return False, None

        except:
            print("Error：连接出错！")
            return False, None
        
class ROILocater(object):
    """用于调整ROI的类
    ----
    封装了：
    * 用滑块调整ROI的方法
    * 使用鼠标点击就可以记录对应ID的ROI位置的方法
    """
    def __init__(self, _cap:cv2.VideoCapture|ReceiveImg, num_id:int=9, window_name:str|None=None, savapath:str|None=None) -> None:
        """
        类初始化
        ----
        * num_id: ROI的数量，默认为9
        * window_name: 窗口名称，默认为None，需要使用鼠标点击需要传入窗口名，与imshow的窗口名一致
        * cap_id: 摄像头ID，默认为0
        * savapath: 保存路径，默认为None
        """
        self.x = 0
        self.y = 0
        self.w = 14
        self.h = 14

        while True:
            _, frame = _cap.read()
            if frame is None:       # 如果没有读取到帧则跳过
                continue
            self.max_x = frame.shape[1]
            self.max_y = frame.shape[0]
            break
        self.max_w = 50
        self.max_h = 50

        self.id = 0

        self.savapath = savapath

        self.d = dict()
        self.num_id = num_id-1
        for i in range(1, self.num_id+2):
            self.d[i] = {'x': None, 'y': None, 'w': None, 'h': None}

        if window_name:
            cv2.namedWindow(window_name)
            cv2.setMouseCallback(window_name, self.mouse_action)

    def mouse_action(self, event, x, y, flags, param):
        """鼠标回调函数
        ----
        鼠标左键单击触发,会保存ROI的位置信息并且将对应ID的滑动条更新"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x = x-self.w//2
            self.y = y-self.h//2
            # 更新滑块
            cv2.setTrackbarPos('x', 'ROI Selector', self.x)
            cv2.setTrackbarPos('y', 'ROI Selector', self.y)
            print(f'ID{self.id}, x:{self.x}, y:{self.y} clicked!')

            # 写入字典
            self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}
            # 保存
            self.save(self.savapath)

    def createTrackbar(self):
        """
        创建调整ROI的滑动条
        * x: ROI的x坐标
        * y: ROI的y坐标
        * w: ROI的宽度
        * h: ROI的高度
        * ID: ROI的ID
        * OK: 用于确认ROI的滑动条
        """
        cv2.namedWindow('ROI Selector')
        cv2.createTrackbar('x', 'ROI Selector', self.x, self.max_x, self.callback_x)
        cv2.createTrackbar('y', 'ROI Selector', self.y, self.max_y, self.callback_y)
        cv2.createTrackbar('w', 'ROI Selector', self.w, self.max_w, self.callback_w)
        cv2.createTrackbar('h', 'ROI Selector', self.h, self.max_h, self.callback_h)
        cv2.createTrackbar('ID', 'ROI Selector', 1, self.num_id+1, self.callback_ID)

        # 用trackbau充当按钮
        cv2.createTrackbar('OK', 'ROI Selector', 0, 1, self.callback_OK)

    # region 回调函数
    def callback_x(self, x):
        x = int(x)
        self.x = x
        # 更新字典
        self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}
    
    def callback_y(self, y):
        y = int(y)
        self.y = y
        # 更新字典
        self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}

    def callback_w(self, w):
        w = int(w)
        self.w = w
        # 更新字典
        self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}

    def callback_h(self, h):
        h = int(h)
        self.h = h
        # 更新字典
        self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}

    def callback_OK(self, value):
        if value == 1:
            print(f'id:{self.id}, x:{self.x}, y:{self.y}, w:{self.w}, h:{self.h}')
            # 修改字典
            self.d[self.id] = {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}
            # 将ROI信息保
            self.save(self.savapath)

            # 重置滑动条
            cv2.setTrackbarPos('OK', 'ROI Selector', 0)
            cv2.setTrackbarPos('x', 'ROI Selector', 0)
            cv2.setTrackbarPos('y', 'ROI Selector', 0)
            cv2.setTrackbarPos('w', 'ROI Selector', 5)
            cv2.setTrackbarPos('h', 'ROI Selector', 5)
        else:
            pass

    def callback_ID(self, value):
        self.id = value
    # endregion
        
    def drawROI(self, _frame:cv2.typing.MatLike, ifcopy:bool = True) -> cv2.typing.MatLike:
        """
        将ROI区域画在图像上
        * _frame: 输入图像
        * ifcopy: 是否对原图像深拷贝，默认为True(不会影响原图像)
        """
        if ifcopy:
            img = _frame.copy()
        else:
            img = _frame

        for i in range(1, self.num_id+2):     # 从1到num_id
            x = self.d[i]['x']
            y = self.d[i]['y']
            w = self.d[i]['w']
            h = self.d[i]['h']
            if not(x and y and w and h):
                continue
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 200, 0), 1)
            cv2.putText(img, f'{i}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)
            
        return img
    
    def save(self, path:str|None=None):
        """
        保存ROI信息到json文件
        * path: 保存路径
        """
        if not path:
            path = 'ROI.json'
        with open(path, 'w') as f:
            json.dump(self.d, f)

if __name__ == '__main__':
    WINDOW_NAME = 'real'
    reveiver = ReceiveImg('192.168.1.245', 8000)
    locater = ROILocater(_cap=reveiver, window_name=WINDOW_NAME,savapath='UP.json', num_id=18)
    locater.createTrackbar()

    cv2.namedWindow(WINDOW_NAME)
    while True:
        _, img = reveiver.read()
        if img is None:
            continue
        
        img1 = locater.drawROI(img)
        cv2.imshow(WINDOW_NAME, img1)
        # cv2.imshow('ori', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
