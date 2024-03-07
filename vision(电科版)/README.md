### 更改了一些错误的地方，然后再结合理解进行重新注释，使得整体更利于理解
### 魔方解法库Twophase，平均19步
### 主要还原魔方算法是cube_solver.py   (主要算法注释与修改过的地方)
### 机械臂动作定义是arm_planning.py    

#### 与练洪还原算法一样，优化点都是在对执行对L面或R面转动时候选择用左手还是右手，练洪是根据检测当前哪只手处于close
#### 状态来进行选择，而电科采取了递归两种情况来进行抉择，时间复杂度可能为2的n次方(不确定)，感觉各有优点


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


