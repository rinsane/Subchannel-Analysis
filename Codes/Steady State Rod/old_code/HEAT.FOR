$DEBUG        
        PROGRAM MAIN
c      This elementary code has the following features

c   1. It is written for a ring pellet with id and od. The same can be
c       used for a solid fuel by defining a very small Inner radius (RIF).
c       Rof is the outer radius of the pellet. This has to fed in the data
c       statement. All lengths in (m)
c   2.  The program starts with 300 K as initial temperature at TIN and goes
c       on to fine the temperature at TMAX with a time step of DELT
c       This is taken care of by the NSTART = 1.
c       This needs modification if you want to change the logic.
c   3.  All the inputs are through DATA statements
c   4.  There are only four data statements. Two in main and two in FUEL
c   5.  Definitions are as given below.

c       NF= number of fuel nodes, NC= number of clad nodes
c       GT gap thickness (gas),  CT Clad thickness.
c       DELTAF=Common ratio parameter used for grids in fuel- keep it as it is
c       DELTAC=Common ratio parameter used for grids in clad- keep it as it is
c       QPR= qprim (watts/m)
c       TINF= bulk fluid temperature (Kelvin)
C       HINF= Heat transfer coefficient (W/m^2-K)
c       HG= Gap conductance (W/m^2-K)

c       Properties functions are given at the end

        implicit double precision(a-h,o-z)

        DATA QPR,TINF,HINF,HG /50200.,544.15,5.962D4,0.852D4/
        DATA TIN,DELT,TMAX /0.0,100000.,900000./
        CALL FUEL(TIN,DELT,TMAX,QPR,TINF,HINF,HG)
        STOP
        END

        SUBROUTINE FUEL(TIN,DELT,TMAX,QPR,TINF,HINF,HG)
        implicit double precision(a-h,o-z)
        DIMENSION R(25),H(25),G(25),S(25),AA(25,3),C(25),RHO(25),
     1  CP(25),Q3PRIM(25),AK(25),T0(25),T1(25)
        COMMON/RAD/NF,NC,ROF,RIF,GT,CT,DELTAF,DELTAC
        DATA NF,NC,ROF,RIF,GT,CT,DELTAF,DELTAC /8,4,7.15D-3,1d-20,
     1  5.9D-5,4.00D-4,0.8,1./
        DATA NSTART /1/
        T=TIN+DELT
C  ****** COMPUTE RADIEI ****
        CALL RADIUS(R)
C  ****** TEMPERATURE AND HEAT FLUX INITIALIZATION ***        
        DO 10 I=2,NF+1
10      Q3PRIM(I)=QPR/(3.1416*ROF*ROF)
        DO 13 I=NF+4,NF+NC+3
13      Q3PRIM(I)=0.
          IF (NSTART.EQ.1) THEN
          DO 11 I=2,NF+1
11        T0(I)=300.
          T0(1)=T0(2)
          T0(NF+2)=T0(NF+1)
          DO 12 I=NF+4,NF+NC+3
12        T0(I)=300.
          T0(NF+3)=T0(NF+4)
          T0(NF+NC+4)=T0(NF+NC+3)
          ELSE
          READ(*,*) (T0(I),I=1,NF+NC+4)
          ENDIF


C  ***** COMPUTATION OF PROPERTIES ****
15      DO 16 I=1,NF+1
        TEMP=(T0(I)+T0(I+1))/2.
16      AK(I)=EKF(TEMP)
        DO 17 I=2,NF+1
        RHO(I)=DENF(T0(I))
17      CP(I)=CPF(T0(I))
        DO 18 I=NF+3,NF+NC+3
        TEMP=(T0(I)+T0(I+1))/2.
18      AK(I)=EKC(TEMP)
        DO 19 I=NF+4,NF+NC+3
        RHO(I)=DENC(T0(I))
19      CP(I)=CPC(T0(I))

C  ****** COMPUTE CONSTANTS ******
        DO 30 I=2,NF
        H(I)=R(I)*AK(I)/((R(I+1)-R(I-1))/2.)
        RIIMUN1=(R(I)+R(I-1))/2.
        DELRI=R(I)-R(I-1)
        S(I)=Q3PRIM(I)*RIIMUN1*DELRI
30      G(I)=RHO(I)*CP(I)*RIIMUN1*DELRI/DELT
        DO 40 I=NF+4,NF+NC+2
        H(I)=R(I)*AK(I)/((R(I+1)-R(I-1))/2.)
        RIIMUN1=(R(I)+R(I-1))/2.
        DELRI=R(I)-R(I-1)
        S(I)=Q3PRIM(I)*RIIMUN1*DELRI
40      G(I)=RHO(I)*CP(I)*RIIMUN1*DELRI/DELT
        H(1)=R(1)*AK(1)/(R(2)-R(1))
        H(NF+1)=R(NF+1)*AK(NF+1)/(R(NF+1)-R(NF))
        RIIMUN1=(R(NF+1)+R(NF))/2.
        DELRI=R(NF+1)-R(NF)
        G(NF+1)=RHO(NF+1)*CP(NF+1)*RIIMUN1*DELRI/DELT
        S(NF+1)=Q3PRIM(NF+1)*RIIMUN1*DELRI
        H(NF+3)=R(NF+3)*AK(NF+3)/(R(NF+4)-R(NF+3))
        H(NF+NC+3)=R(NF+NC+3)*AK(NF+NC+3)/(R(NF+NC+3)-R(NF+NC+2))
        RIIMUN1=(R(NF+NC+3)+R(NF+NC+2))/2.
        DELRI=R(NF+NC+3)-R(NF+NC+2)
        G(NF+NC+3)=RHO(NF+NC+3)*CP(NF+NC+3)*RIIMUN1*DELRI/DELT
        S(NF+NC+3)=Q3PRIM(NF+NC+3)*RIIMUN1*DELRI
C  ****** COMPUTATION OF TRIDIAGONAL COEFFICIENTS FOR INT. NODES ****
        DO 50 I=2,NF+1
        AA(I,1)=H(I-1)
        AA(I,3)=H(I)
        AA(I,2)=-AA(I,1)-AA(I,3)-G(I)
50      C(I)=-T0(I)*G(I)-S(I)
        DO 60 I=NF+4,NF+NC+3
        AA(I,1)=H(I-1)
        AA(I,3)=H(I)
        AA(I,2)=-AA(I,1)-AA(I,3)-G(I)
60      C(I)=-T0(I)*G(I)-S(I)

C Boundry condition is of the type A1*dT/dx+A2*T=A3
C  ******TREATMENT OF BOUNDARY NODES *****
        A1=1.
        B1=0.
        C1=0.
        P1=A1/(R(2)-R(1))
        AA(1,2)=(-P1+B1/2.)
        AA(1,3)=(P1+B1/2.)
        C(1)=0.
C  ***
        HFR=HG*R(NF+1)
        P1=(R(NF+1)*AK(NF+1))/(R(NF+1)-R(NF))
        BNF2=(P1-HFR/2.)
        DNF2=-P1-HFR/2.
        ANF2=HFR/2.
        XNF2=HFR/2.
        P1=R(NF+3)*AK(NF+3)/(R(NF+4)-R(NF+3))
        ANF3=P1-HFR/2.
        BNF3=HFR/2.
        DNF3=-P1-HFR/2.
        YNF3=HFR/2.
        AA(NF+2,1)=BNF2/XNF2*ANF3-YNF3
        AA(NF+2,2)=DNF2/XNF2*ANF3-BNF3
        AA(NF+2,3)=ANF2/XNF2*ANF3-DNF3
        C(NF+2)=0.
        AA(NF+3,1)=BNF3/YNF3*BNF2-DNF2
        AA(NF+3,2)=DNF3/YNF3*BNF2-ANF2
        AA(NF+3,3)=ANF3/YNF3*BNF2-XNF2
        C(NF+3)=0.
C  ****
        AL=-AK(NF+NC+3)
        BL=-HINF
        CL=-HINF*TINF
        P1=AL/(R(NF+NC+3)-R(NF+NC+2))
        AA(NF+NC+4,1)=-P1+BL/2.
        AA(NF+NC+4,2)=P1+BL/2.
        C(NF+NC+4)=CL
C  ******COMPUTATION OF TEMPERATURES ****
        CALL THOMAS(NF+NC+4,AA,C,T1)
C  ****** SETUP FOR NEXT TIME STEP
        DO 110 I=1,NF+NC+4
110     T0(I)=T1(I)
        T=T+DELT
        IF(T.GT.TMAX)GOTO 999
        WRITE(*,100)(T1(1)+T1(2))/2.,(T1(I),I=2,NF+1),(T1(NF+1)+
     1  T1(NF+2))/2.,(T1(NF+3)+T1(NF+4))/2.,(T1(I),I=NF+4,NF+NC+3),
     2  (T1(NF+NC+3)+T1(NF+NC+4))/2.
        GOTO 15
999     CONTINUE
        WRITE(*,100)(T1(1)+T1(2))/2.,(T1(I),I=2,NF+1),(T1(NF+1)+
     1  T1(NF+2))/2.,(T1(NF+3)+T1(NF+4))/2.,(T1(I),I=NF+4,NF+NC+3),
     2  (T1(NF+NC+3)+T1(NF+NC+4))/2.
100     FORMAT(10(1X,F8.2,1X))
        RETURN
        END
C  ******
C
C  ****** THIS SUBROUTINE COMPUTES RADIEI OF NODES *****
        SUBROUTINE RADIUS(R)
        implicit double precision(a-h,o-z)
        DIMENSION R(25)
        COMMON/RAD/NF,NC,ROF,RIF,GT,CT,DELTAF,DELTAC
        ROC=ROF+GT+CT
        RIC=ROF+GT
        IF(DELTAF.NE.1.)AF=(ROF-RIF)*(1.-DELTAF)/(1-DELTAF**NF)
        IF(DELTAF.EQ.1.)AF=(ROF-RIF)/NF
        R(1)=RIF
        DO 10 I=2,NF+1
10      R(I)=R(I-1)+AF*DELTAF**FLOAT(I-2)
        R(NF+3)=ROF+GT
        R(NF+NC+3)=ROC
        IF(DELTAC.NE.1.)AC=(ROC-RIC)*(1.-DELTAC)/(1-DELTAC**NC)
        IF(DELTAC.EQ.1.)AC=(ROC-RIC)/dfloat(NC)
        DO 20 I=NF+4,NF+NC+3
20      R(I)=R(I-1)+AC*DELTAC**FLOAT((I-NF-2)-2)
        WRITE(*,30)(R(I),I=1,NF+1),(R(I),I=NF+3,NF+NC+3)
30      FORMAT('RADII OF NODES',/,5(1X,E15.8,1X))
        RETURN
        END

      function cpf(t)
      implicit double precision(a-h,o-z)
      data c1,c2,c3,th /19.145,7.8473d-4,5.6437d6,535.285/
      data ed,R /37694.6,1.987/
      a1=dexp(th/T)
      a2=dexp(-ed/(R*T))
      term1=c1*th*th/T/T*a1/(a1-1.)/(a1-1.)
      term2=2.*c2*T
      term3=c3*ed/R/T/T*a2
      cpf=15.496*(term1+term2+term3)
      return
      end

      function ekf(t)
      implicit double precision(a-h,o-z)
      data c1,c2,c3,c4,c5 /40.4,464.,1.216d-4,1.867d-3,0.0191/
      Temp=t-273.15
      bet=2.58-0.58d-3*temp
      frac=0.97
      If (temp.lt.0.) then
      write(*,*) 'temperature less than 273 K'
      stop
      endif
      c4t=dexp(c4*Temp)
      term=(1.-bet*(1.-frac))/(1-bet*(1-0.95))
      if (temp.lt.1650.) then
      ekf=term*(c1/(c2+temp)+c3*c4t)*100.
      elseif (temp.lt.2840.) then
      ekf=term*(c5+c3*c4t)*100.
      else
      write(*,*)'temperature out of range'
      stop
      endif
      return
      end
      
      function cpc(t)
      implicit double precision(a-h,o-z)
      if(t.gt.1090) then
      write(*,*)'temperature greater than 1090'
      stop
      else
      cpc=226.72+0.206617*t-6.49249d-5*t*t
      endif
      return
      end

      function ekc(t)
      implicit double precision(a-h,o-z)
      ekc=7.51+2.09d-2*T-1.45d-5*t*t+7.67d-9*t**3.
      return
      end

        FUNCTION DENF(T)
        implicit double precision(a-h,o-z)
        DENF=10960.
        RETURN
        END
C **
        FUNCTION DENC(T)
        implicit double precision(a-h,o-z)
        DENC=7000.
        RETURN
        END
C  ****

C*****TRIDIAGONAL SOLVER*****
        SUBROUTINE THOMAS(N,AA,RHS,SOL)
        implicit double precision(a-h,o-z)
        DIMENSION AA(25,3),RHS(25),SOL(25)
C***** SOLUTION BY THOMAS *****
        AA(1,3)=AA(1,3)/AA(1,2)
        RHS(1)=RHS(1)/AA(1,2)
        DO 100 I=2,N
        DEL=AA(I,2)-AA(I,1)*AA(I-1,3)
        IF(I.EQ.N)GOTO 130
        AA(I,3)=AA(I,3)/DEL
130     RHS(I)=(RHS(I)-AA(I,1)*RHS(I-1))/DEL
100     CONTINUE
        SOL(N)=RHS(N)
        DO 150 I=N-1,1,-1
150     SOL(I)=RHS(I)-AA(I,3)*SOL(I+1)
        RETURN
        END
C
C

