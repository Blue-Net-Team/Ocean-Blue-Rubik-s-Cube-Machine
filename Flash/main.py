import cube_solver
import time
import communication
import arm_planning
import twophase.cubie as cubie
from vision import color_detect_use1
from vision import color_detect_use2
from vision import color_detect_use3
from vision import color_detect_use4


def crack():
    # 获取魔方颜色状态
    [color_state2,color_state3] = color_detect_use2.detect_color()
    color_state1 = color_detect_use1.detect_color()

    color_state4 = color_detect_use3.detect_color()
    [color_state5,color_state6] = color_detect_use4.detect_color()
    color_state = color_state2 + color_state1 + color_state3 + color_state5 + color_state4 + color_state6
    color_state = cube_solver.color2view(color_state)
    print("color state is:" + color_state)

    # 生成随机魔方状态用于测试机械
    # cc = cubie.CubieCube()
    # cnt = [0] * 31
    # cc.randomize()
    # fc = cc.to_facelet_cube()
    # s = fc.to_string()
    # color_state = s

    # 解算得到机械臂步骤
    solve_step = cube_solver.cube_solver(color_state)
    _solve_step = solve_step.split()
    _solve_step = _solve_step[:-1]
    real_solve, cost = cube_solver._SolutionTransAndOptimize(_solve_step)
    arm_step = arm_planning.planning(real_solve)
    # print(solve_step)
    # print(arm_step)
    return arm_step







""" et = time.perf_counter()
time1 = et - st

num = 0
st = time.perf_counter()
for i in arm_step:
    # 按一次回车动一下
    # if input() == 'c':
    #     communication.send_msg('LO RO \r\n')
    #     print(num)
    # else:
        num = num + 1
        i = i + '\r\n'
        communication.send_msg(i)
        if str(i[1]) == 'C':
            time.sleep(0.12)
        elif str(i[1]) == 'O':
            time.sleep(0.12)
        elif str(i[1]) == '2':
            time.sleep(0.29)
        else:
            time.sleep(0.19)
et = time.perf_counter()
time2 = et - st

time.sleep(0.1)
communication.send_msg('LO RO \r\n')
print(num)

print("识别和规划花费了 {:.4f}s.".format((time1)))
print("还原魔方花费了 {:.4f}s.".format((time2))) """
