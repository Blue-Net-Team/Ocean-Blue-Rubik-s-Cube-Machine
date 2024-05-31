import twophase.solver as sv
import twophase.cubie as cubie
import time
import arm_planning
import kociemba

#解算魔方
def cube_solver(view_state):
    solve_step = sv.solve(view_state,0,0.05)
    return solve_step   

#将SVM识别的颜色状态转换成视角状态，blue:U green:D yellow:L white:R orange:B red:F 意思是中心块颜色固定位置，与视角绑定
def color2view(color_state):
    _color_state = ''
    for i in color_state:
        if i == 'B':
            _color_state = _color_state + 'U'
        elif i == 'G':
            _color_state = _color_state + 'D'
        elif i == 'Y':
            _color_state = _color_state + 'L'
        elif i == 'W':
            _color_state = _color_state + 'R'
        elif i == 'R':
            _color_state = _color_state + 'F'
        elif i == 'O':
            _color_state = _color_state + 'B'
    return _color_state

#左手抓down，右手抓back，最优路径搜索(算法优化,原理是在转L,R面时判断是转到左手还是右手,L在背面)
def _SolutionTransAndOptimize(Solution):
    # print(f"Debug: Solution at start of function: {Solution}")
    standard_state = 'UDFBRL'
    transtable = {'U': ('DUFBLR', 0.4),  # U U->D D->U L->R R->L  R 180 degree
                  'D': ('UDFBRL', 0),
                  'F': ('UDBFLR', 0.4),  # F F->B B->F L->R R->L  L 180 degree

                  'I': ('RLFBDU', 0.6),  # L L->D D->R R->U U->L  R_a 90 degree 顺时针
                  'l': ('UDRLBF', 0.6),  # l L->B B->R R->F F->L  L_c 90 degree

                  'Z': ('LRFBUD', 0.6),  # R R->D D->L L->U U->R  R_c 90 degree
                  'r': ('UDLRFB', 0.6),  # r R->B B->L L->F F->R  L_a 90 degree
                  'B': ('UDFBRL', 0)}
    cost = 0
    Solution_temp = []
    for i in range(len(Solution)):
        if Solution[i][0] == 'L':
            Solution_l = Solution[i:len(Solution)]
            Solution_l[0] = Solution_l[0].replace('L', 'l')
            Solution_L = Solution[i:len(Solution)]
            Solution_L[0] = Solution_L[0].replace('L', 'I')
            Solution_temp_l, cost_l = _SolutionTransAndOptimize(Solution_l)
            Solution_temp_L, cost_L = _SolutionTransAndOptimize(Solution_L)

            if cost_L < cost_l:
                Solution_temp.extend(Solution_temp_L) # 既然是最优路径,那么就将最优路径加入当前的暂存列表
                cost += cost_L
            else:
                Solution_temp.extend(Solution_temp_l)
                cost += cost_l
            break
        elif Solution[i][0] == 'R':
            Solution_r = Solution[i:len(Solution)]
            Solution_r[0] = Solution_r[0].replace('R', 'r')
            Solution_R = Solution[i:len(Solution)]
            Solution_R[0] = Solution_R[0].replace('R', 'Z')
            Solution_temp_r, cost_r = _SolutionTransAndOptimize(Solution_r)
            Solution_temp_R, cost_R = _SolutionTransAndOptimize(Solution_R)

            if cost_R < cost_r:
                Solution_temp.extend(Solution_temp_R)
                cost += cost_R
            else:
                Solution_temp.extend(Solution_temp_r)
                cost += cost_r
            break
        else: # 如果不是L或R(即确定的步骤),执行该步骤后魔方状态改变,原来各个面的身份变了,所以后面的步骤也要跟着改变
            if Solution[i][0] not in transtable:
                raise KeyError(f"Unexpected key in Solution: {Solution[i][0]}")
            cost += transtable[Solution[i][0]][1] # 如:'R0'->'R'的cost为0.6
            for j in range(i + 1, len(Solution)):
                for face in range(len(standard_state)):
                    if Solution[j][0] == standard_state[face]:
                        Solution[j] = Solution[j].replace(standard_state[face], transtable[Solution[i][0]][0][face])
                        break
            Solution_temp.append(Solution[i]) # 最后将当前步骤加入暂存列表
    Solution_temp.extend(Solution[len(Solution_temp):])
    for i in range(len(Solution_temp)):
        if Solution_temp[i][0] == 'Z':
            Solution_temp[i] = Solution_temp[i].replace('Z', 'R')
        if Solution_temp[i][0] == 'I':
            Solution_temp[i] = Solution_temp[i].replace('I', 'L')
    return Solution_temp, cost

#blue:U green:D yellow:R white:L orange:B red:F 
def test():
    #生成随机魔方状态用于解算
    cc = cubie.CubieCube()
    cnt = [0] * 31
    cc.randomize()
    fc = cc.to_facelet_cube()
    s = fc.to_string()

    #对比K算法和R算法
    cube_state = s
    #K算法
    # st = time.perf_counter()
    a = kociemba.solve(cube_state)
    # print(a)
    # et = time.perf_counter()
    # print("spent {:.4f}s.".format((et - st)))

    #R算法
    # st = time.perf_counter()
    cube_solve = sv.solve(cube_state,0,0.05)
    print(cube_solve)
    # et = time.perf_counter()
    # print("spent {:.4f}s.".format((et - st)))
    return cube_solve, a

# 对于k算法需要进行转换
def transform(moves):
    dic = {
        'F': 'F1',
        'F2': 'F2',
        "F'": 'F3',
        'R': 'R1',
        'R2': 'R2',
        "R\'": 'R3',
        'U': 'U1',
        'U2': 'U2',
        "U\'": 'U3',
        'B': 'B1',
        'B2': 'B2',
        "B\'": 'B3',
        'L': 'L1',
        'L2': 'L2',
        "L\'": 'L3',
        'D': 'D1',
        'D2': 'D2',
        "D\'": 'D3',
    }

    return [dic[move] for move in moves]

if __name__ == '__main__':  
    solve_step, a = test()
    # r
    # st = time.perf_counter()
    _solve_step = solve_step.split()
    _solve_step = _solve_step[:-1]
    #print(solve_step)
    print(_solve_step)
    real_solve, cost = _SolutionTransAndOptimize(_solve_step)
    arm_step = arm_planning.planning(real_solve)
    print("-------------------------------")
    print(real_solve)
    # print(arm_step)
    # et = time.perf_counter()
    # print("spent {:.4f}s.".format((et - st)))
    
    # k
    """ st = time.perf_counter()
    _a = a.split()
    _a = transform(_a)
    real_solve2, cost2 = _SolutionTransAndOptimize(_a)
    arm_step2 = arm_planning.planning(real_solve2)
    #print(arm_step2)
    et = time.perf_counter()
    print("spent {:.4f}s.".format((et - st))) """