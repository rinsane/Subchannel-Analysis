import math
from SKI import*
from wprim import*
from inputs import*
def xxa():
    # COMMON block variables
   
    
    # Variables from COMMON/A2/
    FACF=np.zeros(NCHANL)

    # Variables from COMMON/A5/
    #S = [[0.0] * NK for _ in range(NCHANL)]
    #ST = [[0.0] * NCHANL for _ in range(NK)]

  

    print('SUBROUTINE XXA')
    
    # Call to WPRIM (assuming it's another subroutine)
    wprim()

    for I in range(0, NCHANL):
        RE[I] = F0[I] * HDIA[I] / (A[I] * VISC)                            # type: ignore ## calculation of reynold no
        FACF[I] = 0.05052 * RE[I] ** (-0.05719)                            ## calculation of friction factor
        X4 = XY[I]
        X1 = (F0[I] / A[I]) ** 2                                             ## ratio of mass flow rate to area
        X2 = 0.5 * FACF[I] / (HDIA[I] * RHO)                                ## pressure drop  due to friction
        X3 = GC * RHO * math.cos(ALPHA * math.pi / 180)                      ## role of gravity
        XA[I] = -X1 * X2 - X3 - X4

    # Print statements for debugging (commented out)
    # print('RE FACF XA')
    for I in range(0, NCHANL):
         print(RE[I], FACF[I], XA[I])

    print('END OF SUB-XXA')


