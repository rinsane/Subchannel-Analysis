from inputs import*
from SKI import*
def MASFLO():
    print("STARTING OF SUBROUTINE MASFLO")
    for I in range(0, NCHANL):
        SUM = 0
        for K in range(0, NK):
            SW = ST[I][K] * WIJ1[K]
            SUM += SW
        F1[I] = F0[I] - (DELX * SUM)

    # Print the results
    print("AXIAL MASS FLOW(F1)=")
    for I in range(0, NCHANL):
        print(f"{F1[I]:13.6e}", end=" ")
    print("\n***** TOTAL MASS FLOW= ", sum(F1))
    print("\n***** TOTAL MASS FLOW initial= ", sum(F0))
    print("END OF SUB-MASFLO")
    return (F1)

