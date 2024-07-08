#!/usr/bin/python3.8
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:
    sys.path.remove(ros_path)

import cv2
import time
try:
    from cam.analysis_dad import Cam
except:
    from analysis_dad import Cam

MODOL_PATH = './Vision/model/svm_cube_10_10_right.model'
IMG_PATH = './Vision/pic/R/Rt.png'

class RightCam(Cam):
    def __init__(self, jsonpath:str='./R.json') -> None:
        self.img_path = IMG_PATH
        super().__init__(jsonpath, MODOL_PATH)

        # 设置曝光时间,负值是短
        # cap.set(cv2.CAP_PROP_EXPOSURE, -3.9)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        # 设置白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        
        # 摄像头参数，可自行修改
        self.cap.set(10,-10) #0 亮度
        self.cap.set(11,50) #50 对比度
        self.cap.set(12,74) #64 饱和度
        self.cap.set(13,0) #0 色调
        self.cap.set(14,64) #64 锐度 图像增益

    def read_usb_capture(self):
        """
        从摄像头读取图像，并且将原图像进行保存
        ----
        * 返回值 img0: 读取的图像
        """
        img0, img1 = super().read_usb_capture()
        cv2.imwrite(self.img_path, img1)
        return img0
    
    def detect_color(self, img:cv2.typing.MatLike, ifio:bool=False):
        st = time.perf_counter()

        results = super().detect_color(img)

        if ifio:
            print(f"""R
{results[0]} {results[1]} {results[2]}
{results[3]} {results[4]} {results[5]}
{results[6]} {results[7]} {results[8]}""")
    
            et = time.perf_counter()
            print("R spent {:.4f}s.".format((et - st)))
        
        color_state = results[0][0]+results[1][0]+results[2][0]+results[3][0]+results[4][0]+results[5][0]+results[6][0]+results[7][0]+results[8][0]
        return color_state

if __name__ == '__main__':  
    Rcam = RightCam()
    img0 = Rcam.read_usb_capture()
    Rcam.detect_color(img0, True)
