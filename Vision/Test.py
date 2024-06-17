import twophase.solver as sv
import twophase.cubie as cubie
import cube_solver as cs

def random_test():
    #生成随机魔方状态用于解算
    cc = cubie.CubieCube()
    cnt = [0] * 31
    cc.randomize()
    fc = cc.to_facelet_cube()
    s = fc.to_string()
    return s

# 从还原状态到特定状态
Y = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
T = random_test()
do = sv.solveto(Y,T,19,0.1)
print("从还原态到特定状态的步骤：")
print(do)
print("--------------------")

cube_solve = sv.solve(T,0,0.05)
# print(cube_solve)
_solve_step = cube_solve.split()
_solve_step = _solve_step[:-1]

better_step,_ = cs._SolutionTransAndOptimize(_solve_step)
print("机械臂步骤：")
print(better_step)