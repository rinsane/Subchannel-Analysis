from inputs import*
from SKI import*
def wprim():
   
     ######         computation of turbulent cross flow W ij'
    #F1 = [0] * 20 ### check it
    
    
   
    #### wpr= beta*gap*avg mass flux

  

    print('SUBROUTINE WPRIM')

    for K in range(NK):
        I = IC[K] - 1
        J = JC[K] - 1

        if 0 <= I < len(IC) and 0 <= J < len(JC):
            
            AHDIA = 0.5 * (HDIA[I] + HDIA[J])                                                             ### avg hdia of adjacent subchannel
            AVRE = 0.5 * ((F1[I] / A[I]) + (F1[J] / A[J])) * AHDIA / VISC                                 ## avg re of adjacent subchannel
            #print(AVRE)
            BETA = 0.0018 * (AVRE ** (-0.1)) * (AHDIA / GAP[K]) * ((GAP[K] / RDIA) ** (1 - 0.4))          ### correlation for beta taken from finding
            
            print("AVRE:", AVRE, "AHDIA:", AHDIA, "GAP[K]:", GAP[K], "RDIA:", RDIA)

            WPR = BETA * GAP[K] * AVRE * VISC / AHDIA                                                       ## wpr is turbulent cross flow
            #print(WPR)
        else:
            print(f"Invalid indices for AHDIA: K={K}, I={I}, J={J}")

    #for K in range(NK):
     #   I = IC[K] - 1
      #  J = JC[K] - 1
       # if 0 <= I < len(IC) and 0 <= J < len(JC):
        #    print(f'K={K}, IC={IC[K]}, JC={JC[K]}, I={I}, J={J}, A[I]={A[I]}, A[J]={A[J]}, F1[I]={F1[I]}, F1[J]={F1[J]}')
        #else:
         #   print(f"Invalid indices for printing: K={K}, I={I}, J={J}")

    for K in range(NK):
        I = IC[K] - 1
        J = JC[K] - 1
        if 0 <= I < len(IC) and 0 <= J < len(JC) and 0 <= K < len(XZ):
            #print(len(XZ))
            XZ[K] = ((F1[I] / A[I]) - (F1[J] / A[J])) * WPR / RHO
            #print(XZ[K])
        else:
            print(f"Invalid indices for XZ: K={K}, I={I}, J={J}")

    for I in range(NCHANL):
        SUM = 0.0
        for K in range(NK):
            if 0 <= I < len(ST) and 0 <= K < len(ST[I]) and 0 <= K < len(XZ):
                SUM += ST[I][K] * XZ[K]
                #print(ST[I][K])################ PROBLEM IS HERE 
        if 0 <= I < len(XY) and 0 <= I < len(A):
            XY[I] = FT * SUM / A[I]
            print(f'XY[{I}] = {XY[I]}')
        else:
            print(f"Invalid index for XY: I={I}")

    print('END OF SUB-WPRIM')

wprim()
# Call the subroutine


