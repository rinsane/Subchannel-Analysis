import numpy as np
from input import*
from grid import*
def coeff_T():
    AE.clear()
    AW.clear()
    AT.clear()
    ATO.clear()
    AQ.clear()
    CAW.clear()
    CAE.clear()
    CAQ.clear()
    CAP.clear()
    S.clear()
    
    
    #AW
    for i in range(0,NF+NC):
        if(i==0):
            AW_ex=0
        else:
            AW_ex=rw[i]*kf[i]/drw[i]
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
            AE_exp=re[i]*kf[i]/dre[i]
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
       
        if(i<=NF+NC):
            AQ_exp=0.5*((re[i]*re[i]-rw[i]*rw[i])*Q[i]) 
        else:
            AQ_exp=0
        AQ.append(AQ_exp)
        #print(AQ_exp)
        
    #CAQ
       

    for i in range(0,NF+NC):
        CAQ_exp=shi*AQ[i]
        CAQ.append(CAQ_exp)
        #print(CAQ_exp)


    #AT
        for i in range(0,NF+NC):
            AT_exp=(Rho[i]*C[i])*((re[i]**2)-(rw[i]**2))/(2*Dt)
            AT.append(AT_exp)
        # print("AT: ",AT)
        
        
    #ATO
        for i in  range(0,NF+NC):
            ATO_exp=(Rho_O[i]*C_O[i])*((re[i]**2)-(rw[i]**2))/(2*Dt)
            ATO.append(ATO_exp)
        #print("ATO",ATO)
        
        
        
        
        
        
        
    #S
    for i in range(0,NF+NC):
        S_exp=CAQ[i]+ATO[i]*T_OLD[i]
        S.append(S_exp)
        print(S_exp)
            
    #CAP
    for i in range(0,NF+NC):
        if(i<=NF+NC-1):
            CAP_exp=CAE[i]+CAW[i]+AT[i]
        elif(i==NF+NC-1):
            CAP_exp=CAW[i]+AT[i]
        CAP.append(CAP_exp)
        #print(CAP_exp)
        
    col_names=["CAW","CAE","CAP","S","AQ","AT","ATO"]
    data=[]
    for i in range(0,NF+NC):
        data.append([CAW[i],CAE[i],CAP[i],S[i],AQ[i],AT[i],ATO[i]])
        
    print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))


coeff_T()

