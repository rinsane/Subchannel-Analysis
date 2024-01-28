from FUNCTIONS import sub_routines
import sys

def main():

    NODE = [sub_routines() for _ in range(sub_routines().NNODE)]

    for i in range(NODE[0].NNODE):

        if i == 0:
            for I in range(NODE[i].NCHANL):
                NODE[i].F1[I] = NODE[i].F0[I]
                NODE[i].P0[I] = NODE[i].PIN
            print("FOR NODE ZERO (init) \n\n")

            for K in range(NODE[i].NK):
                NODE[i].WIJ0[K] = NODE[i].WIJIN
                NODE[i].WIJ1[K] = NODE[i].WIJIN
        
        else:
            print(f"\n\nFOR NODE {i}: \n\n")
            NODE[i].P0 = NODE[i-1].P1.copy()

            NODE[i].F0 = NODE[i-1].F1.copy()
            NODE[i].F1 = NODE[i].F0.copy()

            NODE[i].WIJ0 = NODE[i-1].WIJ1.copy()
            NODE[i].WIJ1 = NODE[i].WIJ0.copy()

            NODE[i].H0 = NODE[i-1].H1.copy()
            
        NODE[i].SKI()
        NODE[i].XD()
        NODE[i].XB()
        NODE[i].XM = NODE[i].YMULT(
            NODE[i].XMLT, NODE[i].S, NODE[i].XM, NODE[i].NCHANL, NODE[i].NK, NODE[i].NCHANL
        )

        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
                NODE[i].XM[I][J] = (
                    NODE[i].DELX * NODE[i].SLP * NODE[i].XM[I][J] / NODE[i].A[I]
                )

        for II in range(NODE[i].NCHANL):
            for JJ in range(NODE[i].NCHANL):
                if II == JJ:
                    NODE[i].XMI[II][JJ] = NODE[i].THETA * NODE[i].XM[II][JJ] + 1
                else:
                    NODE[i].XMI[II][JJ] = NODE[i].THETA * NODE[i].XM[II][JJ]

        for I in range(NODE[i].NCHANL):
            for J in range(NODE[i].NCHANL):
                NODE[i].XM0[I][J] = NODE[i].XMI[I][J] - NODE[i].XM[I][J]

        for I in range(NODE[i].NCHANL):
            SUM = 0
            for J in range(NODE[i].NCHANL):
                PM = NODE[i].XM0[I][J] * NODE[i].P0[J]
                SUM += PM
            NODE[i].PM0[I] = SUM
            NODE[i].PB[I] = NODE[i].B[I] + NODE[i].PM0[I]

        NODE[i].gauss()
        NODE[i].DCROSS()

        for K in range(NODE[i].NK):
            NODE[i].WIJ1[K] = - NODE[i].WIJ1[K]

        for I in range(NODE[i].NCHANL):
            NODE[i].F11[I] = NODE[i].F1[I]
        
        NODE[i].MASFLO()

        for I in range(NODE[i].NCHANL):
            NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])

        EMAX = max(NODE[i].ERROR)
        
        '''if EMAX > 0.01:  ## CHECK ALIGNMENT HERE
            while True:
                NODE[i].AXIMOM()
                for K in range(NODE[i].NK):
                    NODE[i].W2[K] = NODE[i].WIJ1[K]
                NODE[i].DCROSS()
                for K in range(NODE[i].NK):
                    NODE[i].WIJ1[K] = (
                        NODE[i].GAMA * NODE[i].WIJ1[K] + (1 - NODE[i].GAMA) * NODE[i].WIJ0[K]
                    )
                for I in range(NODE[i].NCHANL):
                    NODE[i].F11[I] = NODE[i].F1[I]
                NODE[i].MASFLO()
                for I in range(NODE[i].NCHANL):
                    if NODE[i].F1[I] <= 0:
                        sys.exit("MASS was less than 0")
                    NODE[i].ERR[I] = abs((NODE[i].F1[I] - NODE[i].F11[I]) / NODE[i].F1[I])
                ERRMAX = max(NODE[i].ERR)
                if ERRMAX <= 0.01:
                    break
                else:
                    continue'''
        NODE[i].HM()

        print(f"Pressure {i}: {NODE[i].P1}\n")
        print(f"Enthalpy {i}: {NODE[i].H1}\n")
        print(f"WIJ{i}      : {NODE[i].WIJ1}\n")
        print(f"MassFlow {i}: {NODE[i].F1}")

if __name__ == '__main__':
    main()