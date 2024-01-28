import numpy as np
from inputs import*
from XMULT import*
from YMULT import*
from GAUSS import*
from SKI import*
from XA import*
from wprim import*
from star import*
from XD import*
from XB import*
from HM import*
from DCROSS import*
from MASFLOW import*
from AXIMOM import*
import time
start = time.time()
WIJIN=0.0
PIN=12262500
print(PIN)
for I in range(NCHANL):
    F1[I]=F0[I]
    P0[I]=PIN
    
for K in range(NK):
    WIJ0[K]=WIJIN
    WIJ1[K]=WIJIN

DELX=AXLN/(NNODE-1)
X=0
NODE=1
while X<=AXLN:
    print('CHANNLE AXIAL LENGTH =', X)
    print('NODE =', NODE)
    XD()
    XB()
    YMULT(XMLT,S,XM,NCHANL,NK,NCHANL)
    for I in range(NCHANL):
        for J in range(NCHANL):
            XM[I,J]=DELX*SLP*XM[I,J]/A[I]
    for II in range(NCHANL):
        for JJ in range(NCHANL):
           if II==JJ:
              XMI[II,JJ]=THETA*XM[II,JJ]+1
           else:
              XMI[II,JJ]=THETA*XM[II,JJ]
            
    for I in range(NCHANL):
        for J in range(NCHANL):
          XM0[I,J]=XMI[I,J]-XM[I,J]
        
    for I in range(NCHANL):
        SUM=0
        for J in range(NCHANL):
            PM=XM0[I,J]*P0[J]
        SUM=SUM+PM
        PM0[I]=SUM
        PB[I]=B[I]+PM0[I]
    
    gauss(XMI, P1, PB, NCHANL)
    DCROSS()
    for K in range(NK):
       WIJ1[K]=-WIJ1[K]
    for I in range(NCHANL):
        F11[I]=F1[I]
    MASFLO()
    for I in range(NCHANL):
       ERROR[I]=abs((F11[I]-F1[I])/F1[I])
    for I in range(NCHANL):
       if ERROR[I]>=ERROR[I+1]:
           EMAX=ERROR[I]
       else:
           EMAX=ERROR[I+1]
#### some data to be added 
    if EMAX > 1e-02:
            break
    else:
       X += DELX
       NODE += 1
### special iterative scheme to converge axial mass flow
  
    print(X)
   # print('ITERATION =', IT)
    print('AXIAL FLOW =', F1)
    print('P1 =', P1)
    
    HM()
end = time.time()
print("The time of execution of above program is :",(end-start) * 10**3, "ms") 

for K in range(NK):
    print(WIJ1[K])   
    
    
    
    
    
    
    
### problem exist with wij1 and main program for node motion
