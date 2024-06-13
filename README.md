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

NVIDIA jetson nano\
ESP32-S3R8N8

## 开发环境

- 操作系统：Ubuntu
- 开发语言：Python

## 参考

1. [SVM识别方案](https://blog.csdn.net/lemonbit/article/details/117004167)
2. [魔方解算算法](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
3. [机械臂规划算法](https://gitee.com/harry-fan/rubiks-cube-robot/tree/master)

## 介绍

本魔方机器人采用双爪八字布局，4个摄像头，两个步进电机，气滑环，以及夹爪气缸。通过空压机给气罐充气，撤除空压机，将魔方夹稳，按下启动按钮，夹爪闭合，开始还原魔方。

### 设备清单

- NVIDIA jetson nano
- [ESP32-S3R8N8](https://item.szlcsc.com/22034693.html?fromZone=s)
- 4个摄像头
- [42步进电机-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [闭环控制器Emm42工业版](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D夹爪气缸](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [气滑环 2路气 侧边出气M5牙](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744)*2
- 若干 6mm气管连接头

## 说明

作为上位机的jetson nano会使用svm识别魔方的各色块颜色，得出魔方当前姿态，然后使用魔方解算算法得出还原步骤，但是还原步骤并不能直接传给下位机操控两个机械臂，要对还原步骤进行最短路径计算，得出最短的机械步骤，将机械步骤发送给下位机的ESP32，ESP32会控制步进电机和气缸，完成魔方的还原。\
此机器框架使用30铝型材，全金属框架，**电路板需要注意防止短路**

### 使用说明

首先将jetson nano开机，jetsonnano会引出两个引脚连接LED灯，系统开机后运行程序会点亮此LED，指示程序已经开始运行，此时jetson会等待ESP传输就绪信号，然后开始识别魔方姿态。

ESP32开机后按下PCB上的SW1按钮，触发外部中断，ESP32会发送就绪信号给jetson nano，然后等待jetson nano传输还原步骤，ESP32会根据步骤控制步进电机和气缸，完成魔方还原的机械步骤，收到信号后会立即开始还原魔方

## 开发说明

- **Vision**文件夹用于存储视觉识别以及魔方解算的代码
- **Control**文件夹用于存储电控代码，是一个microPython工程文件夹，在*vscode*中安装*RT-Thread MicroPython*插件，在此文件夹创建microPython工程，即可连接到ESP32，进行代码编写，但是请确保esp32的固件已经烧录
  - 在[microPython官网](https://micropython.org/)下载esp32的固件
  - 使用esptool或者[Thonny](https://micropython.org/)烧录固件
- **Structure**文件夹用于存储机械结构相关模型，使用*SolidWorks2023*打开
- **PCB**文件夹用于存储电路板设计文件，使用*嘉立创EDA专业版*打开
