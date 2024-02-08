from FUNCTIONS import sub_routines
import sys
from tabulate import tabulate
import numpy as np
#Temporary matrix multiplication function for use
def matrix_multiply(A, B):
    # Check if the number of columns in A is equal to the number of rows in B
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in A must be equal to the number of rows in B")

    # Initialize the result matrix with zeros
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    # Perform matrix multiplication using nested loops
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result
#Temporary function
def check_zero_sums(matrix):
    """
    Check if the sum of elements in every row and every column is zero.

    Parameters:
    - matrix: Input matrix (2D list or NumPy array)

    Returns:
    - True if the sums are zero, False otherwise
    """
    row_sums = np.sum(matrix, axis=1)
    col_sums = np.sum(matrix, axis=0)

    return all(row_sum == 0 for row_sum in row_sums) and all(col_sum == 0 for col_sum in col_sums)
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
        #CALLING THE SKI    
        NODE[i].SKI()
        print("Connecting matrix")
        print(tabulate(NODE[i].S, tablefmt="fancy_grid"))
        check = True
        for a in range(NODE[i].NK):
            count  =0
            for b in range(NODE[i].NCHANL):
                if NODE[i].S[a][b] != 0:
                    count+=1
            if count != 2:
                check = False
        for a in range(NODE[i].NCHANL):
            count  =0
            for b in range(NODE[i].NK):
                if NODE[i].S[a][b] != 0:
                    count+=1
            if count != 2:
                check = False
        print("Test currently not working correctly please ignore below 2 messages")
        print("Check for connecting matrix: To see if each and and each column has exactly 2 non-zero values")
        if check == True:
            print("YES")
        else:
            print("NO")
        
        Product = matrix_multiply(NODE[i].ST,NODE[i].S)
        print(tabulate(Product, tablefmt="fancy_grid"))
        if check_zero_sums(Product):
            print("YES")
        else:
            print("NO")

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
                print("Negative pressure in P1 at node {i}")
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        #Check for F1
        for I in range(NODE[i].NCHANL):
            if(NODE[i].F1[I] < 0 ):
                print("Negative massflow rate in F1 at node {i}")
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        print("All checks passes for P1 and F1 and WIj1, values are listed below")
        print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
        print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
        for I in range(NODE[i].NCHANL):
            NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])
        
        EMAX = max(NODE[i].ERROR)
        
        if EMAX > 0.01:  ## CHECK ALIGNMENT HERE
            while True:
                NODE[i].AXIMOM()
                print(NODE[i].F1)
                for K in range(NODE[i].NK):
                    NODE[i].W2[K] = NODE[i].WIJ1[K]
                print(NODE[i].F1)
                NODE[i].DCROSS()
                print(NODE[i].F1)
                for K in range(NODE[i].NK):
                    NODE[i].WIJ1[K] = (
                        NODE[i].GAMA * NODE[i].WIJ1[K] + (1 - NODE[i].GAMA) * NODE[i].WIJ0[K]
                    )
                print(NODE[i].F1)
                for I in range(NODE[i].NCHANL):
                    NODE[i].F11[I] = NODE[i].F1[I]
                print(NODE[i].F1)
                NODE[i].MASFLO()
                print(NODE[i].F1)
                for I in range(NODE[i].NCHANL):
                    if NODE[i].F1[I] <= 0:
                        sys.exit("MASS was less than 0")
                    NODE[i].ERR[I] = abs((NODE[i].F1[I] - NODE[i].F11[I]) / NODE[i].F1[I])
                print(NODE[i].F1)
                ERRMAX = max(NODE[i].ERR)
                print(NODE[i].F1)
                if ERRMAX <= 0.01:
                    break
                else:
                    continue
                print(NODE[i].F1)
        NODE[i].HM()

        print(f"Pressure {i}: {NODE[i].P1}\n")
        print(f"Enthalpy {i}: {NODE[i].H1}\n")
        print(f"WIJ{i}      : {NODE[i].WIJ1}\n")
        print(f"MassFlow {i}: {NODE[i].F1}")

if __name__ == '__main__':
    main()