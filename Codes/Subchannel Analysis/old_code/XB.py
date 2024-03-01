import numpy as np
from XMULT import* 
from XA import*
from inputs import*
from XD import*
from SKI import*
def XB():
    print("subroutine XB")
    XMULT(ST, XUSTD1, XMLT, NCHANL, NK, NK)

    print(XMLT,"GG")

    for K in range(0, NK):
        SAVE1 = USTAR0[K] * WIJ0[K] / DELX
        SAVE2 = SLP * (1 - THETA) * CIJ0[K] * WIJ0[K]
        SAVE[K] = SAVE1 - SAVE2

    for I in range(0, NCHANL):
        SUM = 0.0
        for K in range(0, NK):
            SUM += XMLT[I, K] * SAVE[K]
        SS[I] = SUM

    xxa()

    

    for I in range(0, NCHANL):
        B1[I] = DELX * SS[I] / A[I]
        B2[I] = 2.0 * (F1[I ] - F0[I]) * (F1[I] / A[I] / RHO) / A[I]
        B[I] = DELX * XA[I] - B1[I] - B2[I]

    # Print the results
    for I in range(0, NCHANL):
        print(f"B1[{I}] = {B1[I ]}, B2[{I}] = {B2[I]}, B[{I}] = {B[I]}")
#XB()

