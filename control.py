import RPi.GPIO as GPIO
import time

class SteppingMotor:
    """步进电机"""
    def __init__(self, step_pin, dir_pin, en_pin=None):
        """步进电机的初始化
        ----
        * step_pin: 步进电机的步进引脚，提供脉冲信号
        * dir_pin: 步进电机的方向引脚，提供方向信号
        * en_pin: 步进电机的使能引脚，可选，默认为None"""
        self.step = step_pin
        self.dir = dir_pin
        self.en = en_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.output(self.step, GPIO.LOW)
        GPIO.output(self.dir, GPIO.LOW)

    def move(self, angle, reverse=False):
        """步进电机转动
        ----
        * angle: 转动的角度
        * reverse: 是否反向转动，默认为False(正向转动)"""
        if reverse:
            GPIO.output(self.dir, GPIO.HIGH)
        steps = int(angle/1.8)
        for i in range(steps):
            GPIO.output(self.step, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.step, GPIO.LOW)
            time.sleep(0.001)