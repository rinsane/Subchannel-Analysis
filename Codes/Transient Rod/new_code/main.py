from tabulate import tabulate
from functions import func
import matplotlib.pyplot as plt

curr = 0
while curr <= 1000:
    runner = func()
    
    #'''
    runner.T = [curr for _ in range(runner.NF + runner.NC)]
    runner.T_OLD = [runner.T[i] for i in range(runner.NF + runner.NC)]
    #'''
    #runner.Dt = curr
    print(curr)
    curr += 10
    runner.grid()
    runner.coeff_T()
    runner.bc()
    runner.TDMA()

    plt.plot(runner.r, runner.T_OLD, label='Temperature vs. Radius')
    plt.xlabel('Radius')
    plt.ylabel('Temperature')
    plt.title('Temperature Profile')
    plt.legend()

    '''
    T_total=[]
    for i in range(0,(runner.t)):
        runner.Ai.clear()
        runner.Bi.clear()
        if(i==1):
            runner.T[runner.NT-1]=0
            runner.T_OLD[:]=runner.T[:]
        else:
            runner.T_t[:]=runner.TDMA()
            runner.T_OLD[:]=runner.T_t[:]

        ######saving results in an array####
        if(i==0):
            T_total.append(runner.T[:])
        else:
            T_total.append(runner.T_OLD[:])
        '''

plt.show()