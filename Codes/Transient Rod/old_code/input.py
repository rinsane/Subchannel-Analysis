import numpy as np

R1=0.012
R2=0.015
R3=0.021
GT=0.003
NF=5000
NC=400                                        ##### SOME PROBLEM LIES WITH NC
NG=1                                        ### ALWAYS TAKE 1 NODE TO SOLVE FOR GAP THAT IS IT IS AT INTERSECTION BETWEEN FUEL AND CLAD  
NT=NF+NC

#kf=2.5                                        ### thermal conduvtivity of fuel rod

HTC=7800
shi=1
Tinf=400
r=[]
rw=[]
re=[]
drw=[]
dre=[]
AW=[]
CAW=[]
AW_ex=[]
AE=[]
CAE=[]
AQ=[]
AT=[]
ATO=[]
T_OLD=[]

CAQ=[]
S=[]
CAP=[]
HTCC=3276
T=[0 for i in range(0,NF+NC)]
print(T)
Ai=[]
Bi=[]

qflux=0

#Rho=[10650 for i in range(0,NF+NC)]                                                                  ########### DENSITY
#Rho_O=[10650 for i in range(0,NF+NC)]  

#C=[235 for i in range(0,NF+NC)]    
#C_O=[235 for i in range(0,NF+NC)]                                                                         ### specific heat 

Dt=1
t=1
T_OLD = [T[i] for i in range(NF+NC)]
T_t=[]



############ from here i am using different properties at different intervals
Q=[]
for i in range(0,NF+NC):
    if(i<=NF):
        Q.append(1e7)
    else:
        Q.append(0)

Rho=[]
for i in range(0,NF+NC):
    if(i<=NF):
        Rho.append(18900)
    else:
        Rho.append(6510)
        
Rho_O=[]
for i in range(0,NF+NC):
    if(i<=NF):
        Rho_O.append(18900)
    else:
        Rho_O.append(6510)
        
C=[]
for i in range(0,NF+NC):
    if(i<=NF):
        C.append(120)
    else:
        C.append(270)
        
C_O=[]
for i in range(0,NF+NC):
    if(i<=NF):
        C_O.append(120)
    else:
        C_O.append(270)

kf=[]
for i in range (0,NF+NC):
    if(i<=NF):
        kf.append(10)
    else:
        kf.append(20)
