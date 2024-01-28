      PROGRAM SA12
C     SUBCHANNEL ANALYSIS OF 37-ROD CLUSTER FUEL BUNDLE
C     THIS PROGRAM IS FOR THE STEADY STATE CONDITION ONLY
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A6/XMLT(20,20),XM(20,20),XMI(20,20),P0(20),P1(20),PB(20),XM
     10(20,20),PM0(20),F11(20),ERR(20),ERROR(20)
      COMMON/A7/B(20),B1(20),B2(20),SS(20),SAVE(20)
      COMMON/A8/AHDIA(20),AVRE(20),BETA(20),WPR(20)
      COMMON/A9/H0(20),H1(20),HSTAR(20),DELH(20),Q(20),C1(20),C2(20),C3(
     110),XHST(20,20),S5(20,20),XH(20,20),SD(20,20),XDELH(20,20),XHS(20,
     220),HPERI(20),HF(20)
      COMMON/A10/XY(20),XZ(20)
      COMMON/A11/U1(20),XU1(20,20),YU1(20,20),XXU1(20,20),Z1(20),Z2(20)
      OPEN(UNIT=5,FILE='INS12')
      OPEN(UNIT=6,FILE='SA12.RLT')
      READ(5,*)NK,NCHANL,NNODE,SLP,FACK,RHO,VISC,GC,ALPHA,RDIA,AXLN,FT,T
     1HETA,GAMA
      WRITE(6,*)NK,NCHANL,NNODE,SLP,FACK,RHO,VISC,GC,ALPHA,RDIA,AXLN,FT
     1THETA,GAMA 
      READ(5,*) (A(I),I=1,14) 
      READ(5,*)(HDIA(I),I=1,14)
      READ(5,*)(F0(I),I=1,14) 
      READ(5,*)(H0(I),I=1,14) 
      READ(5,*)(HF(I),I=1,14) 
      READ(5,*)(HPERI(I),I=1,14)
      READ(5,*)(GAP(K),K=1,19)
      WRITE(6,5)(A(I),HDIA(I),F0(I),H0(I),HF(I),HPERI(I),I=1,14)
 5    FORMAT(1X,'AREA',15X,'HDIA',15X,'F0(I)',10X,'H0(I)',10X,'HF(I)',10
     1X,'HPERI(I)'/14(6F15.10/))
      WRITE(6,*)('GAP= ',GAP(K),K=1,19) 
      WIJIN=0.0
      PIN=12262500
      WRITE(6,*)'CHANNEL INLET PRESSURE(IN N/SQ METRE)=',PIN
      DO 10 I=1,NCHANL
      F1(I)=F0(I)
 10   P0(I)=PIN
      DO 12 K=1,NK
      WIJ0(K)=WIJIN 
 12   WIJ1(K)=WIJIN 
      CALL SKI
      DELX=AXLN/(NNODE-1)
      WRITE(6,*)'NODE LENGTH(IN METRE)=',DELX
      WRITE(6,*)'TOTAL AXIAL NODE NO.=',NNODE
      WRITE(6,*)'************ FACTOR FT=',FT
      WRITE(6,*)'*********** THETA=',THETA
      WRITE(6,*)'************* GAMA=',GAMA
      WRITE(6,*)'************* DELTA=',DELTA 
      X=0.
      NODE=1Š 100  WRITE(6,*)'**************************** CHANNLE AXIAL LENGTH=',X
      WRITE(*,*)'AXIAL LENGTH=',X
      WRITE(*,*)'NODE= ',NODE
      WRITE(6,*)'NODE= ',NODE
C16   WRITE(6,*)'****************************************ITERATION=',IT
      CALL XD
      CALL XB
      CALL YMULT(XMLT,S,XM,NCHANL,NK,NCHANL)
      DO 13 I=1,NCHANL
      DO 13 J=1,NCHANL
 13   XM(I,J)=DELX*SLP*XM(I,J)/A(I)
      DO 20 II=1,NCHANL
      DO 20 JJ=1,NCHANL
      IF(II.EQ.JJ) THEN
          XMI(II,JJ)=THETA*XM(II,JJ)+1. 
      ELSE
          XMI(II,JJ)=THETA*XM(II,JJ)
      ENDIF
 20   CONTINUE
      DO 40 I=1,NCHANL
      DO 40 J=1,NCHANL
 40   XM0(I,J)=XMI(I,J)-XM(I,J)
      DO 41 I=1,NCHANL
      SUM=0.
      DO 42 J=1,NCHANL
      PM=XM0(I,J)*P0(J)
 42   SUM=SUM+PM
      PM0(I)=SUM
 41   PB(I)=B(I)+PM0(I)
C     WRITE(6,*)('PB=',PB(I),I=1,NCHANL)
      CALL GAUSS(XMI,P1,PB,NCHANL)
C     WRITE(6,50)(P1(I),I=1,NCHANL)
C50   FORMAT(1X,'P1=',2(7E15.8,2X/))
      CALL DCROSS
      DO 52 K=1,NK
 52   WIJ1(K)=-WIJ1(K)
      DO 51 I=1,NCHANL
 51   F11(I)=F1(I)
      CALL MASFLO
      DO 70 I=1,NCHANL
 70   ERROR(I)=ABS((F11(I)-F1(I))/F1(I))
      DO 69 I=1,NCHANL
      IF(ERROR(I).GT.ERROR(I+1)) THEN
         EMAX=ERROR(I)
      ELSE
         EMAX=ERROR(I+1)
      ENDIF
 69   CONTINUE
      IF(EMAX.GT.1.E-02) THEN 
         GO TO 999
      ELSE
         GO TO 200
      ENDIF
 999  CONTINUE
C     ******************************************************ŠC     SPECIAL ITERATIVE SCHEME TO CONVERGE AXIAL MASS FLOW
      IT=0
 1000 CONTINUE
      IT=IT+1
      CALL AXIMOM
      DO 66 K=1,NK
 66   W2(K)=WIJ1(K) 
      CALL DCROSS
      DO 67 K=1,NK
 67   WIJ1(K)=GAMA*WIJ1(K)+(1-GAMA)*WIJ0(K)
      DO 71 I=1,NCHANL
 71   F11(I)=F1(I)
      CALL MASFLO
      DO 72 I=1,NCHANL
      IF(F1(I).LE.0.) GO TO 99
 72   ERR(I)=ABS((F1(I)-F11(I))/F1(I))
      DO 73 I=1,NCHANL
      IF(ERR(I).GE.ERR(I+1))THEN
         ERRMAX=ERR(I)
      ELSE
         ERRMAX=ERR(I+1)
      ENDIF
 73   CONTINUE
      IF(ERRMAX.LE.1.E-02)THEN
         GO TO 200
      ELSE
         GO TO 1000 
      ENDIF
 200  CONTINUE
      WRITE(6,*)'***************ITERATION = ',IT
      WRITE(6,210)(F1(I),I=1,NCHANL)
 210  FORMAT('AXIAL FLOW='/2(7E15.8,2X/))
      WRITE(6,220)(P1(I),I=1,NCHANL)
 220  FORMAT(1X,'P1=',2(7E15.8,2X/))
C     ***************************************************
      CALL HM
      X=X+DELX
      NODE=NODE+1
      IF(X.GT.AXLN) GO TO 99
      DO 61 I=1,NCHANL
      P0(I)=P1(I)
      F0(I)=F1(I)
 61   H0(I)=H1(I)
      DO 62 K=1,NK
 62   WIJ0(K)=WIJ1(K)
      GO TO 100
 99   STOP
      END 
C   ********************************************************************
C
C    *******************************************************************
      SUBROUTINE XD 
C     COMPUTATION OF MATRIX [D]
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT Š      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      DIMENSION IC(19),JC(19) 
      DATA IC/1,1,2,3,4,3,4,5,6,7,8,9,6,7,9,10,11,12,13/
      DATA JC/2,3,5,4,5,6,8,10,7,8,9,10,11,12,13,14,12,13,14/
C     WRITE(6,*)'SUBROUTINE XD'
      CALL STAR
      DO 10 K=1,NK
      I=IC(K)
      J=JC(K)
      CIJ0(K)=.5*FACK*ABS(WIJ0(K))/(RHO*GAP(K)**2.)
      CIJ1(K)=.5*FACK*ABS(WIJ1(K))/(RHO*GAP(K)**2.)
      D(K)=(USTAR1(K)/DELX)+(SLP*THETA*CIJ1(K))
      USTD1(K)=USTAR1(K)/D(K) 
 10   CONTINUE
C     COMPUTATION OF USTAR MATRIX [XSTD1(K,K)]
      DO 20 KK=1,NK 
      DO 20 II=1,NK 
      IF(KK.EQ.II) THEN
          XUSTD1(KK,II)=USTD1(KK)
      ELSE
          XUSTD1(KK,II)=0.
      ENDIF
 20   CONTINUE
C     WRITE(6,50)(CIJ0(K),CIJ1(K),D(K),USTD1(K),K=1,NK)
C50   FORMAT(1X,5X,'CIJ0',10X,'CIJ1',15X,'D',10X,'USTD1'/20(4E15.8,5X/))
C     WRITE(6,*)'END OF SUB-XD'
      RETURN
      END 
C    ******************************************************************
C
C    ******************************************************************
      SUBROUTINE XXA
C     COMPUTATION OF MATRIX (A')
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A10/XY(20),XZ(20)
C     WRITE(6,*)'SUBROUTINE XXA'
      CALL WPRIM
      DO 10 I=1,NCHANL
      RE(I)=F0(I)*HDIA(I)/(A(I)*VISC)
      FACF(I)=.05052*RE(I)**(-.05719)
      X4=XY(I)
      X1=(F0(I)/A(I))**2.
      X2=.5*FACF(I)/(HDIA(I)*RHO)
      X3=GC*RHO*COS(ALPHA*3.1415927/180.)
      XA(I)=-X1*X2-X3-X4
 10   CONTINUE
C     WRITE(6,50)(RE(I),FACF(I),XA(I),I=1,NCHANL) 
C50   FORMAT(1X,10X,'RE',10X,'FACF',10X,'XA'/1X,20(3E15.8,5X/))
C     WRITE(6,*)'END OF SUB-XXA'Š      RETURN
      END 
C    **************************************************************** 
C
C    **************************************************************** 
      SUBROUTINE SKI
C     COMPUTATION OF CONNECTION MATRIX [S] AND ITS TRANSPOSE [ST]
      COMMON/A1/NK,NCHANL
      COMMON/A5/S(20,20),ST(20,20)
C     COMPUTATION OF S MATRIX 
      INTEGER S,ST
      DIMENSION IC(19),JC(19) 
      DATA IC/1,1,2,3,4,3,4,5,6,7,8,9,6,7,9,10,11,12,13/
      DATA JC/2,3,5,4,5,6,8,10,7,8,9,10,11,12,13,14,12,13,14/
      WRITE(6,*)'SUBROUTINE SKI'
      DO 10 K=1,NK
      DO 20 I=1,NCHANL
      IK=IC(K)
      JK=JC(K)
      S(K,I)=0
      IF(I.EQ.IK) S(K,I)=1
      IF(I.EQ.JK) S(K,I)=-1
 20   CONTINUE
 10   CONTINUE
      WRITE(6,150)((S(K,I),I=1,NCHANL),K=1,NK)
 150  FORMAT(1X,20X,'CONNECTION MATRIX',20X/19(2X,14I2/))
      DO 60 I=1,NCHANL
      DO 60 K=1,NK
 60   ST(I,K)=S(K,I)
      WRITE(6,200)((ST(I,K),K=1,NK),I=1,NCHANL)
 200  FORMAT(1X,20X,'TRANSPOSE OF MATRIX',20X/14(2X,19I2/)) 
C     WRITE(6,*)'END OF SUB-SKI'
      RETURN
      END 
C     ******************************************************************
C
C     ******************************************************************
      SUBROUTINE XMULT(A,B,C,MM,NN,LL)
C     MATRIX MULTIPLICATION [A(M,N)*B(N,L)=C(M,L)],MATRIX [A] INTEGER 
      INTEGER A
      DIMENSION A(20,20),B(20,20),C(20,20)
C     WRITE(6,*)'STARTING OF XMULT'
      DO 10 M=1,MM
      DO 20 L=1,LL
      SUM=0.0
      DO 30 N=1,NN
 30   SUM=SUM+A(M,N)*B(N,L)
      C(M,L)=SUM
 20   CONTINUE
 10   CONTINUE
C     WRITE(6,*)'END OF SUB-XMULT'
      RETURN
      END 
C     **********************************************************************
CŠC     **********************************************************************
      SUBROUTINE YMULT(A,B,C,MM,NN,LL)
C     MATRIX MULTIPLICATION [A(M,N)*B(N,L)=C(M,L)],MATRIX [B] INTEGER 
      INTEGER B
      DIMENSION A(20,20),B(20,20),C(20,20)
C     WRITE(6,*)' STARTING OF SUB-YMULT'
      DO 10 M=1,MM
      DO 20 L=1,LL
      SUM=0.0
      DO 30 N=1,NN
 30   SUM=SUM+A(M,N)*B(N,L)
      C(M,L)=SUM
 20   CONTINUE
 10   CONTINUE
C     WRITE(6,*)'END OF SUB-YMULT'
      RETURN
      END 
C     *************************************************************
C
C     *******************************************************************
      SUBROUTINE GAUSS(AG,XG,YG,IG)
C     SOLUTION OF LINEAR EQUATION BY GAUSS-SEIDEL PROCEDURE 
      DIMENSION AG(20,20),XG(20),YG(20),XG1(20),ERR(20)
C     WRITE(6,*)'SUBROUTINE GAUSS'
      DO 102 I=1,IG 
      XG1(I)=.12E08 
 102  XG(I)=0.
      ITER=1
 103  CONTINUE
      DO 104 I=1,IG 
      AP=YG(I)
      DO 105 J=1,IG 
      IF((I-J).EQ.0) THEN
         GO TO 105
      ELSE
         AP=AP-AG(I,J)*XG(J)
      ENDIF
 105  CONTINUE
      XG(I)=AP/AG(I,I)
 104  CONTINUE
      DO 111 I=1,IG 
 111  ERR(I)=ABS(XG(I)-XG1(I))/XG(I)
      DO 112 I=1,IG 
      IF(ERR(I).GT.ERR(I+1)) THEN
         ERRMAX=ERR(I)
      ELSE
         ERRMAX=ERR(I+1)
      ENDIF
 112  CONTINUE
      IF(ERRMAX.LE.1.E-08) GO TO 108
      DO 106 I=1,IG 
 106  XG1(I)=XG(I)
      ITER=ITER+1
      GO TO 103
 108  WRITE(6,*)'ITERATION=',ITERŠ      WRITE(*,*)'ITERATION=',ITER
C     WRITE(6,109)(XG(I),I=1,IG)
C109  FORMAT(10X,'XG='/,2(10E13.6,/))
C     WRITE(6,*)'END OF SUB-GAUSS'
      RETURN
      END 
C     ******************************************************************
C
C     ******************************************************************
      SUBROUTINE XB 
C     COMPUTATION OF MATRIX (B)
      COMMON/A1/NK,NCHANL
      INTEGER S,ST
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A6/XMLT(20,20),XM(20,20),XMI(20,20),P0(20),P1(20),PB(20),XM
     10(20,20),PM0(20),P11(20),ERR(20),ERROR(20)
      COMMON/A7/B(20),B1(20),B2(20),SS(20),SAVE(20)
      COMMON/A10/XY(20),XZ(20)
C     WRITE(6,*)'SUBROUTINE XB'
      CALL XMULT(ST,XUSTD1,XMLT,NCHANL,NK,NK)
      DO 20 K=1,NK
      SAVE1=USTAR0(K)*WIJ0(K)/DELX
      SAVE2=SLP*(1-THETA)*CIJ0(K)*WIJ0(K)
 20   SAVE(K)=SAVE1-SAVE2
      DO 30 I=1,NCHANL
      SUM=0.0
      DO 40 K=1,NK
 40   SUM=SUM+XMLT(I,K)*SAVE(K)
      SS(I)=SUM
 30   CONTINUE
C     WRITE(6,*)('SAVE(K)=',SAVE(K),K=1,NK)
C     WRITE(6,*)('SS(I)=',SS(I),I=1,NCHANL)
      CALL XXA
      DO 45 I=1,NCHANL
      B1(I)=DELX*SS(I)/A(I)
      B2(I)=2.*(F1(I)-F0(I))*(F1(I)/A(I)/RHO)/A(I)
      B(I)=DELX*XA(I)-B1(I)-B2(I)
 45   CONTINUE
C     WRITE(6,50)(B1(I),B2(I),B(I),I=1,NCHANL)
C50   FORMAT(1X,5X,'B1',15X,'B2',15X,'B'/1X,20(3E15.8,2X/)) 
C     WRITE(6,*)'END OF SUB-XB'
      RETURN
      END 
C     *********************************************************************
C
C     *********************************************************************
      SUBROUTINE WPRIM
C     COMPUTATION OF TURBULENT CROSS FLOW (WIJ')
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT Š      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A8/AHDIA(20),AVRE(20),BETA(20),WPR(20)
      COMMON/A10/XY(20),XZ(20)
      DIMENSION IC(19),JC(19) 
      DATA IC/1,1,2,3,4,3,4,5,6,7,8,9,6,7,9,10,11,12,13/
      DATA JC/2,3,5,4,5,6,8,10,7,8,9,10,11,12,13,14,12,13,14/
C     WRITE(6,*)'SUBROUTINE WPRIM'
      DO 10 K=1,NK
      I=IC(K)
      J=JC(K)
      AHDIA(K)=.5*(HDIA(I)+HDIA(J))
      AVRE(K)=.5*(F1(I)/A(I)+F1(J)/A(J))*AHDIA(K)/VISC
      BETA(K)=.0018*(AVRE(K)**(-.1))*(AHDIA(K)/GAP(K))*((GAP(K)/RDIA)**(
     1-.4))
      WPR(K)=BETA(K)*GAP(K)*AVRE(K)*VISC/AHDIA(K) 
 10   XZ(K)=(F1(I)/A(I)-F1(J)/A(J))*WPR(K)/RHO
      DO 30 I=1,NCHANL
      SUM=0.
      DO 40 K=1,NK
 40   SUM=SUM+ST(I,K)*XZ(K)
 30   XY(I)=FT*SUM/A(I)
C     WRITE(6,299)(BETA(K),WPR(K),XY(K),K=1,NK)
C299  FORMAT(1X,'BETA=',10X,'WPRIM=',10X,'XY'/,19(3E13.6,10X/))
C     WRITE(6,*)'END OF SUB-WPRIM'
      RETURN
      END 
C     ******************************************************************
C
C     *******************************************************************
      SUBROUTINE HM 
C     COMPUTATION OF ENTHALPY(H1) AND MASS FLOW(F1)
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A6/XMLT(20,20),XM(20,20),XMI(20,20),P0(20),P1(20),PB(20),XM
     10(20,20),PM0(20),P11(20),ERR(20),ERROR(20)
      COMMON/A7/B(20),B1(20),B2(20),SS(20),SAVE(20)
      COMMON/A8/AHDIA(20),AVRE(20),BETA(20),WPR(20)
      COMMON/A9/H0(20),H1(20),HSTAR(20),DELH(20),Q(20),C1(20),C2(20),C3(
     110),XHST(20,20),S5(20,20),XH(20,20),SD(20,20),XDELH(20,20),XHS(20,
     220),HPERI(20),HF(20)
      DIMENSION IC(19),JC(19) 
      DATA IC/1,1,2,3,4,3,4,5,6,7,8,9,6,7,9,10,11,12,13/
      DATA JC/2,3,5,4,5,6,8,10,7,8,9,10,11,12,13,14,12,13,14/
      WRITE(6,*)'STARTING OF SUBROUTINE HMW'
      DO 10 K=1,NK
      I=IC(K)
      J=JC(K)
      HSTAR(K)=.5*(H0(I)+H0(J))
      DELH(K)=H0(I)-H0(J)Š 10   CONTINUE
      DO 60 II=1,NK 
      DO 60 JJ=1,NK 
      IF(II.EQ.JJ)THEN
         XDELH(II,JJ)=DELH(II)
         XHS(II,JJ)=HSTAR(II) 
      ELSE
         XDELH(II,JJ)=0
         XHS(II,JJ)=0
      ENDIF
 60   CONTINUE
      DO 110 II=1,NCHANL
      DO 110 JJ=1,NCHANL
      IF(II.EQ.JJ)THEN
         XH(II,JJ)=H0(I)
      ELSE
         XH(II,JJ)=0.
      ENDIF
 110  CONTINUE
      CALL XMULT(ST,XHS,S5,NCHANL,NK,NK)
      CALL XMULT(ST,XDELH,SD,NCHANL,NK,NK)
      CALL YMULT(XH,ST,XHST,NCHANL,NCHANL,NK)
      DO 200 I=1,NCHANL
      Q(I)=HF(I)*HPERI(I)
 200  C1(I)=Q(I)*DELX/F1(I)
      DO 210 II=1,NCHANL
      SUM3=0.
      SUM4=0.
      DO 220 KK=1,NK
      S3=XHST(II,KK)*WIJ1(KK) 
      SS3=S5(II,KK)*WIJ1(KK)
      S3=S3-SS3
      S4=SD(II,KK)*WPR(KK)
      SUM3=SUM3+S3
      SUM4=SUM4+S4
      C2(II)=SUM4*DELX/F1(II) 
      C3(II)=SUM3*DELX/F1(II) 
 220  CONTINUE
 210  CONTINUE
C     WRITE(6,*)('C1(II)',C1(II),'C2(II)=',C2(II),'C3(II)=',C3(II),II=1,
C    1NCHANL)
      DO 250 I=1,NCHANL
 250  H1(I)=H0(I)+C1(I)-C2(I)+C3(I)
      WRITE(6,260)(H1(I),I=1,NCHANL)
 260  FORMAT(1X,'H1=',2X,2(7E15.8/))
C     WRITE(6,*)'END OF SUB-HMW'
      RETURN
      END 
C     *************************************************************
C
C     *************************************************************
      SUBROUTINE DCROSS
C     CALCULATION OF DIVERSION CROSS FLOW (WIJ1) & AXIAL MASS FLOW (F1)
      INTEGER S,ST
      COMMON/A1/NK,NCHANLŠ      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A6/XMLT(20,20),XM(20,20),XMI(20,20),P0(20),P1(20),PB(20),XM
     10(20,20),PM0(20),P11(20),ERR(20),ERROR(20)
      DO 310 K=1,NK 
      SP1=USTAR0(K)*WIJ0(K)/DELX
      SP2=SLP*(1-THETA)*CIJ0(K)*WIJ0(K) 
      SUM3=0.
      SUM4=0.
      DO 320 I=1,NCHANL
      SP3=S(K,I)*P1(I)
      SP4=S(K,I)*P0(I)
      SUM3=SUM3+SP3 
 320  SUM4=SUM4+SP4 
      SP3=SLP*THETA*SUM3
      SP4=SLP*(1-THETA)*SUM4
C     WRITE(6,*)' SP1=',SP1,' SP2=',SP2,' SP3=',SP3,' SP4=',SP4
 310  WIJ1(K)=(SP1-SP2+SP3+SP4)/D(K)
      WRITE(6,330)(WIJ1(K),K=1,NK)
 330  FORMAT(1X,'WIJ1='/,2X,10E13.6/9E13.6)
      RETURN
      END 
C     *****************************************************************
C
C     *****************************************************************
      SUBROUTINE MASFLO
C     CALCULATION OF CHANNEL MASS FLOW (F1)
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      DO 340 I=1,NCHANL
      SUM=0.
      DO 350 K=1,NK 
      SW=ST(I,K)*WIJ1(K)
      SUM=SUM+SW
 350  F1(I)=F0(I)-(DELX*SUM)
 340  CONTINUE
      SUM=0.
      DO 360 I=1,NCHANL
 360  SUM=SUM+F1(I) 
      FTOTAL=SUM
      WRITE(6,400)(F1(I),I=1,NCHANL)
 400  FORMAT(1X,'AXIAL MASS FLOW(F1)'/1X,2(7E13.6/))
      WRITE(6,*)'***** TOTAL MASS FLOW= ',FTOTAL
      RETURN
      END 
C     *************************************************************** 
C
C     *************************************************************** Š      SUBROUTINE AXIMOM
C     COMPUTATION OF NODE EXIT PRESSURE BY USING AXIAL MOMENTUM EQUATION
C     DIRECTLY
      INTEGER S,ST
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)
      COMMON/A5/S(20,20),ST(20,20)
      COMMON/A6/XMLT(20,20),XM(20,20),XMI(20,20),P0(20),P1(20),PB(20),XM
     10(20,20),PM0(20),P11(20),ERR(20),ERROR(20)
      COMMON/A10/XY(20),XZ(20)
      COMMON/A11/U1(20),XU1(20,20),YU1(20,20),XXU1(20,20),Z1(20),Z2(20)
      WRITE(6,*)'STARTING OF SUB-AXIMOM'
      CALL STAR
      DO 10 I=1,NCHANL
 10   U1(I)=F1(I)/A(I)/RHO
      DO 20 I=1,NCHANL
      DO 20 J=1,NCHANL
      IF(I.EQ.J) THEN
         XU1(I,J)=U1(I)
      ELSE
         XU1(I,J)=0.0
      ENDIF
 20   CONTINUE
      CALL YMULT(XU1,ST,YU1,NCHANL,NCHANL,NK)
      CALL XMULT(ST,XUST1,XXU1,NCHANL,NK,NK)
      DO 30 I=1,NCHANL
      SUM1=0.
      SUM2=0.
      DO 40 K=1,NK
      SUM1=SUM1+YU1(I,K)*WIJ1(K)
 40   SUM2=SUM2+XXU1(I,K)*WIJ1(K)
      Z1(I)=2.*DELX*SUM1/A(I) 
      Z2(I)=DELX*SUM2/A(I)
C     WRITE(6,*)' Z1=',Z1(I),' Z2=',Z2(I)
 30   CONTINUE
      DO 45 I=1,NCHANL
      P1(I)=P0(I)+DELX*XA(I)+Z1(I)-Z2(I)
 45   P1(I)=DELTA*P1(I)+(1-DELTA)*P1(I)
      WRITE(6,50)(P1(I),I=1,NCHANL)
 50   FORMAT(1X,'P1=',2(7E15.8,2X/))
      WRITE(6,*)'END OF SUB-AXIMOM'
      RETURN
      END 
C     *************************************************************
C
C     *************************************************************
      SUBROUTINE STAR
      COMMON/A1/NK,NCHANL
      COMMON/A2/GAP(20),SLP,FACK,RHO,VISC,DELX,GC,ALPHA,RDIA,THETA,FT 
      COMMON/A3/A(20),HDIA(20),F1(20),F0(20),RE(20),FACF(20),XA(20)
      COMMON/A4/CIJ0(20),CIJ1(20),WIJ1(20),WIJ0(20),USTAR0(20),XUST0(20,
     120),D(20),USTAR1(20),XUST1(20,20),USTD1(20),XUSTD1(20,20),W2(20)Š      DIMENSION IC(19),JC(19) 
      DATA IC/1,1,2,3,4,3,4,5,6,7,8,9,6,7,9,10,11,12,13/
      DATA JC/2,3,5,4,5,6,8,10,7,8,9,10,11,12,13,14,12,13,14/
C     WRITE(6,*)'STARTING OF SUB-STAR'
      DO 5 K=1,NK
      I=IC(K)
      J=JC(K)
      IF(WIJ1(K)) 10,20,30
 10   USTAR1(K)=F1(J)/(A(J)*RHO)
      GO TO 5
 20   USTAR1(K)=.5*((F1(I)/(A(I)*RHO))+(F1(J)/(A(J)*RHO)))
      GO TO 5
 30   USTAR1(K)=F1(I)/(A(I)*RHO)
 5    CONTINUE
      DO 40 K=1,NK
      I=IC(K)
      J=JC(K)
      IF(WIJ0(K)) 50,60,70
 50   USTAR0(K)=F0(J)/(A(J)*RHO)
      GO TO 40
 60   USTAR0(K)=.5*((F0(I)/(A(I)*RHO))+(F0(J)/(A(J)*RHO)))
      GO TO 40
 70   USTAR0(K)=F0(I)/(A(I)*RHO)
 40   CONTINUE
C     COMPUTATION OF USTAR MATRIX [U0*]&[U1*]
      DO 80 KK=1,NK 
      DO 80 II=1,NK 
      IF(KK.EQ.II) THEN
          XUST0(KK,II)=USTAR0(KK)
          XUST1(KK,II)=USTAR1(KK)
      ELSE
          XUST0(KK,II)=0.
          XUST1(KK,II)=0.
      ENDIF
 80   CONTINUE
C     WRITE(6,90)(USTAR0(K),USTAR1(K),K=1,NK)
C90   FORMAT(1X,5X,'USTAR0',10X,'USTAR1'/20(2E15.8,5X/))
      RETURN
      END 
