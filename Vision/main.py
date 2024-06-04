import cube_solver
import time
import communication
import arm_planning
import twophase.cubie as cubie

from cam import Right
from cam import Up
from cam import Left
from cam import Down


def crack():
    # 获取魔方颜色状态
    [color_state2,color_state3] = Up.detect_color()
    color_state1 = Right.detect_color()

    color_state4 = Left.detect_color()
    [color_state5,color_state6] = Down.detect_color()
    color_state = color_state2 + color_state1 + color_state3 + color_state5 + color_state4 + color_state6
    color_state = cube_solver.color2view(color_state)
    print("color state is:" + color_state)

    # region 生成随机魔方状态用于测试机械
    # cc = cubie.CubieCube()
    # cnt = [0] * 31
    # cc.randomize()
    # fc = cc.to_facelet_cube()
    # s = fc.to_string()
    # color_state = s
    # endregion

    # 解算得到机械臂步骤
    solve_step = cube_solver.cube_solver(color_state)
    _solve_step = solve_step.split()
    _solve_step = _solve_step[:-1]
    real_solve, cost = cube_solver._SolutionTransAndOptimize(_solve_step)
    arm_step = arm_planning.planning(real_solve)  # ['RO', 'L2', 'RC', 'R2']
    Transmitter = communication.UART()
    
    step_str = ''
    for i in arm_step:
        if i != arm_step[-1]:
            step_str += i + ' '
        else:
            step_str += i

    Transmitter.write(step_str)
    
    return arm_step


