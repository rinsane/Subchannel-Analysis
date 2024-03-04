from functions import func
import matplotlib.pyplot as plt


curr = 1
while curr <= 1:
    runner = func()
    '''runner.T = [curr for _ in range(runner.NF + runner.NC)]
    runner.T_OLD = [runner.T[i] for i in range(runner.NF + runner.NC)]'''
    runner.Dt = curr
    curr += 0.1
    runner.grid()
    runner.coeff_T()
    runner.bc()
    T_total=[]
    for i in range(0,(runner.t*1)):
        runner.Ai.clear()
        runner.Bi.clear()
        if(i==1):
            runner.T[runner.NT-1]=0
            runner.T_OLD[:]=runner.T[:]
        else:
            #coeff_T()
            runner.T_t[:]=runner.TDMA()
            # print("T: ",runner.T_t)
            runner.T_OLD[:]=runner.T_t[:]
            # print("T_old",runner.T_OLD)

        ######saving results in an array####
        if(i==0):
            T_total.append(runner.T[:])
        else:
            T_total.append(runner.T_OLD[:])
        # print("T_total: ",T_total)

    plt.plot(runner.r, runner.T_OLD, label=f'Time {round(curr, 2)}')

plt.xlabel('Radius')
plt.ylabel('Temperature')
plt.title('Temperature Profile')
plt.legend()
plt.show() 
# col_names = ['time(sec)','temperature']
    # data = []
# for i in range(0, (t*100)):
#    data.append(T_total[i]])

# print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))   
    #forming tabular form

'''for i in range(0,(runner.t*1)):
    if(i==0):
        print("T_steady: ",T_total[i])
    elif(i==(runner.t)-1):
        print("T_last: ",T_total[i])
for i in range(0,(runner.t*1)):
    if(i==0):
        plt.plot(runner.r,T_total[i],label='steady')
else:
        plt.plot(runner.r,T_total[i],label='transient')
plt.xlabel('lenght')
plt.ylabel('temperature')
plt.title('temperature vs length')
plt.legend()
plt.show()'''