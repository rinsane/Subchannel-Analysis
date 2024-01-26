import numpy as np
AXLN=5.9436
NNODE=97
NK = 19                         ######### no of connections
NCHANL = 14                             ### no of subchannel
SLP=0.5                                
FACK=0.5
VISC=0.000011
GC=9.81                            ##   accelaeration due to gravity

 
F1 = [0] * 14  
F0 = [.090576301,.090576301,.331301059,.1810780788,.331301059,.331301059,.27866318100,.39238281,.278663181,.331301059,.250849063,.501698126,.501698126,.25084906] 
 
RHO = 817.4  
IC = [1, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 9, 6, 7, 9, 10, 11, 12, 13]                             ## representation of interconnections of different subchannels
JC = [2, 3, 5, 4, 5, 6, 8, 10, 7, 8, 9, 10, 11, 12, 13, 14, 12, 13, 14]

USTAR1 = [0.0] * NK
USTAR0 = [0.0] * NK
XUST0 = [[0.0] * NK for _ in range(NK)]
XUST1 = [[0.0] * NK for _ in range(NK)]
DELX=AXLN/(NNODE-1)



  
HDIA = [.0056277,.0056277,.0084154,.005627,.0084154,.0084154,.0074985,.0094202,.0074485,.0084154,.0070309,.0070309,.0070309,.0070309] 
A = [.000014451,.000014451,.000043225,.000028903,.000043225,.000043225,.000038516000,.000048387,.000038516,.000043225,.000035806,.000071612,.000071612,.000035806]

H0=[1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7]
RE = [0] * 20 
HF=[607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59000,607.59,607.59,607.59]

HPERI=[.010272,.010272,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020371,.040742,.040742,.020371]
GAP=[.0018034,.0009,.0009,.0018034,.0018034,.0009,.0018034,.0009,.0018034,.004140000,.00414,.0018034,.000991,.0019558,.0019558,.000991,.00194,.00194,.00194]  
ALPHA = 90 #######################################(ANGLE )
RDIA = 0.01308  
THETA = 0.5                          ### IMPLICIT FAV
GAMA=0.1
ST = [[0.0] * 20 for _ in range(20)]  

XY = [0.0] * NCHANL                                                         ### matrix calculation for ft*stranspose*delu*wpr/area
XZ = [0.0] * NK


WIJ0=[0]*NK
CIJ0=[0]*NK
WIJ1=[0]*NK
CIJ1=[0]*NK

D=np.zeros(NK)
USTD1=[0]*NK
XUSTD1 = np.zeros((NK, NK), dtype=np.float64)

XMLT = np.zeros((NK, NK))
XM = np.zeros((NK, NK))
XMI = np.zeros((NK, NK))
XM0 = np.zeros((NK, NK))
P0 = np.zeros(NK)
P1 = np.zeros(NK)
PB = np.zeros(NK)
PM0 = np.zeros(NK)
P11 = np.zeros(NK)
ERR = np.zeros(NK)
ERROR = np.zeros(NK)
B = np.zeros(NCHANL)
B1 = np.zeros(NCHANL)
B2 = np.zeros(NCHANL)
SS = np.zeros(NCHANL)
SAVE = np.zeros(NK)

XA = np.zeros(NCHANL)

XDELH = np.zeros((NK, NK))
XHS = np.zeros((NK, NK))
XH = np.zeros((NCHANL, NCHANL))

H1 = np.zeros(NK)
HSTAR = np.zeros(NK)
DELH = np.zeros(NK)
Q = np.zeros(NCHANL)
C1 = np.zeros(NCHANL)
C2 = np.zeros(NCHANL)
C3 = np.zeros(NCHANL)
XHST = np.zeros((NK, NK))
S5 = np.zeros((NK, NK))
SD = np.zeros((NK, NK))
W2=np.zeros(NK)

WPR = np.zeros(NK)
F11=np.zeros(NK)
S = np.zeros((NK, NK))
YU1 = np.zeros((NK, NK))
ERROR=np.zeros(NK)
ERR=np.zeros(NK)
DELTA=0.5
FT=0.1                                                              ###  turbulent factor used to compensate imperfect analogy bw turbulent transport of enthalpy and momentum
X=0
NODE=1

WIJIN=0.0
PIN=12262500
print(PIN)
if X==0:
    for I in range(NCHANL):
       F1[I]=F0[I]                                # type: ignore ##############   WHY THIS BC IS NOT UPDATING
       P0[I]=PIN
    
    for K in range(NK):
       WIJ0[K]=WIJIN # type: ignore
       WIJ1[K]=WIJIN # type: ignore


DELX=AXLN/(NNODE-1)
print(DELX)
print(SLP)
