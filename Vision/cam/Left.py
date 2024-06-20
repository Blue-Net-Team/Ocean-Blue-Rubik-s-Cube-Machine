#!/usr/bin/python3.8
import sys
ros_path = '/opt/ros/kinetic/lib/python2.7/dist-packages'

if ros_path in sys.path:

    sys.path.remove(ros_path)

import cv2

import numpy as np
import joblib
# import matplotlib.pyplot as plt
import time

model_path = 'model/svm_cube_10_10_left4.model'
img_path = 'pic/L/L.png'
clf = joblib.load(model_path) # 加载模型

def process_image(image):
    global point1_x,point1_y,point2_x,point2_y,point3_x,point3_y,point4_x,point4_y,point5_x,point5_y,point6_x,point6_y,point7_x,point7_y,point8_x,point8_y,point9_x,point9_y
    # Find the center coordinates of the frame
    frame_height, frame_width, _ = image.shape
    center_x = frame_width // 2
    center_y = frame_height // 2

    # Set the dimensions of the box
    box_width = 300
    box_height = 300

    # Calculate the coordinates of the top-left and bottom-right corners of the box
    top_left_x = center_x - (box_width // 2)
    top_left_y = center_y - (box_height // 2)
    bottom_right_x = center_x + (box_width // 2)
    bottom_right_y = center_y + (box_height // 2)

    # Draw the box on the image
    # cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255, 0, 0), 2)

    # Crop the image to the region of interest (ROI)
    roi = image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

    # Process the ROI
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    edges_roi = cv2.Canny(blurred_roi, 50, 150)

    # Find contours in the ROI
    contours, _ = cv2.findContours(edges_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diamond_contours = []

    for contour in contours:
        # 近似轮廓
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        # 检查是否为菱形（4个顶点）
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            if ratio >= 0.9 and ratio <= 1.2 and area > 10000 and area < 30000:
                diamond_contours.append(contour)

    # 假设中心菱形块是面积最大的菱形
    max_area = 0
    center_diamond = None
    print(len(diamond_contours))
    for contour in diamond_contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            center_diamond = contour

    if center_diamond is not None:
        # 将中心块框的坐标转换为原始图像的坐标
        center_diamond[:, 0, 0] += top_left_x
        center_diamond[:, 0, 1] += top_left_y

        # cv2.drawContours(image, [center_diamond], -1, (0, 255, 0), 2)
        M = cv2.moments(center_diamond)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        print(f"Center diamond coordinates: ({cx}, {cy})")
        point1_x = cx
        point1_y = cy - 200
        point2_x = cx + 100
        point2_y = cy - 100
        point3_x = cx + 200
        point3_y = cy
        point4_x = cx - 100
        point4_y = cy - 100
        point5_x = cx
        point5_y = cy
        point6_x = cx + 94
        point6_y = cy + 94
        point7_x = cx - 200
        point7_y = cy
        point8_x = cx - 94
        point8_y = cy + 94
        point9_x = cx
        point9_y = cy + 200

def read_usb_capture():
    # 选择摄像头的编号
    cap = cv2.VideoCapture(2)
    
    # 设置曝光时间,负值是短
    cap.set(cv2.CAP_PROP_EXPOSURE, -3.9)

    # 设置白平衡
    cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
    
    cap.set(10,-40) #0 亮度
    cap.set(11,50) #50 对比度
    cap.set(12,64) #64 饱和度
    cap.set(13,0) #0 色调
    cap.set(14,70) #64 锐度 图像增益
    
    # 添加这句是可以用鼠标拖动弹出的窗体
    # cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)
    frame_num = 0
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read()
        process_image(frame)
        if not (point5_x and point5_y):
            continue
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