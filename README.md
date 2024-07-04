# 海蓝魔方机

针对2024年的[中国高校智能机器人创意大赛](https://www.robotcontest.cn/datacenter/news/detail?id=6292)的主题2，还原魔方的机器人，追求更快的速度。

**本项目为2024年中国高校智能机器人创意大赛的参赛作品，仅供学习交流使用，不得用于商业用途。**

## 开发团队

- 院校：广东海洋大学
- 所属学院：机械工程学院
- 团队名称：[蓝网科技创新团队](https://gitee.com/blue-net-vision)
- 队伍成员：
  - 视觉：[许凯杰](https://gitee.com/d-vision)，[何云峰](https://gitee.com/iven_he)
  - 算法：[许凯杰](https://gitee.com/d-vision)
  - 电控：[何云峰](https://gitee.com/iven_he)
  - 结构：吉泧均，何云峰

## 开发平台

- NVIDIA jetson nano
- ESP32-S3R8N8

## 开发环境

- 操作系统：Ubuntu
- 开发语言：Python

## 参考

1. [SVM识别方案](https://blog.csdn.net/lemonbit/article/details/117004167)
2. [魔方解算算法](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
3. [机械臂规划算法](https://gitee.com/harry-fan/rubiks-cube-robot)

## 介绍

本魔方机器人采用双爪八字布局，4个摄像头，两个步进电机，气滑环，以及夹爪气缸。通过空压机给气罐充气，撤除空压机，将魔方夹稳，按下启动按钮，夹爪闭合，开始还原魔方。

### 设备清单

- NVIDIA jetson nano
- [ESP32-S3R8N8](https://item.szlcsc.com/22034693.html?fromZone=s)
- 4个摄像头
- [42步进电机-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [闭环控制器Emm42工业版](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D夹爪气缸](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [气滑环 2路气 侧边出气M5牙](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744)*2
- [二路五通电磁阀](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=631999517519&_u=42qf50kd72cc)*2
- [200M 2F汇流排](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=682537654244&_u=42qf50kd02df)
- [200M堵头3个和消音器2只](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=682537654244&_u=42qf50kd02df)
- [12v锂电池](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.2e4a2e8dQz8SzG&id=632184698346&_u=42qf50kd578b)
- 若干 6mm气管连接头

## 说明

作为上位机的jetson nano会使用svm识别魔方的各色块颜色，得出魔方当前姿态，然后使用魔方解算算法得出还原步骤，但是还原步骤并不能直接传给下位机操控两个机械臂，要对还原步骤进行最短路径计算，得出最短的机械步骤，将机械步骤发送给下位机的ESP32，ESP32会控制步进电机和气缸，完成魔方的还原。\
此机器框架使用30铝型材，全金属框架，**电路板需要注意防止短路**

### 使用说明

本项目主要使用难点在于视觉方面，一下回主要介绍Jetson nano的连接和程序启动，调试等部分

#### 连接

首先将jetson nano开机，使用vscode的远程连接功能连接Jetson nano。对于首次使用Jetson nano，需要使用外接显示屏来连接WiFi，确认IP地址等操作。此后的连接方式与树莓派一致。

#### 魔方摆放

此视觉识别方案中，对魔方的摆放可能有要求，**目前没有测试其他的摆放方式是否可以完成还原**。

摄像头的示例图片位于路径 **./Vision/pic** 中，摄像头对应的识别文件 **./Vision/cam** 中。\
在图片中，上侧摄像头的左侧就是左机械臂所在一侧，以此一来：

- **蓝色面**在右手机械臂的上方
- **橙色面**位于机器前方，即人面向机器时左手对应左机械臂时人所在机器的位置
- 以此类推

#### ROI区域调试

本项目使用vscode进行调试，不依赖外部显示器，所以不能在代码中使用OpenCV有关qt窗口的函数，为了解决快速调试的需求，我们使用远程图传用于调试ROI区域。

- 我们在*Vision*文件夹中编写了*ROIlocater.py*文件，用于快速调整摄像头对各个色块的ROI区域\
- 我们在*Vision*文件夹中同样编写了Jetson nano 上运行的远程图传文件*Captest.py*，文件的运行需要使用命令行传参，使用*Python Debugger*进行调试的时候需要选择**带有参数的Python文件**，在交互框中协商对应的参数名和参数\
`--cap 1` 此参数的意义是使用摄像头id为`1`的摄像头进行远程图传。\
或者直接在命令行直接用Python命令运行Python文件\

  ```bash
  python Captest.py --cap 1
  ```

启动*ROIlocater.py*文件前需要修改222行的参数`serface_name`，改为需要修改的对应的摄像头的位置，例如

- 上摄像头：U
- 下摄像头：D
- 左摄像头：L
- 右摄像头：R

**先启动Jetson nano上的远程图传服务器程序，再启动对端的*ROIlocater.py*文件**

两个文件都启动后会弹出滑块窗口用于调整滑块的位置、大小和编号。调整前需要查看事例图片上的编号顺序，ROI的顺序不能出错。ROI的编号对应的是滑块*ID*的值，**ID为0的时候是无效ROI**

示例图片位于文件夹 **./Vision/pic** 中。

对应示例的图片**随机应变**，按照ROI顺序依次点击识别区域，此操作尽可能需要在步进电机通电的情况进行，这样可以保证电机的角度基本不变。使用鼠标单击完成ROI设置后就可以直接结束程序。在滑块窗口中有*OK*标签的滑块充当保存按钮，使用鼠标单击的模式可以直接忽略这个滑块，但是如果是使用滑块来调节ROI位置的需要将*OK*标签滑到1进行保存在回到0复位。

完成ROI设置后，将工作目录中的对应json文件复制到Jetson nano 的工作目录中，替换原有的json文件就可以完成ROI的设置。

#### 识别调试

在本项目中，调整好ROI区域后大部分报错是由颜色识别出错导致，运行*main.py*文件可以直接查看各个摄像头的识别结果，识别的图片会保存在 **./Vision/pic** 文件夹下以摄像头位置命名。依据图片和结果一一对比，查出识别出错的摄像头，在对应的摄像头文件中(位于文件夹 **./Vision/cam** 中)修改亮度,大部分是识别问题都可以通过修改亮度来解决。

```python
# 自动曝光
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

cap.set(10,0) # 亮度0
```

经过测试，自动曝光参数`3`效果最佳

## 开发说明

- **Vision**文件夹用于存储视觉识别以及魔方解算的代码
- **Control**文件夹用于存储电控代码，是一个microPython工程文件夹，在*vscode*中安装*RT-Thread MicroPython*插件，在此文件夹创建microPython工程，即可连接到ESP32，进行代码编写，但是请确保esp32的固件已经烧录
  - 在[microPython官网](https://micropython.org/)下载esp32的固件
  - 使用esptool或者[Thonny](https://micropython.org/)烧录固件
- **Structure**文件夹用于存储机械结构相关模型，使用*SolidWorks2023*打开
- **PCB**文件夹用于存储电路板设计文件，使用*嘉立创EDA专业版*打开

# 最后说明

此仓库中的Raspberry Pi分支是原来只使用树莓派进行开发的版本，现在已经废弃，不再维护，如果有相关需求或者想法可以加入我们。
