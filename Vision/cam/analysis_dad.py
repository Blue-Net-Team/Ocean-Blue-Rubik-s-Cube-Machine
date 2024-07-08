import json
import cv2
import joblib
import numpy as np

class Cam:
    def __init__(self, jsonpath:str, model_path:str) -> None:
        """
        摄像头父类初始化
        ----
        * jsonpath: ROI的json文件路径
        * model_path: svm模型文件路径
        """
        d_nums = {'D':18,
                  'U':18,
                  'L':9,
                  'R':9
                  }
        d_capid = {'L':0,
                   'U':1,
                   'R':2,
                   'D':3
                   }
        self.nums = d_nums[jsonpath.split('/')[-1][0]]
        self.capid = d_capid[jsonpath.split('/')[-1][0]]
        self.cap = cv2.VideoCapture(self.capid)
        self.clf = joblib.load(model_path) # 加载模
        
        # 从json文件中读取ROI信息
        with open(jsonpath, 'r') as f:
            self.ROI = json.load(f)

    def img2vector(self, img:cv2.typing.MatLike) -> np.ndarray:
        """
        将图像归一化并且转换为一维数组
        """
        img_arr = np.array(img) 
        img_normlization = img_arr/255      # type: ignore
        img_arr2 = np.reshape(img_normlization, (1,-1)) 
        return img_arr2
    
    def read_usb_capture(self):
        """
        读取摄像头图像，进行ROI的标记
        ----
        * 返回值 frame: 读取的图像
        * 返回值 img: 画了ROI的图像
        """
        while True:
            # 读取摄像头的画面
            ret, frame = self.cap.read()

            if not ret:
                continue

            img = frame.copy()

            img = cv2.medianBlur(img, 5)

            # region 画框
            for i in range(self.nums):
                cv2.rectangle(img,(self.ROI[str(i+1)]['x']-7,self.ROI[str(i+1)]['y']-7),(self.ROI[str(i+1)]['x'] + 7,self.ROI[str(i+1)]['y'] + 7),(0,255,0))
                cv2.putText(img, str(i+1), (self.ROI[str(i+1)]['x']-10, self.ROI[str(i+1)]['y']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            # endregion
                
            self.cap.release()
            cv2.destroyAllWindows()
            break
        return frame, img
    
    def detect_color(self, img:cv2.typing.MatLike) -> list:
        """
        使用svm模型检测颜色
        ----
        * img: 输入图像
        * 返回值 results: 检测结果
        """
        ROI_lst = []
        for i in range(self.nums):
            ROI_lst.append(img[self.ROI[str(i+1)]['y'] - 5:self.ROI[str(i+1)]['y'] + 5, self.ROI[str(i+1)]['x'] - 5:self.ROI[str(i+1)]['x'] + 5])
        img2arr_list = list(map(self.img2vector, 
                                ROI_lst))

        results = list(map(self.clf.predict, img2arr_list))
        return results