from inputs import*
from SKI import*
def star():
    

    print('STARTING OF SUB-STAR')

    for K in range(NK):
        I = IC[K] - 1
        J = JC[K] - 1
        if F1[J]:
            USTAR1[K] = F1[J] / (A[J] * RHO)
        elif F1[I] and F1[J]:
            USTAR1[K] = 0.5 * ((F1[I] / (A[I] * RHO)) + (F1[J] / (A[J] * RHO)))
        elif F1[I]:
            USTAR1[K] = F1[I] / (A[I] * RHO)
    
    for K in range(NK):
        I = IC[K] - 1
        J = JC[K] - 1
        if F0[J]:
            USTAR0[K] = F0[J] / (A[J] * RHO)
        elif F0[I] and F0[J]:
            USTAR0[K] = 0.5 * ((F0[I] / (A[I] * RHO)) + (F0[J] / (A[J] * RHO)))
        elif F0[I]:
            USTAR0[K] = F0[I] / (A[I] * RHO)

    for KK in range(NK):
        for II in range(NK):
            if KK == II:
                XUST0[KK][II] = USTAR0[KK]
                XUST1[KK][II] = USTAR1[KK]
            else:
                XUST0[KK][II] = 0.0
                XUST1[KK][II] = 0.0

    # Print USTAR0 and USTAR1
    for K in range(NK):
        print(f'USTAR0[{K}] = {USTAR0[K]}, USTAR1[{K}] = {USTAR1[K]}')

# Call the subroutine
