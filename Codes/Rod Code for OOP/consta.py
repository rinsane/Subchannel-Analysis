import numpy as np

R1=0.012
R2=0.015
R3=0.021

NF=13
NC=8                                        ##### SOME PROBLEM LIES WITH NC
NG=1                                        ### ALWAYS TAKE 1 NODE TO SOLVE FOR GAP THAT IS IT IS AT INTERSECTION BETWEEN FUEL AND CLAD  
NT=NF+NC

kf=2.5                                        ### thermal conduvtivity of fuel rod
Q=10e6
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

CAQ=[]
S=[]
CAP=[]
HTCC=3840
T=[0 for i in range(0,NF+NC)]
print(T)
Ai=[]
Bi=[]

qflux=0