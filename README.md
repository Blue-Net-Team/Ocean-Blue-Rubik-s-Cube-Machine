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

NVIDIA jetson nano
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
- ESP32-S3R8N8
- 4个摄像头
- [42步进电机-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [闭环控制器Emm42工业版](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D夹爪气缸](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [气滑环 2路气 侧边出气M5牙](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744)*2
- 若干 气管连接头

## 说明

作为上位机的jetson nano会使用svm识别魔方的各色块颜色，得出魔方当前姿态，然后使用魔方解算算法得出还原步骤，但是还原步骤并不能直接传给下位机操控两个机械臂，要对还原步骤进行最短路径计算，得出最短的机械步骤，将机械步骤发送给下位机的ESP32，ESP32会控制步进电机和气缸，完成魔方的还原。
