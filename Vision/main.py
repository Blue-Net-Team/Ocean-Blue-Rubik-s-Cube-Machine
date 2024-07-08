import cube_solver
import time
import communication
import arm_planning
import cam
import cv2
from multiprocessing import Pool

Ucam = cam.UpCam()
Dcam = cam.DownCam()
Lcam = cam.LeftCam()
Rcam = cam.RightCam()

ifio:bool=True

def main_detect_color(img:cv2.typing.MatLike, _cam:cam.UpCam|cam.DownCam|cam.LeftCam|cam.RightCam):
    return _cam.detect_color(img, ifio)
    
def main_read_img(side:str):
    if side == 'U':
        return Ucam.read_usb_capture()
    elif side == 'D':
        return Dcam.read_usb_capture()
    elif side == 'L':
        return Lcam.read_usb_capture()
    elif side == 'R':
        return Rcam.read_usb_capture()
    else:
        raise ValueError("side must be in ['U','D','L','R']")

def crack():
    t1 = time.perf_counter()
    # 获取魔方颜色状态
    with Pool(4) as p:
        img_res = p.map(main_read_img,['U','R','L','D'])
    t2 = time.perf_counter()
    print(f'read time {t2-t1}')

    res0 = [
            main_detect_color(img_res[0][0],Ucam),
            main_detect_color(img_res[1][0],Rcam),
            main_detect_color(img_res[2][0],Lcam),
            main_detect_color(img_res[3][0],Dcam)
            ]
    t2 = time.perf_counter()
    print('detect time:',t2-t1)

    color_state2,color_state3 = res0[0]     # type:ignore
    color_state1 = res0[1]
    color_state4 = res0[2]
    color_state5,color_state6 = res0[3]     # type:ignore
    color_state = color_state3 + color_state1 + color_state2 + color_state6 + color_state4 + color_state5   # type:ignore
    color_state = cube_solver.color2view(color_state)
    print("color state is:" + color_state)

    # 解算得到机械臂步骤
    solve_step = cube_solver.cube_solver(color_state)
    _solve_step = solve_step.split()
    _solve_step = _solve_step[:-1]
    print("the orign step is:", _solve_step)
    real_solve, cost = cube_solver._SolutionTransAndOptimize(_solve_step)
    # real_solve = _solve_step
    arm_step = arm_planning.planning(real_solve)  # ['RO', 'L2', 'RC', 'R2']
    print("--------------------------------------------")
    print("the optimize step is:",real_solve)
    print("--------------------------------------------")
    print("arm_step:",arm_step)
    step_str = ''
    for index,i in enumerate(arm_step):
        if index != len(arm_step) - 1:
            step_str += i + ' '
        else:
            step_str += i

    Transmitter.write(step_str)
    
    return arm_step

Transmitter = communication.UART()

if __name__ == '__main__':
    input("Press 'enter' to continues:")
    crack()
