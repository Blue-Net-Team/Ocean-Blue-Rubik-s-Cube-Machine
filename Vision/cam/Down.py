#!/usr/bin/python3.8
import json
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:
    sys.path.remove(ros_path)

import cv2
import numpy as np
import joblib
import time


class DownCam():
    def __init__(self) -> None:
        model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_down3.model'
        self.img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/D/Dt.png'
        self.clf = joblib.load(model_path) # 加载模型

        # 从json文件中读取ROI信息
        with open('./D.json', 'r') as f:
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

            self.point10_x = ROI['10']['x']
            self.point10_y = ROI['10']['y']

            self.point11_x = ROI['11']['x']
            self.point11_y = ROI['11']['y']

            self.point12_x = ROI['12']['x']
            self.point12_y = ROI['12']['y']

            self.point13_x = ROI['13']['x']
            self.point13_y = ROI['13']['y']

            self.point14_x = ROI['14']['x']
            self.point14_y = ROI['14']['y']

            self.point15_x = ROI['15']['x']
            self.point15_y = ROI['15']['y']

            self.point16_x = ROI['16']['x']
            self.point16_y = ROI['16']['y']

            self.point17_x = ROI['17']['x']
            self.point17_y = ROI['17']['y']

            self.point18_x = ROI['18']['x']
            self.point18_y = ROI['18']['y']
 
    def read_usb_capture(self):
        # 选择摄像头的编号
        cap = cv2.VideoCapture(3)

        # 设置白平衡
        cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        # 自动曝光
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        
        cap.set(10,50) #0 亮度
        cap.set(11,70) #50 对比度
        cap.set(12,64) #64 饱和度
        cap.set(13,0) #0 色调
        cap.set(14,74) #64 锐度
        
        while(cap.isOpened()):
            # 读取摄像头的画面
            ret, frame = cap.read()

            frame = cv2.GaussianBlur(frame, (3, 3), 0)      # 高斯模糊

            # 真实图
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

            cv2.rectangle(frame,(self.point10_x-7,self.point10_y-7),(self.point10_x + 7,self.point10_y + 7),(0,255,0))
            cv2.putText(frame, '10', (self.point10_x-15, self.point10_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point11_x-7,self.point11_y-7),(self.point11_x + 7,self.point11_y + 7),(0,255,0))
            cv2.putText(frame, '11', (self.point11_x-15, self.point11_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point12_x-7,self.point12_y-7),(self.point12_x + 7,self.point12_y + 7),(0,255,0))
            cv2.putText(frame, '12', (self.point12_x-15, self.point12_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point13_x-7,self.point13_y-7),(self.point13_x + 7,self.point13_y + 7),(0,255,0))
            cv2.putText(frame, '13', (self.point13_x-15, self.point13_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point14_x-7,self.point14_y-7),(self.point14_x + 7,self.point14_y + 7),(0,255,0))
            cv2.putText(frame, '14', (self.point14_x-15, self.point14_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point15_x-7,self.point15_y-7),(self.point15_x + 7,self.point15_y + 7),(0,255,0))
            cv2.putText(frame, '15', (self.point15_x-15, self.point15_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point16_x-7,self.point16_y-7),(self.point16_x + 7,self.point16_y + 7),(0,255,0))
            cv2.putText(frame, '16', (self.point16_x-15, self.point16_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point17_x-7,self.point17_y-7),(self.point17_x + 7,self.point17_y + 7),(0,255,0))
            cv2.putText(frame, '17', (self.point17_x-15, self.point17_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.rectangle(frame,(self.point18_x-7,self.point18_y-7),(self.point18_x + 7,self.point18_y + 7),(0,255,0))
            cv2.putText(frame, '18', (self.point18_x-15, self.point18_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

            cv2.imwrite(self.img_path,frame)
            cap.release()
            cv2.destroyAllWindows()
        return frame

    def img2vector(self, img):
    
        img_arr = np.array(img) 
        img_normlization = img_arr/255 
        img_arr2 = np.reshape(img_normlization, (1,-1)) 
        return img_arr2

    def detect_color(self):
        st = time.perf_counter()
        img = self.read_usb_capture()

        ROI1 = img[self.point1_y - 5:self.point1_y + 5, self.point1_x - 5:self.point1_x + 5]
        ROI2 = img[self.point2_y - 5:self.point2_y + 5, self.point2_x - 5:self.point2_x + 5]
        ROI3 = img[self.point3_y - 5:self.point3_y + 5, self.point3_x - 5:self.point3_x + 5]
        ROI4 = img[self.point4_y - 5:self.point4_y + 5, self.point4_x - 5:self.point4_x + 5]
        ROI5 = img[self.point5_y - 5:self.point5_y + 5, self.point5_x - 5:self.point5_x + 5]
        ROI6 = img[self.point6_y - 5:self.point6_y + 5, self.point6_x - 5:self.point6_x + 5]
        ROI7 = img[self.point7_y - 5:self.point7_y + 5, self.point7_x - 5:self.point7_x + 5]
        ROI8 = img[self.point8_y - 5:self.point8_y + 5, self.point8_x - 5:self.point8_x + 5]
        ROI9 = img[self.point9_y - 5:self.point9_y + 5, self.point9_x - 5:self.point9_x + 5]

        ROI10 = img[self.point10_y - 5:self.point10_y + 5, self.point10_x - 5:self.point10_x + 5]
        ROI11 = img[self.point11_y - 5:self.point11_y + 5, self.point11_x - 5:self.point11_x + 5]
        ROI12 = img[self.point12_y - 5:self.point12_y + 5, self.point12_x - 5:self.point12_x + 5]
        ROI13 = img[self.point13_y - 5:self.point13_y + 5, self.point13_x - 5:self.point13_x + 5]
        ROI14 = img[self.point14_y - 5:self.point14_y + 5, self.point14_x - 5:self.point14_x + 5]
        ROI15 = img[self.point15_y - 5:self.point15_y + 5, self.point15_x - 5:self.point15_x + 5]
        ROI16 = img[self.point16_y - 5:self.point16_y + 5, self.point16_x - 5:self.point16_x + 5]
        ROI17 = img[self.point17_y - 5:self.point17_y + 5, self.point17_x - 5:self.point17_x + 5]
        ROI18 = img[self.point18_y - 5:self.point18_y + 5, self.point18_x - 5:self.point18_x + 5]

        img2arr1 = self.img2vector(ROI1)
        img2arr2 = self.img2vector(ROI2)
        img2arr3 = self.img2vector(ROI3)
        img2arr4 = self.img2vector(ROI4)
        img2arr5 = self.img2vector(ROI5)
        img2arr6 = self.img2vector(ROI6)
        img2arr7 = self.img2vector(ROI7)
        img2arr8 = self.img2vector(ROI8)
        img2arr9 = self.img2vector(ROI9)

        img2arr10 = self.img2vector(ROI10)
        img2arr11 = self.img2vector(ROI11)
        img2arr12 = self.img2vector(ROI12)
        img2arr13 = self.img2vector(ROI13)
        img2arr14 = self.img2vector(ROI14)
        img2arr15 = self.img2vector(ROI15)
        img2arr16 = self.img2vector(ROI16)
        img2arr17 = self.img2vector(ROI17)
        img2arr18 = self.img2vector(ROI18)

        
        preResult1 = self.clf.predict(img2arr1)
        preResult2 = self.clf.predict(img2arr2)
        preResult3 = self.clf.predict(img2arr3)
        preResult4 = self.clf.predict(img2arr4)
        preResult5 = self.clf.predict(img2arr5)
        preResult6 = self.clf.predict(img2arr6)
        preResult7 = self.clf.predict(img2arr7)
        preResult8 = self.clf.predict(img2arr8)
        preResult9 = self.clf.predict(img2arr9)

        preResult10 = self.clf.predict(img2arr10)
        preResult11 = self.clf.predict(img2arr11)
        preResult12 = self.clf.predict(img2arr12)
        preResult13 = self.clf.predict(img2arr13)
        preResult14 = self.clf.predict(img2arr14)
        preResult15 = self.clf.predict(img2arr15)
        preResult16 = self.clf.predict(img2arr16)
        preResult17 = self.clf.predict(img2arr17)
        preResult18 = self.clf.predict(img2arr18)

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        print(preResult1,preResult2,preResult3,'  ',preResult10,preResult11,preResult12)
        print(preResult4,preResult5,preResult6,'  ',preResult13,preResult14,preResult15)
        print(preResult7,preResult8,preResult9,'  ',preResult16,preResult17,preResult18)
        
        et = time.perf_counter()
        print("spent {:.4f}s.".format((et - st)))

        color_state1 = preResult1[0]+preResult2[0]+preResult3[0]+preResult4[0]+preResult5[0]+preResult6[0]+preResult7[0]+preResult8[0]+preResult9[0]
        color_state2 = preResult10[0]+preResult11[0]+preResult12[0]+preResult13[0]+preResult14[0]+preResult15[0]+preResult16[0]+preResult17[0]+preResult18[0]
        return color_state1,color_state2

if __name__ == '__main__':  
    Dcam = DownCam()
    Dcam.detect_color()