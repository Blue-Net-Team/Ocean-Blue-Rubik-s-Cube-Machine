#!/usr/bin/python3.8
import json
from multiprocessing import Pool
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:
    sys.path.remove(ros_path)

import cv2
import numpy as np
import joblib
import time
try:
    from cam.analysis_dad import Cam
except:
    from analysis_dad import Cam

MODOL_PATH = './Vision/model/svm_cube_10_10_down3.model'
IMG_PATH = './Vision/pic/D/Dt.png'


class DownCam(Cam):
    def __init__(self, jsonpath:str='./D.json') -> None:
        self.img_path = IMG_PATH
        super().__init__(jsonpath, MODOL_PATH)

        # 设置白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        # 自动曝光
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        
        self.cap.set(10,50) #0 亮度
        self.cap.set(11,80) #50 对比度
        self.cap.set(12,70) #64 饱和度
        self.cap.set(13,0) #0 色调
        self.cap.set(14,50) #64 锐度

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
            print(f"""D
{results[0]} {results[1]} {results[2]}   {results[9]} {results[10]} {results[11]}
{results[3]} {results[4]} {results[5]}   {results[12]} {results[13]} {results[14]}
{results[6]} {results[7]} {results[8]}   {results[15]} {results[16]} {results[17]}""")

            et = time.perf_counter()
            print("D spent {:.4f}s.".format((et - st)))

        res = []
        for i in range(2):
            color_state0:str = results[i*9][0]+results[i*9+1][0]+results[i*9+2][0]+results[i*9+3][0]+results[i*9+4][0]+results[i*9+5][0]+results[i*9+6][0]+results[i*9+7][0]+results[i*9+8][0]
            res.append(color_state0)
        return res


if __name__ == '__main__':  
    Dcam = DownCam()
    img0 = Dcam.read_usb_capture()
    Dcam.detect_color(img0, True)