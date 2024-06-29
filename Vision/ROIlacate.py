"""
用于调整ROI的文件
"""
import cv2
import json

class ROILocater(object):
    """用于调整ROI的类
    ----
    封装了：
    * 用滑块调整ROI的方法
    * 使用鼠标点击就可以记录对应ID的ROI位置的方法
    """
    def __init__(self, num_id:int=9, window_name:str|None=None, cap_id:int=0, savapath:str|None=None) -> None:
        """
        类初始化
        ----
        * num_id: ROI的数量，默认为9
        * window_name: 窗口名称，默认为None，需要使用鼠标点击需要传入窗口名，与imshow的窗口名一致
        * cap_id: 摄像头ID，默认为0
        * savapath: 保存路径，默认为None
        """
        cap = cv2.VideoCapture(cap_id)
        _, frame = cap.read()

        self.x = 0
        self.y = 0
        self.w = 5
        self.h = 5

        self.max_x = frame.shape[1]
        self.max_y = frame.shape[0]
        self.max_w = 10
        self.max_h = 10

        self.id = 0

        self.savapath = savapath

        self.d = dict()
        self.num_id = num_id
        for i in range(self.num_id):
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
            print(f'x:{self.x}, y:{self.y} clicked!')

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
        cv2.createTrackbar('ID', 'ROI Selector', 0, self.num_id, self.callback_ID)

        # 用trackbau充当按钮
        cv2.createTrackbar('OK', 'ROI Selector', 0, 1, self.callback_OK)

    # region 回调函数
    def callback_x(self, x):
        x = int(x)
        self.x = x
    
    def callback_y(self, y):
        y = int(y)
        self.y = y

    def callback_w(self, w):
        w = int(w)
        self.w = w

    def callback_h(self, h):
        h = int(h)
        self.h = h

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

        for i in range(self.num_id):
            x = self.d[i]['x']
            y = self.d[i]['y']
            w = self.d[i]['w']
            h = self.d[i]['h']
            if not(x and y and w and h):
                continue
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
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
    WINDOW_NAME = 'frame'

    cap = cv2.VideoCapture(0)
    locater = ROILocater(window_name=WINDOW_NAME)

    locater.createTrackbar()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = locater.drawROI(frame)

        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
