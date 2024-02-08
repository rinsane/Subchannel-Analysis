from star import *
from inputs import *
from SKI import*
def XD():
    
    print(DELX)
    print("subroutine XD")
    star()
    

    for K in range(0, NK):
        if K < len(IC) and K < len(JC):
            I = IC[K] - 1
            J = JC[K] - 1
            CIJ0[K] = 0.5 * FACK * abs(WIJ0[K]) / (RHO * GAP[K] ** 2)
            CIJ1[K] = 0.5 * FACK * abs(WIJ1[K]) / (RHO * GAP[K] ** 2)
            D[K] = (USTAR1[K] / DELX) + (SLP * THETA * CIJ1[K])
            USTD1[K] = USTAR1[K] / D[K]                                                        ### OTHER MATRIX
        else:
            print(f'Index out of range: K={K}, IC={IC}, JC={JC}')

    for KK in range(NK):
        for II in range(NK):
            if KK == II:
                XUSTD1[KK][II] = USTD1[KK]
            else:
                XUSTD1[KK][II] = 0
    print(XUSTD1[KK][II],"DFDX")
    for K in range(NK):
        print(f'CIJ0[{K}] = {CIJ0[K]}, CIJ1[{K}] = {CIJ1[K]}, D[{K}] = {D[K]}, USTD1[{K}] = {USTD1[K]}')

#XD()