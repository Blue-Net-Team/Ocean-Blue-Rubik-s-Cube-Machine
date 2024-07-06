#!/usr/bin/python3.8
import json
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:

    sys.path.remove(ros_path)

import cv2

import numpy as np
import joblib
# import matplotlib.pyplot as plt
import time
from cam.analysis_dad import Cam

class LeftCam(Cam):
    def __init__(self, jsonpath:str='./L.json'):
        # 选择摄像头的编号
        self.cap = cv2.VideoCapture(0)
        
        # 设置曝光时间,负值是短
        # cap.set(cv2.CAP_PROP_EXPOSURE, 1250.0)

        # 设置白平衡
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        
        self.cap.set(10,0) #0 亮度
        self.cap.set(11,85) #50 对比度
        self.cap.set(12,74) #64 饱和度
        self.cap.set(13,0) #0 色调
        self.cap.set(14,70) #64 锐度 图像增益

        model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_left4.model'
        self.img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/L/L.png'
        self.clf = joblib.load(model_path) # 加载模型

        # 从json文件中读取ROI信息
        with open(jsonpath, 'r') as f:
            self.ROI = json.load(f)

    def read_usb_capture(self):
        frame_num = 0
        while(self.cap.isOpened()):
            # 读取摄像头的画面
            ret, frame = self.cap.read()
            
            if not ret:
                continue

            frame_num = frame_num + 1

            # region 画框
            for i in range(9):
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
        for i in range(9):
            ROI_lst.append(img[self.ROI[str(i+1)]['y'] - 5:self.ROI[str(i+1)]['y'] + 5, self.ROI[str(i+1)]['x'] - 5:self.ROI[str(i+1)]['x'] + 5])
        img2arr_list = list(map(self.img2vector, 
                                ROI_lst))

        results = list(map(self.clf.predict, img2arr_list))

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
    Lcam.detect_color(img0)