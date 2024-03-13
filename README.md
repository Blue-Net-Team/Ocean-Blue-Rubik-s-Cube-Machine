# 海蓝魔方机
针对2024年的智能机器人创意大赛的主题2，还原魔方的机器人，追求更快的速度。

## 开发团队
 - 院校：广东海洋大学
 - 所属学院：机械工程学院
 - 团队名称：蓝网科技创新团队
 - 队伍成员：
    - 视觉：许凯杰，何云峰
    - 算法：许凯杰
    - 电控：何云峰
    - 结构：吉泧均，何云峰

## 开发平台
树莓派4B

## 开发环境
 - 操作系统：Raspbian
 - 开发语言：Python

## 参考
1.  SVM识别方案，参考教程：https://blog.csdn.net/lemonbit/article/details/117004167
2.  魔方解算算法，参考教程：https://github.com/hkociemba/RubiksCube-TwophaseSolver
3.  机械臂规划算法，参考教程：https://gitee.com/harry-fan/rubiks-cube-robot/tree/master

## 介绍
本魔方机器人采用双爪八字布局，4个摄像头，两个步进电机，气滑环，以及夹爪气缸。通过空压机给气罐充气，撤除空压机，将魔方放在托架后，按下启动按钮，夹爪闭合，开始还原魔方。
### 设备清单
- 树莓派4B
- 4个摄像头
- [42步进电机-L40](https://item.taobao.com/item.htm?abbucket=5&id=682797640293&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5057239338765) + [闭环控制器Emm42工业版](https://item.taobao.com/item.htm?abbucket=5&id=673302946671&ns=1&spm=a21n57.1.0.0.6903523cZRZY1D&skuId=5032954871240) *2
- [MHL2-16D夹爪气缸](https://item.taobao.com/item.htm?id=537049565191&spm=a1z0d.6639537/tb.1997196601.34.257c7484ZwafTI&skuId=3206052770907) *2
- [气滑环 2路气 侧边出气M5牙](https://detail.tmall.com/item.htm?_u=d2qf50kdb8b2&id=555594152568&skuId=3431370232744)*2
- 若干 气管连接头