import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class SteppingMotor:
    """步进电机"""
    def __init__(self, step_pin, dir_pin, en_pin):
        """步进电机的初始化
        ----
        * step_pin: 步进电机的步进引脚，提供脉冲信号
        * dir_pin: 步进电机的方向引脚，提供方向信号
        * en_pin: 步进电机的使能引脚，可选，默认为None"""
        self.step = step_pin
        self.dir = dir_pin
        self.en = en_pin
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.output(self.dir, GPIO.HIGH)
        GPIO.output(self.en, GPIO.HIGH)

    def move(self, cycle, reverse=False):
        """步进电机转动
        ----
        * cycle: 转动的圈数
        * reverse: 是否反向转动，默认为False(正向转动)"""
        if reverse:
            GPIO.output(self.dir, GPIO.LOW)
        steps = int(cycle*3200)
        for i in range(steps):
            GPIO.output(self.step, GPIO.HIGH)
            for i in range(50):
                pass
            GPIO.output(self.step, GPIO.LOW)
            for i in range(50):
                pass
  

class ClampCylinder:
    """气缸夹爪"""
    def __init__(self, Pin) -> None:
        """气缸夹爪的初始化
        ----
        * Pin: 气缸夹爪的控制引脚，输出高电平时夹爪闭合"""
        self.pin = Pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def close(self):
        """气缸夹爪闭合"""
        GPIO.output(self.pin, GPIO.HIGH)

    def open(self):
        """气缸夹爪张开"""
        GPIO.output(self.pin, GPIO.LOW)


class Arm:
    """机械臂"""
    def __init__(self, clamp:ClampCylinder, motor:SteppingMotor) -> None:
        """机械臂的初始化
        ----
        * clamp: 手臂的夹爪
        * motor: 步进电机"""
        self.clamp:ClampCylinder = clamp
        self.motor:SteppingMotor = motor

    def close_spin(self, num:int|float, reverse=False):
        """机械臂闭合并旋转 -> 转动魔方
        ----
        * num: 旋转的圈数
        * reverse: 是否反向旋转，默认为False(顺时旋转)"""
        self.clamp.close()
        self.motor.move(num, reverse)

    def open_spin(self, num:int|float, reverse=False):
        """机械臂张开并旋转 -> 手指归位
        ----
        * num: 旋转的圈数
        * reverse: 是否反向旋转，默认为False(顺时旋转)"""
        self.clamp.open()
        self.motor.move(num, reverse)

    def open(self):
        """手指张开"""
        self.clamp.open()


class CubeSolution:
    """魔方解法
    ----
    魔方结构定义：
          _______
          |  0  |
    ______|__U__|___________
    |  2  |  4  |  3  |  5  |
    |__L__|__F__|__R__|__B__|
          |  1  |
          |__D__|
    
    机械臂抓持D,R
    """
    def __init__(self, left_arm:Arm, right_arm:Arm) -> None:
        self.left_arm = left_arm
        self.right_arm = right_arm

        self.cube_dict = {0: 'U', 1: 'D', 2: 'L', 3: 'R', 4: 'F', 5: 'B'}
        self.cube = [0, 2, 4, 3, 5, 1]      # 左机械臂抓持self.cube[5], 右机械臂抓持self.cube[3]

    def r_slip(self, num:int, reverse=False) -> list:
        """右侧空转
        ----
        右侧手指闭合，左侧手张开，带动魔方空转
        * num: 旋转的面数
        * reverse: 是否反向旋转，默认为False(顺时旋转)"""
        def _swap(a, b):
            a, b = b, a
        if num != 1 and num != 2:       # 旋转面数只能为1或2
            raise ValueError('num must be 1 or 2')
        self.left_arm.open()            # 左手指张开
        for i in range(num):
            self.right_arm.close_spin(num/4, reverse=reverse)

            # region 更新魔方结构的列表
            if reverse:             # 逆时针旋转
                _swap(self.cube[4], self.cube[5])
                _swap(self.cube[2], self.cube[5])
                _swap(self.cube[0], self.cube[2])
            else:                   # 顺时针旋转
                _swap(self.cube[2], self.cube[5])
                _swap(self.cube[0], self.cube[5])
                _swap(self.cube[4], self.cube[5])
            # endregion
                
        return self.cube


if __name__ == '__main__':
    motor = SteppingMotor(27, 22, 17)
    motor.move(1)