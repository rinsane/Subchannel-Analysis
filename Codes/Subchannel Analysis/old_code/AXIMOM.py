from XMULT import *
from YMULT import *
from star import *
from inputs import *
from SKI import*

def AXIMOM():
    print("STARTING OF SUBROUTINE AXIMOM")
    star()

    U1 = [F1[I] / A[I] / RHO for I in range(NCHANL)]
    XU1 = [[U1[I] if I == J else 0.0 for J in range(NCHANL)] for I in range(NCHANL)]
    
    YU1 = [[0.0] * NK for _ in range(NCHANL)]
    YMULT(XU1, ST, YU1, NCHANL, NCHANL, NK)

    XXU1 = [[0.0] * NK for _ in range(NCHANL)]
    XMULT(ST, XUST1, XXU1, NCHANL, NK, NK)

    Z1 = [0.0] * NCHANL
    Z2 = [0.0] * NCHANL

    for I in range(NCHANL):
        SUM1 = sum(YU1[I][K] * WIJ1[K] for K in range(NK))
        SUM2 = sum(XXU1[I][K] * WIJ1[K] for K in range(NK))
         
        Z1[I] = 2.0 * DELX * SUM1 / A[I]
        Z2[I] = DELX * SUM2 / A[I]

    P1 = [P0[I] + DELX * XA[I] + Z1[I] - Z2[I] for I in range(NCHANL)]
    P1 = [DELTA * P + (1 - DELTA) * P for P in P1]

    for I, p in enumerate(P1):
        print(f'P1[{I}] = {p}')

    print("END OF SUB-AXIMOM")
    return (P1)
