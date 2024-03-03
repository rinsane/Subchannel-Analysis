import numpy as np
from consta import*
from grid import*


#AW
for i in range(0,NF+NC):
    if(i==0):
        AW_ex=0
    else:
        AW_ex=rw[i]*kf/drw[i]
    AW.append(AW_ex)
    #print("AW",AW_ex)
    
    
#CAW
for i in range(0,NF+NC):
    CAW_exp=shi*AW[i]
    CAW.append(CAW_exp)
   #print(CAW_exp)
    
#AE
for i in range(0,NF+NC):
    if(i<=NF+NC-2):
        AE_exp=re[i]*kf/dre[i]
    else:
        AE_exp=0
    AE.append(AE_exp)
    #print(AE_ex)
    
    
#CAE
for i in range(0,NF+NC):
    CAE_exp=shi*AE[i]
    CAE.append(CAE_exp)
    #print(CAE_exp)
    
#AQ
for i in range(0,NF+NC):
    if(i<NF):
        Q=10000000
    else:
        Q=0
    if(i<=NF+NC):
        AQ_exp=0.5*((re[i]*re[i]-rw[i]*rw[i])*Q) 
    else:
        AQ_exp=0
    AQ.append(AQ_exp)
    #print(AQ_exp)

#CAQ
for i in range(0,NF+NC):
    CAQ_exp=shi*AQ[i]
    CAQ.append(CAQ_exp)
    #print(CAQ_exp)

#S
for i in range(0,NF+NC):
    S_exp=CAQ[i]
    S.append(S_exp)
    #print(S_exp)
        
#CAP
for i in range(0,NF+NC):
    if(i<=NF+NC-1):
        CAP_exp=CAE[i]+CAW[i]
    elif(i==NF+NC-1):
        CAP_exp=CAW[i]
    CAP.append(CAP_exp)
    #print(CAP_exp)
    
col_names=["CAW","CAE","CAP","S","AQ"]
data=[]
for i in range(0,NF+NC):
    data.append([CAW[i],CAE[i],CAP[i],S[i],AQ[i]])
    
print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))