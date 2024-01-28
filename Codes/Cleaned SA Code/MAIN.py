from input_zero import *
from FUNCTIONS import sub_routines

dum = sub_routines()

NODE = [sub_routines() for _ in range(dum.NNODE)]

for i in range(len(NODE)):
    if i == 0:
        for I in range(NODE[i].NCHANL):
            NODE[i].F1[I] = NODE[i].F0[I]
            NODE[i].P0[I] = NODE[i].PIN
            print(NODE[i].P0[I])
        print("FGfg")
        for K in range(NODE[i].NK):
            NODE[i].WIJ0[K] = NODE[i].WIJIN
            NODE[i].WIJ1[K] = NODE[i].WIJIN
        XD()
        XB()
        YMULT(XMLT,S,XM,NODE[i].NCHANL,NODE[i].NK,NODE[i].NCHANL)
        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
                XM[I,J]=DELX*SLP*XM[I,J]/A[I]
                #print(XM)
        for II in range(NODE[i].NCHANL):
            for JJ in range(NODE[i].NCHANL):
               if II==JJ:
                  XMI[II,JJ]=THETA*XM[II,JJ]+1
               else:
                  XMI[II,JJ]=THETA*XM[II,JJ]
            print(XMI[II,JJ],"XDFFG") 
        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
              XM0[I,J]=XMI[I,J]-XM[I,J]
            
        for I in range(NODE[i].NCHANL):
            SUM=0
            for J in range(NODE[i].NCHANL):
                PM=XM0[I,J]*NODE[i].P0[J]
            SUM=SUM+PM
            PM0[I]=SUM
            PB[I]=B[I]+PM0[I]
        
        gauss(XMI, P1, PB, NODE[i].NCHANL)
        print(P1,"P1")
        DCROSS()
        for K in range(NODE[i].NK):
            NODE[i].WIJ1[K]=-NODE[i].WIJ1[K]
        for I in range(NODE[i].NCHANL):
            F11[I]=NODE[i].F1[I]
        MASFLO()
        for I in range(NODE[i].NCHANL):
            ERROR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(NODE[i].NK):
               W2[K]=NODE[i].WIJ1[K]
           DCROSS()
           for K in range(NODE[i].NK):
               NODE[i].WIJ1[K]=GAMA*NODE[i].WIJ1[K]+(1-GAMA)*NODE[i].WIJ0[K]
           for I in range(NODE[i].NCHANL):
               F11[I]=NODE[i].F1[I]
           MASFLO()
           for I in range(NODE[i].NCHANL):
               if NODE[i].F1[I]>=0:
                   ERR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
               else:
                   break
        else:
            break
        HM()
    elif i>0:
        XD()
        XB()
        YMULT(XMLT,S,XM,NODE[i].NCHANL,NODE[i].NK,NODE[i].NCHANL)
        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
                XM[I,J]=DELX*SLP*XM[I,J]/A[I]
        for II in range(NODE[i].NCHANL):
            for JJ in range(NODE[i].NCHANL):
                if II==JJ:
                    XMI[II,JJ]=THETA*XM[II,JJ]+1
                else:
                    XMI[II,JJ]=THETA*XM[II,JJ]
                    
        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
                XM0[I,J]=XMI[I,J]-XM[I,J]
                #print("dzff")
        for I in range(NODE[i].NCHANL):
            SUM=0
            for J in range(NODE[i].NCHANL):
                PM=XM0[I,J]*NODE[i].P0[J]
                SUM=SUM+PM                                                  ## CHECK THIS ALLIGNMENT
            PM0[I]=SUM
            PB[I]=B[I]=+PM0[I]
        gauss(XMI,P1,PB,NODE[i].NCHANL)
        DCROSS()
        for K in range(NODE[i].NK):
            NODE[i].WIJ1[K]=-NODE[i].WIJ1[K]
        for I in range(NODE[i].NCHANL):
            F11[I]=NODE[i].F1[I]
        MASFLO()
        print("DFHH")
        for I in range(NODE[i].NCHANL):
            ERROR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(NODE[i].NK):
               W2[K]=NODE[i].WIJ1[K]
           DCROSS()
           for K in range(NODE[i].NK):
               NODE[i].WIJ1[K]=GAMA*NODE[i].WIJ1[K]+(1-GAMA)*NODE[i].WIJ0[K]
           for I in range(NODE[i].NCHANL):
               F11[I]=NODE[i].F1[I]
           MASFLO()
           for I in range(NODE[i].NCHANL):
               if NODE[i].F1[I]>=0:
                   ERR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
               else:
                   break
        else:
            break
        HM()
        
print(H1[I])   