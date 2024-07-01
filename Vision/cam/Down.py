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

model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_down3.model'
img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/D/Dt.png'
clf = joblib.load(model_path) # 加载模型

# 从json文件中读取ROI信息
with open('./D.json', 'r') as f:
    ROI = json.load(f)
    point1_x = ROI['1']['x']
    point1_y = ROI['1']['y']

    point2_x = ROI['2']['x']
    point2_y = ROI['2']['y']

    point3_x = ROI['3']['x']
    point3_y = ROI['3']['y']

    point4_x = ROI['4']['x']
    point4_y = ROI['4']['y']

    point5_x = ROI['5']['x']
    point5_y = ROI['5']['y']

    point6_x = ROI['6']['x']
    point6_y = ROI['6']['y']

    point7_x = ROI['7']['x']
    point7_y = ROI['7']['y']

    point8_x = ROI['8']['x']
    point8_y = ROI['8']['y']

    point9_x = ROI['9']['x']
    point9_y = ROI['9']['y']

    point10_x = ROI['10']['x']
    point10_y = ROI['10']['y']

    point11_x = ROI['11']['x']
    point11_y = ROI['11']['y']

    point12_x = ROI['12']['x']
    point12_y = ROI['12']['y']

    point13_x = ROI['13']['x']
    point13_y = ROI['13']['y']

    point14_x = ROI['14']['x']
    point14_y = ROI['14']['y']

    point15_x = ROI['15']['x']
    point15_y = ROI['15']['y']

    point16_x = ROI['16']['x']
    point16_y = ROI['16']['y']

    point17_x = ROI['17']['x']
    point17_y = ROI['17']['y']

    point18_x = ROI['18']['x']
    point18_y = ROI['18']['y']
 
def read_usb_capture():
    # 选择摄像头的编号
    cap = cv2.VideoCapture(3)
    
    # 设置曝光时间,负值是短
    # cap.set(cv2.CAP_PROP_EXPOSURE, -3.9)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,  3)

    # 设置白平衡
    cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
    
    cap.set(10,-15) #0 亮度
    cap.set(11,70) #50 对比度
    cap.set(12,64) #64 饱和度
    cap.set(13,0) #0 色调
    cap.set(14,74) #64 锐度 图像增益
    
    # 添加这句是可以用鼠标拖动弹出的窗体
    # cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
    frame_num = 0
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read()
        frame_num = frame_num + 1
        # 真实图
        cv2.rectangle(frame,(point1_x-7,point1_y-7),(point1_x + 7,point1_y + 7),(0,255,0))
        cv2.putText(frame, '1', (point1_x-10, point1_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point2_x-7,point2_y-7),(point2_x + 7,point2_y + 7),(0,255,0))
        cv2.putText(frame, '2', (point2_x-10, point2_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point3_x-7,point3_y-7),(point3_x + 7,point3_y + 7),(0,255,0))
        cv2.putText(frame, '3', (point3_x-10, point3_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point4_x-7,point4_y-7),(point4_x + 7,point4_y + 7),(0,255,0))
        cv2.putText(frame, '4', (point4_x-10, point4_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point5_x-7,point5_y-7),(point5_x + 7,point5_y + 7),(0,255,0))
        cv2.putText(frame, '5', (point5_x-10, point5_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point6_x-7,point6_y-7),(point6_x + 7,point6_y + 7),(0,255,0))
        cv2.putText(frame, '6', (point6_x-10, point6_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point7_x-7,point7_y-7),(point7_x + 7,point7_y + 7),(0,255,0))
        cv2.putText(frame, '7', (point7_x-10, point7_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point8_x-7,point8_y-7),(point8_x + 7,point8_y + 7),(0,255,0))
        cv2.putText(frame, '8', (point8_x-10, point8_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point9_x-7,point9_y-7),(point9_x + 7,point9_y + 7),(0,255,0))
        cv2.putText(frame, '9', (point9_x-10, point9_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point10_x-7,point10_y-7),(point10_x + 7,point10_y + 7),(0,255,0))
        cv2.putText(frame, '10', (point10_x-15, point10_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point11_x-7,point11_y-7),(point11_x + 7,point11_y + 7),(0,255,0))
        cv2.putText(frame, '11', (point11_x-15, point11_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point12_x-7,point12_y-7),(point12_x + 7,point12_y + 7),(0,255,0))
        cv2.putText(frame, '12', (point12_x-15, point12_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point13_x-7,point13_y-7),(point13_x + 7,point13_y + 7),(0,255,0))
        cv2.putText(frame, '13', (point13_x-15, point13_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point14_x-7,point14_y-7),(point14_x + 7,point14_y + 7),(0,255,0))
        cv2.putText(frame, '14', (point14_x-15, point14_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point15_x-7,point15_y-7),(point15_x + 7,point15_y + 7),(0,255,0))
        cv2.putText(frame, '15', (point15_x-15, point15_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point16_x-7,point16_y-7),(point16_x + 7,point16_y + 7),(0,255,0))
        cv2.putText(frame, '16', (point16_x-15, point16_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point17_x-7,point17_y-7),(point17_x + 7,point17_y + 7),(0,255,0))
        cv2.putText(frame, '17', (point17_x-15, point17_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.rectangle(frame,(point18_x-7,point18_y-7),(point18_x + 7,point18_y + 7),(0,255,0))
        cv2.putText(frame, '18', (point18_x-15, point18_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        # cv2.imshow('real_img', frame)
        # 按下'q'就退出
        # cv2.waitKey(1)
        if frame_num > 2:
            cv2.imwrite(img_path,frame)
            cap.release()
            cv2.destroyAllWindows()
    return frame

def img2vector(img):
 
    img_arr = np.array(img) 
    img_normlization = img_arr/255 
    img_arr2 = np.reshape(img_normlization, (1,-1)) 
    return img_arr2

def detect_color():
    st = time.perf_counter()
    img = read_usb_capture()
    

    ROI1 = img[point1_y - 5:point1_y + 5, point1_x - 5:point1_x + 5]
    ROI2 = img[point2_y - 5:point2_y + 5, point2_x - 5:point2_x + 5]
    ROI3 = img[point3_y - 5:point3_y + 5, point3_x - 5:point3_x + 5]
    ROI4 = img[point4_y - 5:point4_y + 5, point4_x - 5:point4_x + 5]
    ROI5 = img[point5_y - 5:point5_y + 5, point5_x - 5:point5_x + 5]
    ROI6 = img[point6_y - 5:point6_y + 5, point6_x - 5:point6_x + 5]
    ROI7 = img[point7_y - 5:point7_y + 5, point7_x - 5:point7_x + 5]
    ROI8 = img[point8_y - 5:point8_y + 5, point8_x - 5:point8_x + 5]
    ROI9 = img[point9_y - 5:point9_y + 5, point9_x - 5:point9_x + 5]

    ROI10 = img[point10_y - 5:point10_y + 5, point10_x - 5:point10_x + 5]
    ROI11 = img[point11_y - 5:point11_y + 5, point11_x - 5:point11_x + 5]
    ROI12 = img[point12_y - 5:point12_y + 5, point12_x - 5:point12_x + 5]
    ROI13 = img[point13_y - 5:point13_y + 5, point13_x - 5:point13_x + 5]
    ROI14 = img[point14_y - 5:point14_y + 5, point14_x - 5:point14_x + 5]
    ROI15 = img[point15_y - 5:point15_y + 5, point15_x - 5:point15_x + 5]
    ROI16 = img[point16_y - 5:point16_y + 5, point16_x - 5:point16_x + 5]
    ROI17 = img[point17_y - 5:point17_y + 5, point17_x - 5:point17_x + 5]
    ROI18 = img[point18_y - 5:point18_y + 5, point18_x - 5:point18_x + 5]

    img2arr1 = img2vector(ROI1)
    img2arr2 = img2vector(ROI2)
    img2arr3 = img2vector(ROI3)
    img2arr4 = img2vector(ROI4)
    img2arr5 = img2vector(ROI5)
    img2arr6 = img2vector(ROI6)
    img2arr7 = img2vector(ROI7)
    img2arr8 = img2vector(ROI8)
    img2arr9 = img2vector(ROI9)

    img2arr10 = img2vector(ROI10)
    img2arr11 = img2vector(ROI11)
    img2arr12 = img2vector(ROI12)
    img2arr13 = img2vector(ROI13)
    img2arr14 = img2vector(ROI14)
    img2arr15 = img2vector(ROI15)
    img2arr16 = img2vector(ROI16)
    img2arr17 = img2vector(ROI17)
    img2arr18 = img2vector(ROI18)

    
    preResult1 = clf.predict(img2arr1)
    preResult2 = clf.predict(img2arr2)
    preResult3 = clf.predict(img2arr3)
    preResult4 = clf.predict(img2arr4)
    preResult5 = clf.predict(img2arr5)
    preResult6 = clf.predict(img2arr6)
    preResult7 = clf.predict(img2arr7)
    preResult8 = clf.predict(img2arr8)
    preResult9 = clf.predict(img2arr9)

    preResult10 = clf.predict(img2arr10)
    preResult11 = clf.predict(img2arr11)
    preResult12 = clf.predict(img2arr12)
    preResult13 = clf.predict(img2arr13)
    preResult14 = clf.predict(img2arr14)
    preResult15 = clf.predict(img2arr15)
    preResult16 = clf.predict(img2arr16)
    preResult17 = clf.predict(img2arr17)
    preResult18 = clf.predict(img2arr18)


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
    #read_usb_capture()
    detect_color()