from input import *
from grid import *
from coefficient import *
from bc import*
import matplotlib.pyplot as plt

def TDMA_T():
   
    for i in range(0,NT):
        if(i==0):
            Ai_exp=CAE[i]/CAP[i]
            Bi_exp=S[i]/CAP[i]
            Ai.append(Ai_exp)
            Bi.append(Bi_exp)
        


        else:
            Ai_exp=CAE[i]/(CAP[i]-(CAW[i]*Ai[i-1]))
            Bi_exp=(S[i]+(CAW[i]*(Bi[i-1])))/(CAP[i]-(CAW[i]*Ai[i-1]))
            Ai.append(Ai_exp)
            Bi.append(Bi_exp)
            
    print("Ai: ",Ai)
    print("Bi: ",Bi)
    
    T_OLD[NT-1]=Bi[NT-1]
    for i in range(NT-2,-1,-1):
        T_to=(Ai[i]*T_OLD[i+1])+(Bi[i])
        T_OLD[i]=T_to  
    # T[0]=T[1]       
                                              ############## CENTERLINE BC ISSUE RESOLVED
    print("T: ",T_OLD)
    return (T_OLD)
    


TDMA_T()
col_names=["T","r"]
data=[]
for i in range(0,NF+NC):
    data.append([T_OLD[i],r[i]])
    
print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))


plt.plot(r, T_OLD, label='Temperature vs. Radius')
plt.xlabel('Radius')
plt.ylabel('Temperature')
plt.title('Temperature Profile')
plt.legend()
plt.show()