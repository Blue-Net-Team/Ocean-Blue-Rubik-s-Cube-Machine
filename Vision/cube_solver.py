import twophase.solver as sv
import twophase.cubie as cubie
import time
import arm_planning
import kociemba


def cube_solver(view_state):
    """魔方求解"""
    solve_step = sv.solve(view_state,0,0.05)
    return solve_step    

def color2view(color_state):
    """将SVM识别的颜色状态转换成视角状态，blue:U green:D yellow:F white:B orange:R red:L 意思是中心块颜色固定位置，与视角绑定"""
    _color_state = ''
    for i in color_state:
        if i == 'B':
            _color_state = _color_state + 'U'
        elif i == 'G':
            _color_state = _color_state + 'D'
        elif i == 'Y':
            _color_state = _color_state + 'F'
        elif i == 'W':
            _color_state = _color_state + 'B'
        elif i == 'R':
            _color_state = _color_state + 'L'
        elif i == 'O':
            _color_state = _color_state + 'R'
    return _color_state


def _SolutionTransAndOptimize(Solution):        #以这样的抓法，正对自己的是R,背后是L,右上是U,左上是F
    """二叉树搜索最优路径，算法优化,原理是在转L,R面时判断是转到左手还是右手
    左手抓down，右手抓back"""
    standard_state = 'UDFBRL'
    transtable = {'U' :('DUFBLR',0.4),      #U U->D D->U L->R R->L  R 180 degree
                  'D' :('UDFBRL',0),
                  'F' :('UDBFLR',0.4),      #F F->B B->F L->R R->L  L 180 degree

                  'I' :('RLFBDU',0.6),      #L L->D D->R R->U U->L  R_a 90 degree
                  'l' :('UDRLBF',0.6),      #l L->B B->R R->F F->L  L_c 90 degree

                  'Z' :('LRFBUD',0.6),      #R R->D D->L L->U U->R  R_c 90 degree
                  'r' :('UDLRFB',0.6),      #r R->B B->L L->F F->R  L_a 90 degree
                  'B' :('UDFBRL',0)}
    cost = 0
    cost_l = 0
    cost_L = 0
    Solution_l = []
    Solution_L = []
    Solution_temp_l = []
    Solution_temp_L = []
    for i in range(len(Solution)):
        if Solution[i][0] == 'L':
            Solution_l = Solution[i:len(Solution)]
            Solution_l[0] = Solution_l[0].replace('L','l')
            Solution_L = Solution[i:len(Solution)]
            Solution_L[0] = Solution_L[0].replace('L','I')
            Solution_temp_l,cost_l = _SolutionTransAndOptimize(Solution_l)
            Solution_temp_L,cost_L = _SolutionTransAndOptimize(Solution_L)
            
            if cost_L < cost_l:
                _Solution = Solution[0:i]
                if (Solution_temp_L[0][0] == 'I'):
                    Solution_temp_L[0] = Solution_temp_L[0].replace('I','L')
                _Solution = _Solution + Solution_temp_L
                cost = cost+cost_L
                return _Solution,cost
            else:
                _Solution = Solution[0:i]
                if (Solution_temp_l[0][0] == 'I'):
                    Solution_temp_l[0] = Solution_temp_l[0].replace('I','L')
                _Solution = _Solution + Solution_temp_l
                cost = cost+cost_l
                return _Solution,cost
        elif Solution[i][0] == 'R':
            Solution_r = Solution[i:len(Solution)]
            Solution_r[0] = Solution_r[0].replace('R','r')
            Solution_R = Solution[i:len(Solution)]
            Solution_R[0] = Solution_R[0].replace('R','Z')
            Solution_temp_r,cost_r = _SolutionTransAndOptimize(Solution_r)
            Solution_temp_R,cost_R = _SolutionTransAndOptimize(Solution_R)
            
            if cost_R < cost_r:
                _Solution = Solution[0:i]
                if (Solution_temp_R[0][0] == 'Z'):
                    Solution_temp_R[0] = Solution_temp_R[0].replace('Z','R')
                _Solution = _Solution + Solution_temp_R 
                cost = cost+cost_R
                return _Solution,cost
            else:
                _Solution = Solution[0:i]
                if (Solution_temp_r[0][0] == 'Z'):
                    Solution_temp_r[0] = Solution_temp_r[0].replace('Z','R')
                _Solution = _Solution + Solution_temp_r
                cost = cost+cost_r
                return _Solution,cost
        else:
            cost = cost + transtable[Solution[i][0]][1]
            for j in range((i+1),len(Solution)):
                for face in range(len(standard_state)):
                    if (Solution[j][0] == standard_state[face]):
                        Solution[j] = Solution[j].replace(standard_state[face],transtable[Solution[i][0]][0][face])
                        break
    for i in range(len(Solution)):
        # cost = cost + transtable[Solution[i][0]][1]
        if (Solution[i][0] == 'Z'):
            Solution[i] = Solution[i].replace('Z','R')
        if (Solution[i][0] == 'I'):
            Solution[i] = Solution[i].replace('I','L')
    return Solution, cost

#blue:U green:D yellow:F white:B orange:R red:L 
def test():
    """生成随机魔方状态用于解算"""
    cc = cubie.CubieCube()
    cnt = [0] * 31
    cc.randomize()
    fc = cc.to_facelet_cube()
    s = fc.to_string()

    #对比K算法和R算法
    cube_state = s
    #K算法
    st = time.perf_counter()
    print(kociemba.solve(cube_state))
    et = time.perf_counter()
    print("spent {:.4f}s.".format((et - st)))

    #R算法
    st = time.perf_counter()
    cube_solve = sv.solve(cube_state,0,0.05)
    print(cube_solve)
    et = time.perf_counter()
    print("spent {:.4f}s.".format((et - st)))
    return cube_solve

if __name__ == '__main__':  
    solve_step = test()
    _solve_step = solve_step.split()
    print(solve_step)
    print(_solve_step)
    real_solve, cost = _SolutionTransAndOptimize(_solve_step)
    arm_step = arm_planning.planning(real_solve)
    
    # print(real_solve)
    print(arm_step)