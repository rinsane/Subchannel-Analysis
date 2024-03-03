import matplotlib.pyplot as plt
from input import *
from grid import *
from coefficient import *
from TDMAT import *
import numpy as np
import os
from tabulate import tabulate

T_total=[]
for i in range(0,(t*1)):
    Ai.clear()
    Bi.clear()
    if(i==1):
        T[NT-1]=0
        T_OLD[:]=T[:]
    else:
        #coeff_T()
        T_t[:]=TDMA_T(i)
        print("T: ",T_t)
        T_OLD[:]=T_t[:]
        print("T_old",T_OLD)
    
    ######saving results in an array####
    if(i==0):
        T_total.append(T[:])
    else:
        T_total.append(T_OLD[:])
    print("T_total: ",T_total)

# col_names = ['time(sec)','temperature']
# data = []
# for i in range(0, (t*100)):
#    data.append([i+1,T_total[i]])

# print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))   
    #forming tabular form

for i in range(0,(t*1)):
    if(i==0):
        print("T_steady: ",T_total[i])
    elif(i==(t)-1):
        print("T_last: ",T_total[i])

import matplotlib.pyplot as plt
for i in range(0,(t*1)):
    if(i==0):
       plt.plot(r,T_total[i],label='steady')
    else:
       plt.plot(r,T_total[i],label='transient')
plt.xlabel('lenght')
plt.ylabel('temperature')
plt.title('temperature vs length')
plt.legend()
plt.show()