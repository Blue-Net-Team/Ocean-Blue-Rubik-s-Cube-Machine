# 更改了一些错误的地方，然后再结合理解进行重新注释，使得整体更利于理解
# 魔方解法库Twophase，平均19步
# 主要还原魔方算法是cube_solver.py   (自己注释与修改过的地方)
# 机械臂动作定义是arm_planning.py

#### 软件架构
系统：ubuntu16.04

python版本：3.8.1


#### 安装教程

1.  SVM识别方案，参考教程：https://blog.csdn.net/lemonbit/article/details/117004167
2.  魔方解算算法，参考教程：https://github.com/hkociemba/RubiksCube-TwophaseSolver
3.  机械臂规划算法，参考教程：https://gitee.com/harry-fan/rubiks-cube-robot/tree/master

#### 使用说明

1.  使用时执行main.py文件即可
2.  vision文件夹中的view.py文件中的参数可根据自己的需求自行修改
3.  model文件夹中存放的是SVM得到的训练模型


