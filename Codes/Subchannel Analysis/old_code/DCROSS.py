from inputs import*
from SKI import*
def DCROSS():
    
    # fpr computation of diversion cross flow raTE AND AXIAL MASS FLOW F1
    print("STARTING OF SUBROUTINE DCROSS")
    for K in range(0, NK):
        SP1 = USTAR0[K] * WIJ0[K] / DELX
        SP2 = SLP * (1 - THETA) * CIJ0[K] * WIJ0[K]
        SUM3 = 0
        SUM4 = 0

        for I in range(0, NCHANL):
            SP3 = S[K][I] * P1[I]
            SP4 = S[K][I] * P0[I]
            SUM3 += SP3
            SUM4 += SP4

        SP3 = SLP * THETA * SUM3
        SP4 = SLP * (1 - THETA) * SUM4

        WIJ1[K] = (SP1 - SP2 + SP3 + SP4) / D[K]

    # Print the results
    print("WIJ1=")
    for K in range(0, NK):
        print(f"{WIJ1[K]:13.6e}", end=" ")
    print("\nEND OF SUB-DCROSS")
    return

