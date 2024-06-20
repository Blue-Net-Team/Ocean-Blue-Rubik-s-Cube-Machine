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
try:
    import communication
except:
    import Vision.communication as communication

sys.path.append("..")

model_path = '/home/lanwang/rubiks-cube-machine/Vision/model/svm_cube_10_10_up2.model'
img_path = '/home/lanwang/rubiks-cube-machine/Vision/pic/U/Ut.png'
clf = joblib.load(model_path) # 加载模型

def process_image(image):
    global point1_x,point1_y,point2_x,point2_y,point3_x,point3_y,point4_x,point4_y,point5_x,point5_y,point6_x,point6_y,point7_x,point7_y,point8_x,point8_y,point9_x,point9_y
    # Find the center coordinates of the frame
    frame_height, frame_width, _ = image.shape
    center_x = frame_width // 2
    center_y = frame_height // 2

    # Set the dimensions of the box
    box_width = 180
    box_height = 180

    # Calculate the coordinates of the top-left and bottom-right corners of the box
    top_left_x = center_x - (box_width // 2)
    top_left_y = center_y - (box_height // 2)
    bottom_right_x = center_x + (box_width // 2)
    bottom_right_y = center_y + (box_height // 2)

    # Draw the box on the image
    # cv2.rectangle(image, (top_left_x - 120, top_left_y-20), (bottom_right_x -120, bottom_right_y-20), (255, 0, 0), 2)
    # cv2.rectangle(image, (top_left_x + 150, top_left_y-20), (bottom_right_x + 150, bottom_right_y-20), (0, 255, 0), 2)
    
    # Crop the image to the region of interest (ROI)
    # Define the coordinates of the two boxes
    box1_top_left_x = top_left_x - 150
    box1_top_left_y = top_left_y
    box1_bottom_right_x = bottom_right_x - 150
    box1_bottom_right_y = bottom_right_y

    box2_top_left_x = top_left_x + 150
    box2_top_left_y = top_left_y
    box2_bottom_right_x = bottom_right_x + 150
    box2_bottom_right_y = bottom_right_y

    # Crop the image to the region of interest (ROI) for box 1
    roi1 = image[box1_top_left_y:box1_bottom_right_y, box1_top_left_x:box1_bottom_right_x]

    # Process the ROI for box 1
    gray_roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
    blurred_roi1 = cv2.GaussianBlur(gray_roi1, (5, 5), 0)
    edges_roi1 = cv2.Canny(blurred_roi1, 50, 150)

    # Find contours in the ROI for box 1
    contours1, _ = cv2.findContours(edges_roi1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diamond_contours1 = []

    for contour in contours1:
        # Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        # Check if it is a diamond shape (4 vertices)
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            if ratio >= 0.5 and ratio <= 1.2 and area > 1000 and area < 30000:
                diamond_contours1.append(contour)

    # Assume the center diamond is the one with the largest area
    max_area1 = 0
    center_diamond1 = None

    for contour in diamond_contours1:
        area = cv2.contourArea(contour)
        if area > max_area1:
            max_area1 = area
            center_diamond1 = contour

    if center_diamond1 is not None:
        # Convert the coordinates of the center box to the original image coordinates
        center_diamond1[:, 0, 0] += box1_top_left_x
        center_diamond1[:, 0, 1] += box1_top_left_y

        # cv2.drawContours(image, [center_diamond1], -1, (0, 255, 0), 2)
        M1 = cv2.moments(center_diamond1)
        cx1 = int(M1['m10']/M1['m00'])
        cy1 = int(M1['m01']/M1['m00'])
        # print(f"Center diamond 1 coordinates: ({cx1}, {cy1})")
        # p2,p8 = (cx1 - 60, cy1), (cx1 + 90, cy1)
        # p4,p6 = (cx1, cy1 - 100), (cx1, cy1 + 100)
        # p3,p7 = (cx1 - 60, cy1 - 100), (cx1 + 90, cy1 + 100)
        # p1,p9 = (cx1 + 90, cy1 - 100), (cx1 - 60, cy1 + 100)
        point1_x,point1_y = (cx1 + 90, cy1 - 100)
        point2_x,point2_y = (cx1 - 60, cy1)
        point3_x,point3_y = (cx1 - 60, cy1 - 100)
        point4_x,point4_y = (cx1, cy1 - 100)
        point5_x,point5_y = (cx1, cy1)
        point6_x,point6_y = (cx1, cy1 + 100)
        point7_x,point7_y = (cx1 + 90, cy1 + 100)
        point8_x,point8_y = (cx1 + 90, cy1)
        point9_x,point9_y = (cx1 - 60, cy1 + 100)

    global point10_x,point10_y,point11_x,point11_y,point12_x,point12_y,point13_x,point13_y,point14_x,point14_y,point15_x,point15_y,point16_x,point16_y,point17_x,point17_y,point18_x,point18_y
    # Crop the image to the region of interest (ROI) for box 2
    roi2 = image[box2_top_left_y:box2_bottom_right_y, box2_top_left_x:box2_bottom_right_x]

    # Process the ROI for box 2
    gray_roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
    blurred_roi2 = cv2.GaussianBlur(gray_roi2, (5, 5), 0)
    edges_roi2 = cv2.Canny(blurred_roi2, 50, 150)

    # Find contours in the ROI for box 2
    contours2, _ = cv2.findContours(edges_roi2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diamond_contours2 = []

    for contour in contours2:
        # Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * peri, True)

        # Check if it is a diamond shape (4 vertices)
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)
            ratio = w / float(h)
            if ratio >= 0.5 and ratio <= 1.2 and area > 1000 and area < 30000:
                diamond_contours2.append(contour)

    # Assume the center diamond is the one with the largest area
    max_area2 = 0
    center_diamond2 = None

    for contour in diamond_contours2:
        area = cv2.contourArea(contour)
        if area > max_area2:
            max_area2 = area
            center_diamond2 = contour

    if center_diamond2 is not None:
        # Convert the coordinates of the center box to the original image coordinates
        center_diamond2[:, 0, 0] += box2_top_left_x
        center_diamond2[:, 0, 1] += box2_top_left_y

        # cv2.drawContours(image, [center_diamond2], -1, (0, 255, 0), 2)
        M2 = cv2.moments(center_diamond2)
        cx2 = int(M2['m10']/M2['m00'])
        cy2 = int(M2['m01']/M2['m00'])
        # print(f"Center diamond 2 coordinates: ({cx2}, {cy2})")
        # 画出中心点
        point10_x,point10_y = (cx2 + 60, cy2 - 100)
        point11_x,point11_y = (cx2 - 60, cy2)
        point12_x,point12_y = (cx2 - 60, cy2 - 100)
        point13_x,point13_y = (cx2, cy2 + 100)
        point14_x,point14_y = (cx2, cy2)
        point15_x,point15_y = (cx2, cy2 - 100)
        point16_x,point16_y = (cx2 + 60, cy2 + 100)
        point17_x,point17_y = (cx2 + 60, cy2)
        point18_x,point18_y = (cx2 - 60, cy2 + 100)
 
def read_usb_capture():
    # ser = communication.UART()
    # 选择摄像头的编号
    cap = cv2.VideoCapture(1)
    
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
    while(cap.isOpened()):
        # 读取摄像头的画面
        ret, frame = cap.read()
        process_image(frame)
        if not (point5_x and point5_y and point14_x and point14_y):
            continue
        # 真实图
        cv2.rectangle(frame,(point1_x-7,point1_y-7),(point1_x + 7,point1_y + 7),(0,255,0))
        cv2.rectangle(frame,(point2_x-7,point2_y-7),(point2_x + 7,point2_y + 7),(0,255,0))
        cv2.rectangle(frame,(point3_x-7,point3_y-7),(point3_x + 7,point3_y + 7),(0,255,0))
        cv2.rectangle(frame,(point4_x-7,point4_y-7),(point4_x + 7,point4_y + 7),(0,255,0))
        cv2.rectangle(frame,(point5_x-7,point5_y-7),(point5_x + 7,point5_y + 7),(0,255,0))
        cv2.rectangle(frame,(point6_x-7,point6_y-7),(point6_x + 7,point6_y + 7),(0,255,0))
        cv2.rectangle(frame,(point7_x-7,point7_y-7),(point7_x + 7,point7_y + 7),(0,255,0))
        cv2.rectangle(frame,(point8_x-7,point8_y-7),(point8_x + 7,point8_y + 7),(0,255,0))
        cv2.rectangle(frame,(point9_x-7,point9_y-7),(point9_x + 7,point9_y + 7),(0,255,0))

        cv2.rectangle(frame,(point10_x-7,point10_y-7),(point10_x + 7,point10_y + 7),(0,255,0))
        cv2.rectangle(frame,(point11_x-7,point11_y-7),(point11_x + 7,point11_y + 7),(0,255,0))
        cv2.rectangle(frame,(point12_x-7,point12_y-7),(point12_x + 7,point12_y + 7),(0,255,0))
        cv2.rectangle(frame,(point13_x-7,point13_y-7),(point13_x + 7,point13_y + 7),(0,255,0))
        cv2.rectangle(frame,(point14_x-7,point14_y-7),(point14_x + 7,point14_y + 7),(0,255,0))
        cv2.rectangle(frame,(point15_x-7,point15_y-7),(point15_x + 7,point15_y + 7),(0,255,0))
        cv2.rectangle(frame,(point16_x-7,point16_y-7),(point16_x + 7,point16_y + 7),(0,255,0))
        cv2.rectangle(frame,(point17_x-7,point17_y-7),(point17_x + 7,point17_y + 7),(0,255,0))
        cv2.rectangle(frame,(point18_x-7,point18_y-7),(point18_x + 7,point18_y + 7),(0,255,0))
        cv2.imshow('real_img', frame)
        # 按下'q'之前阻塞进程
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # ser.write('LC RC')
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
    # plt.imshow(img)
    # plt.show()
    color_state1 = preResult1[0]+preResult2[0]+preResult3[0]+preResult4[0]+preResult5[0]+preResult6[0]+preResult7[0]+preResult8[0]+preResult9[0]
    color_state2 = preResult10[0]+preResult11[0]+preResult12[0]+preResult13[0]+preResult14[0]+preResult15[0]+preResult16[0]+preResult17[0]+preResult18[0]
    return color_state1,color_state2

if __name__ == '__main__':  
    #read_usb_capture()
    detect_color()