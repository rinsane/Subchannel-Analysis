from FUNCTIONS import sub_routines
import sys

def main():

    NODE = [sub_routines() for _ in range(sub_routines().NNODE)]

    for i in range(NODE[0].NNODE):

        #For setting the boundary condition -- no error
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
        '''/////////////////////////////////////////////////'''
        #CALLING THE SKI -- For finding the connecting matrix S and its transpose ST   
        NODE[i].SKI()

