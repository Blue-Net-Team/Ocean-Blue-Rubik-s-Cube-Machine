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

class RightCam(Cam):
    def __init__(self, jsonpath:str='./R.json') -> None:
        
        # 选择摄像头的编号
        self.cap = cv2.VideoCapture(2)
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
        model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_right.model'
        self.img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/R/Rt.png'
        self.clf = joblib.load(model_path) # 加载模
        # 从json文件中读取ROI信息
        with open(jsonpath, 'r') as f:
            ROI = json.load(f)
            self.point1_x = ROI['1']['x']
            self.point1_y = ROI['1']['y']

            self.point2_x = ROI['2']['x']
            self.point2_y = ROI['2']['y']

            self.point3_x = ROI['3']['x']
            self.point3_y = ROI['3']['y']

            self.point4_x = ROI['4']['x']
            self.point4_y = ROI['4']['y']

            self.point5_x = ROI['5']['x']
            self.point5_y = ROI['5']['y']

            self.point6_x = ROI['6']['x']
            self.point6_y = ROI['6']['y']

            self.point7_x = ROI['7']['x']
            self.point7_y = ROI['7']['y']

            self.point8_x = ROI['8']['x']
            self.point8_y = ROI['8']['y']

            self.point9_x = ROI['9']['x']
            self.point9_y = ROI['9']['y']

    def read_usb_capture(self):
        frame_num = 0
        
        while(self.cap.isOpened()):
            # 读取摄像头的画面
            ret, frame = self.cap.read()
            
            if not ret:
                continue

            frame_num = frame_num + 1
            cv2.rectangle(frame,(self.point1_x-7,self.point1_y-7),(self.point1_x + 7,self.point1_y + 7),(0,255,0))
            cv2.putText(frame, '1', (self.point1_x-10, self.point1_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point2_x-7,self.point2_y-7),(self.point2_x + 7,self.point2_y + 7),(0,255,0))
            cv2.putText(frame, '2', (self.point2_x-10, self.point2_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point3_x-7,self.point3_y-7),(self.point3_x + 7,self.point3_y + 7),(0,255,0))
            cv2.putText(frame, '3', (self.point3_x-10, self.point3_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point4_x-7,self.point4_y-7),(self.point4_x + 7,self.point4_y + 7),(0,255,0))
            cv2.putText(frame, '4', (self.point4_x-10, self.point4_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point5_x-7,self.point5_y-7),(self.point5_x + 7,self.point5_y + 7),(0,255,0))
            cv2.putText(frame, '5', (self.point5_x-10, self.point5_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point6_x-7,self.point6_y-7),(self.point6_x + 7,self.point6_y + 7),(0,255,0))
            cv2.putText(frame, '6', (self.point6_x-10, self.point6_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point7_x-7,self.point7_y-7),(self.point7_x + 7,self.point7_y + 7),(0,255,0))
            cv2.putText(frame, '7', (self.point7_x-10, self.point7_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point8_x-7,self.point8_y-7),(self.point8_x + 7,self.point8_y + 7),(0,255,0))
            cv2.putText(frame, '8', (self.point8_x-10, self.point8_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point9_x-7,self.point9_y-7),(self.point9_x + 7,self.point9_y + 7),(0,255,0))
            cv2.putText(frame, '9', (self.point9_x-10, self.point9_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

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

        ROI1 = img[self.point1_y-5:self.point1_y + 5, self.point1_x-5:self.point1_x + 5]
        ROI2 = img[self.point2_y-5:self.point2_y + 5, self.point2_x-5:self.point2_x + 5]
        ROI3 = img[self.point3_y-5:self.point3_y + 5, self.point3_x-5:self.point3_x + 5]
        ROI4 = img[self.point4_y-5:self.point4_y + 5, self.point4_x-5:self.point4_x + 5]
        ROI5 = img[self.point5_y-5:self.point5_y + 5, self.point5_x-5:self.point5_x + 5]
        ROI6 = img[self.point6_y-5:self.point6_y + 5, self.point6_x-5:self.point6_x + 5]
        ROI7 = img[self.point7_y-5:self.point7_y + 5, self.point7_x-5:self.point7_x + 5]
        ROI8 = img[self.point8_y-5:self.point8_y + 5, self.point8_x-5:self.point8_x + 5]
        ROI9 = img[self.point9_y-5:self.point9_y + 5, self.point9_x-5:self.point9_x + 5]

        img2arr_list = list(map(self.img2vector, 
                                [ROI1, ROI2, ROI3, ROI4, ROI5, ROI6, ROI7, ROI8, ROI9]))


        results = list(map(self.clf.predict, img2arr_list))

        if ifio:
            print(f"""
R
{results[0]} {results[1]} {results[2]}
{results[3]} {results[4]} {results[5]}
{results[6]} {results[7]} {results[8]}
                  """)
    
            et = time.perf_counter()
            print("R spent {:.4f}s.".format((et - st)))
        
        color_state = results[0][0]+results[1][0]+results[2][0]+results[3][0]+results[4][0]+results[5][0]+results[6][0]+results[7][0]+results[8][0]
        return color_state

if __name__ == '__main__':  
    Rcam = RightCam()
    img0 = Rcam.read_usb_capture()
    Rcam.detect_color(img0)
