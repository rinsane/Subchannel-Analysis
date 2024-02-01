from FUNCTIONS import sub_routines
import sys
from tabulate import tabulate

def main():

    NODE = [sub_routines() for _ in range(sub_routines().NNODE)]

    for i in range(NODE[0].NNODE):                                       ### CERTAIN CLARFICATION

        #For setting the boundary condition -- no error
        if i == 0:
            for I in range(NODE[i].NCHANL):
                NODE[i].F1[I] = NODE[i].F0[I]
                NODE[i].P0[I] = NODE[i].PIN
            print("FOR NODE ZERO (init)\n")

            for K in range(NODE[i].NK):
                NODE[i].WIJ0[K] = NODE[i].WIJIN
                NODE[i].WIJ1[K] = NODE[i].WIJIN
        
        else:
            
            NODE[i].P0 = NODE[i-1].P1.copy()

            NODE[i].F0 = NODE[i-1].F1.copy()
            NODE[i].F1 = NODE[i].F0.copy()

            NODE[i].WIJ0 = NODE[i-1].WIJ1.copy()
            NODE[i].WIJ1 = NODE[i].WIJ0.copy()

            NODE[i].H0 = NODE[i-1].H1.copy()
        '''/////////////////////////////////////////////////'''
        #CALLING THE SKI    
        NODE[i].SKI()
        NODE[i].XD()
        NODE[i].XB()
        NODE[i].gauss()
        NODE[i].DCROSS()

        #Reversing the flow
        for K in range(NODE[i].NK):
            NODE[i].WIJ1[K] = - NODE[i].WIJ1[K]
        
        NODE[i].MASFLO()
        #copying the F1 in F11
        for I in range(NODE[i].NCHANL):
            NODE[i].F11[I] = NODE[i].F1[I]
        
        '''
        P1, WIJ1, F1, -- calculated from above functions respectively
        now introducing checks if P1, F1, is positive or not
        '''
        #Check for P1
        for I in range(NODE[i].NCHANL):
            if(NODE[i].P1[I] < 0 ):
                print(f"Negative pressure in P1 at node {i}")
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        #Check for F1
        for I in range(NODE[i].NCHANL):
            if(NODE[i].F1[I] < 0 ):
                print(f"Negative massflow rate in F1 at node {i}")
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        #print("All checks passes for P1 and F1 and WIj1, values are listed below")
        '''print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
        print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))'''
        for I in range(NODE[i].NCHANL):
            NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])
        
        EMAX = max(NODE[i].ERROR)

        while EMAX > 10E-8:
            NODE[i].AXIMOM()
            for I in range(NODE[i].NCHANL):
                NODE.P1[I] = (NODE[i].DELTA *NODE[i].P1[I]) + ((1 - NODE[i].DELTA) * NODE[i].P0[I])
            NODE[i].DCROSS()
            for I in range(NODE[i].NCHANL):
                NODE.WIJ1[I] = (NODE[i].GAMA *NODE[i].WIJ1[I]) + ((1 - NODE[i].GAMA) * NODE[i].WIJ0[I])
            for I in range(NODE[i].NCHANL):
                NODE[i].F11[I] = NODE[i].F1[I]
            
            NODE[i].MASFLO()

            for I in range(NODE[i].NCHANL):
                NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])
            
            EMAX = max(NODE[i].ERROR)

        NODE[i].HM()

        if i%1000 == 0 or i in [NODE[0].NNODE - 1, NODE[0].NNODE - 2]:
            print(f"FOR NODE {i}:\n")
            print(f"Pressure {i}: {NODE[i].P1}\n")
            print(f"Enthalpy {i}: {NODE[i].H1}\n")
            print(f"WIJ{i}      : {NODE[i].WIJ1}\n")
            print(f"MassFlow {i}: {NODE[i].F1}")

if __name__ == '__main__':
    main()