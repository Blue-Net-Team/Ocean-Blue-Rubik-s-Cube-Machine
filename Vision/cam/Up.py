#!/usr/bin/python3.8
import json
import sys
from typing import Tuple
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


class UpCam(Cam):
    def __init__(self, jsonpath:str='./U.json') -> None:
        # 选择摄像头的编号
        self.cap = cv2.VideoCapture(1)

        # 设置白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        # 自动曝光
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        
        self.cap.set(10,-15) #0 亮度
        self.cap.set(11,90) #50 对比度
        self.cap.set(12,70) #64 饱和度
        self.cap.set(13,0) #0 色调
        self.cap.set(14,50) #64 锐度
        
        model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_up2.model'
        self.img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/U/Ut.png'
        self.clf = joblib.load(model_path) # 加载模型

        # 从json文件中读取ROI信息
        with open(jsonpath, 'r') as f:
            self.ROI = json.load(f)
            
    def read_usb_capture(self):
        while(self.cap.isOpened()):
            # 读取摄像头的画面
            ret, frame = self.cap.read()

            if not ret:
                continue

            # region 画框
            for i in range(18):
                cv2.rectangle(frame,(self.ROI[str(i+1)]['x']-7,self.ROI[str(i+1)]['y']-7),(self.ROI[str(i+1)]['x'] + 7,self.ROI[str(i+1)]['y'] + 7),(0,255,0))
                cv2.putText(frame, str(i+1), (self.ROI[str(i+1)]['x']-10, self.ROI[str(i+1)]['y']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            # endregion

            cv2.imwrite(self.img_path,frame)
            self.cap.release()
            cv2.destroyAllWindows()
        return frame

    def img2vector(self, img):
    
        img_arr = np.array(img) 
        img_normlization = img_arr/255 
        img_arr2 = np.reshape(img_normlization, (1,-1)) 
        return img_arr2

    def detect_color(self, img:cv2.typing.MatLike, ifio:bool=False):
        st = time.perf_counter()

        ROI_lst = []
        for i in range(18):
            ROI_lst.append(img[self.ROI[str(i+1)]['y'] - 5:self.ROI[str(i+1)]['y'] + 5, self.ROI[str(i+1)]['x'] - 5:self.ROI[str(i+1)]['x'] + 5])
        img2arr_list = list(map(self.img2vector, 
                                ROI_lst))

        results = list(map(self.clf.predict, img2arr_list))

        if ifio:
            print(f"""U
{results[0]} {results[1]} {results[2]}   {results[9]} {results[10]} {results[11]}
{results[3]} {results[4]} {results[5]}   {results[12]} {results[13]} {results[14]}
{results[6]} {results[7]} {results[8]}   {results[15]} {results[16]} {results[17]}""")

            et = time.perf_counter()
            print("U spent {:.4f}s.".format((et - st)))

        res = tuple()
        for i in range(2):
            color_state0:str = results[i*9][0]+results[i*9+1][0]+results[i*9+2][0]+results[i*9+3][0]+results[i*9+4][0]+results[i*9+5][0]+results[i*9+6][0]+results[i*9+7][0]+results[i*9+8][0]
            res += (color_state0,)
        return res

if __name__ == '__main__':  
    Ucam = UpCam()
    img0 = Ucam.read_usb_capture()
    # Ucam.detect_color(img0, True)