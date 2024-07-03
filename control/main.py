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
        if len(now_step) != 2:      # 确认步骤合法
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return
        oled.fill(0)                        # 清屏
        oled.text(f'{now_step}', 0, 10)     # 显示当前步骤
        oled.show()                         # 显示

        sign1 = now_step[0]        # L or R
        sign2 = now_step[1]        # ["1", "2", "3", "O", "C"]
        
        # 确认下一步
        try:
            next1_step = str_data_lst[index+1]
            try:
                next2_step = str_data_lst[index+2]
            except IndexError:
                next2_step = [None, None]
        except IndexError:
            next1_step = [None, None]

        # 调整延迟
        if next1_step[0]!=sign1:     # 下一步在不同手臂
            # t1:手指张和后的延迟
            # t2:手腕旋转后的延迟
            t1=0.1
            t2=0.2
            if next1_step[1] in ['1', '2', '3'] and now_step[1] in ['O']:        # [LO,R1,LC]
                t1=0.07
            if now_step[1] in ['1', '2', '3'] and next1_step[1] in ['C']:
                t2=0.24
        else:
            t1=0.13
            t2=0.23
        
        # 确认左右手
        if sign1 == "L":
            motor = left_motor
            cylinder = left_cylinder
            _cylinder = right_cylinder
        elif sign1 == "R":
            motor = right_motor
            cylinder = right_cylinder
            _cylinder = left_cylinder
        else:
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return

        # 选择动作
        if sign2 == 'O' and index == len(str_data_lst)-3:                # 这一步是张手指并且是倒数第三步
            if next1_step[0] == sign1:      # 下一步在同一手臂
                if next1_step[1] in ['1','3'] and next2_step[1] in ['C']:
                    cylinder.open()
                    _cylinder.open()
                    time.sleep(1)
                    motor.rotate('1', 0)
                    break
        elif sign2 in ["O", "C"]:
            if sign2 == 'O':
                cylinder.open()
            if sign2 == "C":
                cylinder.close()
            time.sleep(t1)
        elif sign2 in ['1','2','3']:
            if sign2 in ["1", "3"]:
                motor.rotate(sign2, 0)
            elif sign2 == "2":
                motor.rotate(sign2, 0)
            time.sleep(t2)
        else:
            oled.fill(0)
            oled.text("Invalid step", 0, 0)
            oled.show()
            print("Invalid step")
            return
        

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
