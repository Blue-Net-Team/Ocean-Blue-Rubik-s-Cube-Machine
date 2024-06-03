#!/usr/bin/python3.8
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:

    sys.path.remove(ros_path)

import cv2

import numpy as np
import joblib
import matplotlib.pyplot as plt
import time

# XXX: 路径可能需要修改
model_path = '/home/lt/mofang/model/svm_cube_10*10_right4.model'
img_path = '/home/lt/mofang/view3/test.jpg'
clf = joblib.load(model_path) # 加载模型

point1_x = 174
point1_y = 234
point2_x = 242
point2_y = 156
point3_x = 320
point3_y = 88
point4_x = 255
point4_y = 300
point5_x = 323
point5_y = 228
point6_x = 395
point6_y = 163
point7_x = 324
point7_y = 386
point8_x = 392
point8_y = 300
point9_x = 469
point9_y = 234

def read_usb_capture():
    # 选择摄像头的编号
    cap = cv2.VideoCapture(2)
    cap.set(10,-30) #0
    cap.set(11,20) #50
    cap.set(12,64) #64
    cap.set(13,-15) #0
    cap.set(14,64) #64
    # 添加这句是可以用鼠标拖动弹出的窗体
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
    frame_num = 0
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read()
        frame_num = frame_num + 1
        # 真实图
        cv2.rectangle(frame,(point1_x - 7,point1_y - 7),(point1_x + 7,point1_y + 7),(0,105,0))
        cv2.rectangle(frame,(point2_x - 7,point2_y - 7),(point2_x + 7,point2_y + 7),(0,105,0))
        cv2.rectangle(frame,(point3_x - 7,point3_y - 7),(point3_x + 7,point3_y + 7),(0,105,0))
        cv2.rectangle(frame,(point4_x - 7,point4_y - 7),(point4_x + 7,point4_y + 7),(0,105,0))
        cv2.rectangle(frame,(point5_x - 7,point5_y - 7),(point5_x + 7,point5_y + 7),(0,105,0))
        cv2.rectangle(frame,(point6_x - 7,point6_y - 7),(point6_x + 7,point6_y + 7),(0,105,0))
        cv2.rectangle(frame,(point7_x - 7,point7_y - 7),(point7_x + 7,point7_y + 7),(0,105,0))
        cv2.rectangle(frame,(point8_x - 7,point8_y - 7),(point8_x + 7,point8_y + 7),(0,105,0))
        cv2.rectangle(frame,(point9_x - 7,point9_y - 7),(point9_x + 7,point9_y + 7),(0,105,0))
        cv2.imshow('real_img', frame)
        # 按下'q'就退出
        cv2.waitKey(1)
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

    img2arr1 = img2vector(ROI1)
    img2arr2 = img2vector(ROI2)
    img2arr3 = img2vector(ROI3)
    img2arr4 = img2vector(ROI4)
    img2arr5 = img2vector(ROI5)
    img2arr6 = img2vector(ROI6)
    img2arr7 = img2vector(ROI7)
    img2arr8 = img2vector(ROI8)
    img2arr9 = img2vector(ROI9)


    preResult1 = clf.predict(img2arr1)
    preResult2 = clf.predict(img2arr2)
    preResult3 = clf.predict(img2arr3)
    preResult4 = clf.predict(img2arr4)
    preResult5 = clf.predict(img2arr5)
    preResult6 = clf.predict(img2arr6)
    preResult7 = clf.predict(img2arr7)
    preResult8 = clf.predict(img2arr8)
    preResult9 = clf.predict(img2arr9)

    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    print(preResult1,preResult2,preResult3)
    print(preResult4,preResult5,preResult6)
    print(preResult7,preResult8,preResult9)
 
    et = time.perf_counter()
    print("spent {:.4f}s.".format((et - st)))
    # plt.subplot(3,3,1)
    # plt.imshow(ROI1)
    # plt.subplot(3,3,2)
    # plt.imshow(ROI2)
    # plt.subplot(3,3,3)
    # plt.imshow(ROI3)
    # plt.subplot(3,3,4)
    # plt.imshow(ROI4)
    # plt.subplot(3,3,5)
    # plt.imshow(ROI5)
    # plt.subplot(3,3,6)
    # plt.imshow(ROI6)
    # plt.subplot(3,3,7)
    # plt.imshow(ROI7)
    # plt.subplot(3,3,8)
    # plt.imshow(ROI8)
    # plt.subplot(3,3,9)
    # plt.imshow(ROI9)
    # plt.imshow(img)
    # plt.show()
    color_state = preResult1[0]+preResult2[0]+preResult3[0]+preResult4[0]+preResult5[0]+preResult6[0]+preResult7[0]+preResult8[0]+preResult9[0]
    return color_state

if __name__ == '__main__':  
    #read_usb_capture()
    detect_color()