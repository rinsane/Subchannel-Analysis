from FUNCTIONS import sub_routines

dum = sub_routines()

NODE = [sub_routines() for _ in range(dum.NNODE)]

for i in range(dum.NNODE):
    if i == 0:
        for I in range(dum.NCHANL):
            NODE[i].F1[I] = NODE[i].F0[I]
            NODE[i].P0[I] = NODE[i].PIN
            print(NODE[i].P0[I])
        print("FGfg")

        for K in range(dum.NK):
            NODE[i].WIJ0[K] = NODE[i].WIJIN
            NODE[i].WIJ1[K] = NODE[i].WIJIN
        XD()
        XB()
        YMULT(NODE[i].XMLT,S,NODE[i].XM,dum.NCHANL,dum.NK,dum.NCHANL)
        
        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM[I,J]=NODE[i].DELX*dum.SLP*NODE[i].XM[I,J]/A[I]
                #print(NODE[i].XM)
        
        for II in range(dum.NCHANL):
            for JJ in range(dum.NCHANL):
               if II==JJ:
                  XMI[II,JJ]=THETA*NODE[i].XM[II,JJ]+1
               else:
                  XMI[II,JJ]=THETA*NODE[i].XM[II,JJ]
            print(XMI[II,JJ],"XDFFG") 
        
        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
              XM0[I,J]=XMI[I,J]-NODE[i].XM[I,J]
            
        
        for I in range(dum.NCHANL):
            SUM=0
            for J in range(dum.NCHANL):
                PM=XM0[I,J]*NODE[i].P0[J]
            SUM=SUM+PM
            PM0[I]=SUM
            PB[I]=B[I]+PM0[I]
        
        gauss(XMI, P1, PB, dum.NCHANL)
        print(P1,"P1")
        DCROSS()
        
        for K in range(dum.NK):
            NODE[i].WIJ1[K]=-NODE[i].WIJ1[K]
        
        for I in range(dum.NCHANL):
            F11[I]=NODE[i].F1[I]
        MASFLO()
        
        for I in range(dum.NCHANL):
            ERROR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
        
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(dum.NK):
               W2[K]=NODE[i].WIJ1[K]
           DCROSS()
           for K in range(dum.NK):
               NODE[i].WIJ1[K]=GAMA*NODE[i].WIJ1[K]+(1-GAMA)*NODE[i].WIJ0[K]
           for I in range(dum.NCHANL):
               F11[I]=NODE[i].F1[I]
           MASFLO()
           for I in range(dum.NCHANL):
               if NODE[i].F1[I]>=0:
                   ERR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
               else:
                   break
        else:
            break
        HM()
    
    else:
        XD()
        XB()
        YMULT(NODE[i].XMLT,S,NODE[i].XM,dum.NCHANL,dum.NK,dum.NCHANL)
        
        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM[I,J]=NODE[i].DELX*dum.SLP*NODE[i].XM[I,J]/A[I]
        
        for II in range(dum.NCHANL):
            for JJ in range(dum.NCHANL):
                if II==JJ:
                    XMI[II,JJ]=THETA*NODE[i].XM[II,JJ]+1
                else:
                    XMI[II,JJ]=THETA*NODE[i].XM[II,JJ]
                    
        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                XM0[I,J]=XMI[I,J]-NODE[i].XM[I,J]
                #print("dzff")
        
        for I in range(dum.NCHANL):
            SUM=0
            for J in range(dum.NCHANL):
                PM=XM0[I,J]*NODE[i].P0[J]
                SUM=SUM+PM                                                  ## CHECK THIS ALLIGNMENT
            PM0[I]=SUM
            PB[I]=B[I]=+PM0[I]
        gauss(XMI,P1,PB,dum.NCHANL)
        DCROSS()
        
        for K in range(dum.NK):
            NODE[i].WIJ1[K]=-NODE[i].WIJ1[K]
        
        for I in range(dum.NCHANL):
            F11[I]=NODE[i].F1[I]
        MASFLO()
        print("DFHH")
        
        for I in range(dum.NCHANL):
            ERROR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
        
        if ERROR[I]>=0.01:                                              ## CHECK ALIGNMENT HERE
           AXIMOM()
           for K in range(dum.NK):
               W2[K]=NODE[i].WIJ1[K]
           DCROSS()
           for K in range(dum.NK):
               NODE[i].WIJ1[K]=GAMA*NODE[i].WIJ1[K]+(1-GAMA)*NODE[i].WIJ0[K]
           for I in range(dum.NCHANL):
               F11[I]=NODE[i].F1[I]
           MASFLO()
           for I in range(dum.NCHANL):
               if NODE[i].F1[I]>=0:
                   ERR[I]=abs((F11[I]-NODE[i].F1[I])/NODE[i].F1[I])
               else:
                   break
        else:
            break
        
        HM()