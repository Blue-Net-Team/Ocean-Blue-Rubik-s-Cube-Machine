#将解算魔方步骤转换成机械臂操作步骤(这里定义了解魔方所有的步骤对应的机械臂操作)
def planning(command): #1 means clockwise 90 degree
                       #2 means 180 degree
                       #3 means anticlockwise 90 degree
                       #O means hand open
                       #C means hand close
                       #R means right arm
                       #L means left arm
                       
                       #字典的键里面L,R开头的操作是将(L或R面)转到D面操作,而l,r是将将(L或R面)转到B面进行操作
                       #字典里面的L,R是机器臂的左右,不要与键里面的混淆
    hash_dic = {     'D1':'L1 LO L3 LC',
                     'D2':'L2',
                     'D3':'L3 LO L1 LC',

                     'B1':'R1 RO R3 RC',
                     'B2':'R2',
                     'B3':'R3 RO R1 RC',

                     'U1':'LO R2 LC L1 LO L3 LC',
                     'U2':'LO R2 LC L2',
                     'U3':'LO R2 LC L3 LO L1 LC',

                     'F1':'RO L2 RC R1 RO R3 RC',
                     'F2':'RO L2 RC R2',
                     'F3':'RO L2 RC R3 RO R1 RC',

                     'L1':'LO R1 LC RO R3 RC L1 LO L3 LC',
                     'L2':'LO R1 LC RO R3 RC L2',
                     'L3':'LO R1 LC RO R3 RC L3 LO L1 LC',

                     'R1':'LO R3 LC RO R1 RC L1 LO L3 LC',
                     'R2':'LO R3 LC RO R1 RC L2',
                     'R3':'LO R3 LC RO R1 RC L3 LO L1 LC',
                
                     'l1':'RO L3 RC LO L1 LC R1 RO R3 RC',
                     'l2':'RO L3 RC LO L1 LC R2',
                     'l3':'RO L3 RC LO L1 LC R3 RO R1 RC',

                     'r1':'RO L1 RC LO L3 LC R1 RO R3 RC',
                     'r2':'RO L1 RC LO L3 LC R2',
                     'r3':'RO L1 RC LO L3 LC R3 RO R1 RC',
               }
    arm_step = ''
    for i in command:
           arm_step += hash_dic[i] + ' '
    arm_step = arm_step.split()
    _arm_step = []

    #优化操作步骤
    num = 0
    while(num < len(arm_step) - 1):
        if(arm_step[num] == 'LC' and arm_step[num + 1] == 'LO'):
            num = num + 2
        elif(arm_step[num] == 'RC' and arm_step[num + 1] == 'RO'):
            num = num + 2
        else:
            _arm_step .append(arm_step[num])
            num = num + 1
    _arm_step.append(arm_step[len(arm_step)-1])
    return _arm_step

if __name__ == '__main__': 
    planning(['F2', 'D2', 'R3', 'R2', 'B2', 'r1', 'r2', 'r1', 'F2', 'D1', 'L2', 'F1', 'F2', 'U1', 'F2', 'F3', 'U3', 'l3', 'U1'])