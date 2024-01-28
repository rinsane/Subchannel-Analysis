import numpy as np
from XMULT import* 
from YMULT import*
from inputs import*
from SKI import* 


def HM():
    print("STARTING OF SUBROUTINE HMW")
    for K in range(0, NK):
        I = IC[K]-1
        J = JC[K]-1
        HSTAR[K] = 0.5 * (H0[I] + H0[J])
        DELH[K] = H0[I] - H0[J]

    
    for II in range(0, NK):
        for JJ in range(0, NK):
            if II == JJ:
                XDELH[II, JJ] = DELH[II]
                XHS[II, JJ] = HSTAR[II]
            else:
                XDELH[II, JJ] = 0
                XHS[II, JJ] = 0

    

    for II in range(0, NCHANL):
        for JJ in range(0, NCHANL):
            if II == JJ:
                XH[II, JJ] = H0[I]
            else:
                XH[II, JJ] = 0

    XMULT(ST, XHS,S5, NCHANL, NK, NK)
    XMULT(ST, XDELH,SD, NCHANL, NK, NK)
    YMULT(XH, ST,XHST, NCHANL, NCHANL, NK)

    

    for I in range(0, NCHANL):
        Q[I] = HF[I] * HPERI[I]
        #print(Q[I])
    for I in range(0, NCHANL):
        C1[I] = Q[I] * DELX / F1[I]

    for II in range(0, NCHANL):
        SUM3 = 0
        SUM4 = 0
        for KK in range(0, NK):
            S3 = XHST[II, KK] * WIJ1[KK]
            SS3 = S5[II, KK] * WIJ1[KK]
            S3 = S3 - SS3
            S4 = SD[II, KK ] * WPR[KK]
            SUM3 += S3
            SUM4 += S4
            C2[II ] = SUM4 * DELX / F1[II]
            C3[II] = SUM3 * DELX / F1[II]

    for I in range(0, NCHANL):
        H1[I] = H0[I] + C1[I] - C2[I] + C3[I]

    # Print the results
    for I in range(0, NCHANL):
        print(f"H1[{I}] = {H1[I]}")

    print("END OF SUB-HMW")
    return (H1)


HM()
