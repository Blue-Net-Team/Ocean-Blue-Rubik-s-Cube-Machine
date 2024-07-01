r"""
*********************************************
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '&lt;  `.___\_&lt;|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='

			   佛祖镇楼 永无BUG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""
import time
from machine import Pin, UART
from machine import I2C
import ssd1306
from arm import SteppingMotor, ClampCylinder


def restore():
    """还原
    ----
    收到信号触发"""
    for index, now_step in enumerate(str_data_lst):
        if len(now_step) != 2:
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return
        oled.fill(0)
        oled.text(f'{now_step}', 0, 10)
        oled.show()
        print(now_step)
        sign1 = now_step[0]        # L or R
        sign2 = now_step[1]        # ["1", "2", "3", "O", "C"]
        try:
            next_step = str_data_lst[index+1]
        except IndexError:
            next_step = [None, None]

        if next_step[0]!=sign1:     # 下一步在不同手臂
            # t1:手指张和后的延迟
            # t2:手腕旋转后的延迟
            t1=0.1
            t2=0.225
            if next_step[1] in ['1', '2', '3'] and now_step[1] in ['O']:        # [LO,R1,LC]
                t1=0.07
            if now_step[1] in ['1', '2', '3'] and next_step[1] in ['C']:
                t2=0.25
        else:
            t1=0.16
            t2=0.23

        if sign1 == "L":
            motor = left_motor
            cylinder = left_cylinder
            
        elif sign1 == "R":
            motor = right_motor
            cylinder = right_cylinder

        else:
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return

        if sign2 in ["O", "C"]:
            if sign2 == 'O':
                cylinder.open()
            if sign2 == "C":
                cylinder.close()
            time.sleep(t1)        # 0.15可用 5个压    0.1 6个压测试
        elif sign2 in ['1','2','3']:
            if sign2 in ["1", "3"]:
                motor.rotate(sign2, 0)     # 5
            elif sign2 == "2":
                motor.rotate(sign2, 0)      # 5
            time.sleep(t2)
        else:
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return
        # input()
        

def read(ser:UART, HEAD:str='@', TAIL:str='#') -> bytes:
    PACKET_HEAD = HEAD.encode('ASCII')
    PACKET_TAIL = TAIL.encode('ASCII')

    data = b''  # 用于存储接收到的数据

    while True:
        byte = ser.read(1)
        if byte == b'' or byte is None:
            continue
        if byte == PACKET_HEAD:
            data = b''
            continue
        if byte == PACKET_TAIL:
            break
        data += byte
    return data

if __name__ == "__main__":
    # region 创建对象
    left_cylinder = ClampCylinder(11)
    right_cylinder = ClampCylinder(12)
    print("Cylinder created")

    gas_switch = Pin(41, Pin.OUT)
    print("Gas switch created")

    led = Pin(9, Pin.OUT)
    print("LED created")

    IIC = I2C(0, scl=Pin(5), sda=Pin(4))
    print("IIC created")

    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, IIC)
    print("OLED created")
    # endregion 

    while True:
        # 与Jetson Nano通信的串口对象
        uart = UART(1, baudrate=9600, tx=8, rx=7)       # type: ignore
        # region 读取数据
        data = read(uart)
        str_data = data.decode()
        str_data_lst = str_data.split(' ')
        # endregion
        # print(str_data_lst)
        del uart
        print('uart release')

        left_motor = SteppingMotor(stp=47, en=48, _dir=38)
        right_motor = SteppingMotor(stp=40, en=39, _dir=21)
        print("Motor created")

        print(str_data_lst)

        t0 = time.time()        # 计时开始
        oled.fill(0)            # 清屏

        gas_switch.value(1)     # 打开气源
        oled.text(f'{len(str_data_lst)} steps', 0, 0)
        led.on()        # 就绪指示灯亮起
        restore()       # 还原
        led.off()       # 就绪指示灯熄灭

        t1 = time.time()        # 计时结束
        oled.fill(0)            # 清屏
        oled.text(f'Finish in', 0, 0)        # 显示时间
        oled.text(f'{t1-t0}', 0, 10)
        oled.text(f'seconds', 0, 20)
        oled.show()        # 刷新屏幕

        # 打开两个手指
        left_cylinder.open()
        right_cylinder.open()

        # 关闭气源
        gas_switch.value(0)

        time.sleep(1)       # 等待1s

        # 关闭两个手指
        left_cylinder.close()
        right_cylinder.close()

        del left_motor
        del right_motor
        print("Motor release")
