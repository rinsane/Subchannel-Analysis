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


for i in range(NNODE):
    if i==0:
        for I in range(NCHANL):
            F1[I]=F0[I]
            P0[I]=PIN
            print(P0[I])
        print("FGfg")
        for K in range(NK):
            WIJ0[K]=WIJIN
            WIJ1[K]=WIJIN
        XD()
        XB()
        YMULT(XMLT,S,XM,NCHANL,NK,NCHANL)
        for I in range(NCHANL):
            for J in range(NCHANL):
                XM[I,J]=DELX*SLP*XM[I,J]/A[I]
                #print(XM)
        for II in range(NCHANL):
            for JJ in range(NCHANL):
               if II==JJ:
                  XMI[II,JJ]=THETA*XM[II,JJ]+1
               else:
                  XMI[II,JJ]=THETA*XM[II,JJ]
            print(XMI[II,JJ],"XDFFG") 
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
        print(P1,"P1")
        DCROSS()
        for K in range(NK):
            WIJ1[K]=-WIJ1[K]
        for I in range(NCHANL):
            F11[I]=F1[I]
        MASFLO()
        for I in range(NCHANL):
            ERROR[I]=abs((F11[I]-F1[I])/F1[I])
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(NK):
               W2[K]=WIJ1[K]
           DCROSS()
           for K in range(NK):
               WIJ1[K]=GAMA*WIJ1[K]+(1-GAMA)*WIJ0[K]
           for I in range(NCHANL):
               F11[I]=F1[I]
           MASFLO()
           for I in range(NCHANL):
               if F1[I]>=0:
                   ERR[I]=abs((F11[I]-F1[I])/F1[I])
               else:
                   break
        else:
            break
        HM()
    elif i>0:
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
                #print("dzff")
        for I in range(NCHANL):
            SUM=0
            for J in range(NCHANL):
                PM=XM0[I,J]*P0[J]
                SUM=SUM+PM                                                  ## CHECK THIS ALLIGNMENT
            PM0[I]=SUM
            PB[I]=B[I]=+PM0[I]
        gauss(XMI,P1,PB,NCHANL)
        DCROSS()
        for K in range(NK):
            WIJ1[K]=-WIJ1[K]
        for I in range(NCHANL):
            F11[I]=F1[I]
        MASFLO()
        print("DFHH")
        for I in range(NCHANL):
            ERROR[I]=abs((F11[I]-F1[I])/F1[I])
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(NK):
               W2[K]=WIJ1[K]
           DCROSS()
           for K in range(NK):
               WIJ1[K]=GAMA*WIJ1[K]+(1-GAMA)*WIJ0[K]
           for I in range(NCHANL):
               F11[I]=F1[I]
           MASFLO()
           for I in range(NCHANL):
               if F1[I]>=0:
                   ERR[I]=abs((F11[I]-F1[I])/F1[I])
               else:
                   break
        else:
            break
        HM()
        
print(H1[I])           
            