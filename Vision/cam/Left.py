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

MODOL_PATH = './Vision/model/svm_cube_10_10_left4.model'
IMG_PATH = './Vision/pic/L/L.png'

class LeftCam(Cam):
    def __init__(self, jsonpath:str='./L.json'):
        self.img_path = IMG_PATH
        super().__init__(jsonpath, MODOL_PATH)
        
        # 设置曝光时间,负值是短
        # cap.set(cv2.CAP_PROP_EXPOSURE, 1250.0)

        # 设置白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        
        self.cap.set(10,5) #0 亮度
        self.cap.set(11,85) #50 对比度
        self.cap.set(12,74) #64 饱和度
        self.cap.set(13,0) #0 色调
        self.cap.set(14,70) #64 锐度 图像增益

    def read_usb_capture(self):
        img0, img1 = super().read_usb_capture()
        cv2.imwrite(self.img_path, img1)
        return img0

    def detect_color(self, img:cv2.typing.MatLike, ifio:bool=False):
        st = time.perf_counter()

        results = super().detect_color(img)

        if ifio:
            print(f"""L
{results[0]} {results[1]} {results[2]}
{results[3]} {results[4]} {results[5]}
{results[6]} {results[7]} {results[8]}""")
            
            et = time.perf_counter()
            print("L spent {:.4f}s.".format((et - st)))
        
        color_state = results[0][0]+results[1][0]+results[2][0]+results[3][0]+results[4][0]+results[5][0]+results[6][0]+results[7][0]+results[8][0]
        return color_state

if __name__ == '__main__':  
    Lcam = LeftCam()
    img0 = Lcam.read_usb_capture()
    Lcam.detect_color(img0, True)