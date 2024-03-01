
from consta import *
from grid import *
from coefff import *
from bc import*

def TDMA_ST():
   
    for i in range(0,NT):
        if(i==0):
            Ai_exp=CAE[i]/CAP[i]
            Bi_exp=S[i]/CAP[i]
            Ai.append(Ai_exp)
            Bi.append(Bi_exp)
        
        elif(i==NT):
            Ai_exp=CAW[i]/CAP[i]
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
    
    
    
    T[NT-1]=Bi[NT-1]
    for i in range(NT-2,0,-1):
        T_exp=(Ai[i]*T[i+1])+(Bi[i])
        T[i]=T_exp  
    T[0]=T[1]       
                                              ############## CENTERLINE BC ISSUE RESOLVED
    print("T: ",T)
    return T
    
