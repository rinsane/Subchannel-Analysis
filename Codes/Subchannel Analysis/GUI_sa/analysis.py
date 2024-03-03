import sys
from tabulate import tabulate
import numpy as np
import tkinter as tk

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

def calculate(NODE):

    Axial_length = [NODE[0].DELX*i for i in range(NODE[0].NNODE)]
    Enthalpy = [[] for _ in range(NODE[0].NCHANL)]      # H1
    MassFlowRate = [[] for _ in range(NODE[0].NCHANL)]  # F1
    Pressure = [[] for _ in range(NODE[0].NCHANL)]      # P1
    Crossflow = [[] for _ in range(NODE[0].NK)]

    for i in range(NODE[0].NNODE): ### CERTAIN CLARFICATION
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
        #print("Connecting matrix")
        #print(tabulate(NODE[i].S, tablefmt="fancy_grid"))
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
        #print("Test currently not working correctly please ignore below 2 messages")
        #print("Check for connecting matrix: To see if each and and each column has exactly 2 non-zero values")
        
        '''
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
        '''

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
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                return (f"Negative pressure in P1 at node {i}!", 0, 0, 0, 0, 0)
        #Check for F1
        for I in range(NODE[i].NCHANL):
            if(NODE[i].F1[I] < 0 ):
                print(tabulate([[NODE[i].P1[I], NODE[i].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[i].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                return (f"Negative massflow rate in F1 at node {i}!", 0, 0, 0, 0, 0)
        #print("All checks passes for P1 and F1 and WIj1, values are listed below")
        
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

        for chan in range(NODE[0].NCHANL):
            Enthalpy[chan].append(NODE[i].H1[chan])
            MassFlowRate[chan].append(NODE[i].F1[chan])
            Pressure[chan].append(NODE[i].P1[chan])

        for chan in range(NODE[0].NK):
            Crossflow[chan].append(NODE[i].WIJ1[chan])

    return (NODE, Axial_length, Enthalpy, MassFlowRate, Pressure, Crossflow)