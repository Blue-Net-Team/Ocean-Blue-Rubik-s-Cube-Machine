import cube_solver
import time
import arm_planning
import twophase.cubie as cubie
# FIXME: 将下面的模块名更改，更改所有匹配项
from cam import color_detect_use1
from cam import color_detect_use2
from cam import color_detect_use3
from cam import color_detect_use4


def crack():
    # 获取魔方颜色状态
    [color_state2,color_state3] = color_detect_use2.detect_color()
    color_state1 = color_detect_use1.detect_color()

    color_state4 = color_detect_use3.detect_color()
    [color_state5,color_state6] = color_detect_use4.detect_color()
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
    arm_step = arm_planning.planning(real_solve)
    return arm_step


