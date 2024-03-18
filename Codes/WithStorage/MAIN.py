from FUNCTIONS import sub_routines
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import copy
import pandas as pd

'''#Temporary matrix multiplication function for use
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

    return all(row_sum == 0 for row_sum in row_sums) and all(col_sum == 0 for col_sum in col_sums)'''
def main():

    NODE = [sub_routines() for _ in range(2)]
    NODE_initial = NODE[0]

    Axial_length = [NODE[0].DELX*i for i in range(NODE[0].NNODE)]
    Enthalpy = [[] for _ in range(NODE[0].NCHANL)]      # H1
    MassFlowRate = [[] for _ in range(NODE[0].NCHANL)]  # F1
    Pressure = [[] for _ in range(NODE[0].NCHANL)]      # P1
    Crossflow = [[] for _ in range(NODE[0].NK)]

    for i in range(NODE[0].NNODE):                                       ### CERTAIN CLARFICATION

        #For setting the boundary condition -- no error
        if i == 0:
            for I in range(NODE[1].NCHANL):
                NODE[1].F1[I] = NODE[1].F0[I]
                NODE[1].P0[I] = NODE[1].PIN
            #print("FOR NODE ZERO (init)\n")

            for K in range(NODE[1].NK):
                NODE[1].WIJ0[K] = NODE[1].WIJIN
                NODE[1].WIJ1[K] = NODE[1].WIJIN
        else:
            #print(f"FOR NODE {i}\n")
            NODE[1].P0 = NODE[0].P1.copy()

            NODE[1].F0 = NODE[0].F1.copy()
            NODE[1].F1 = NODE[1].F0.copy()

            NODE[1].WIJ0 = NODE[0].WIJ1.copy()
            NODE[1].WIJ1 = NODE[1].WIJ0.copy()

            NODE[1].H0 = NODE[0].H1.copy()

        '''/////////////////////////////////////////////////'''
        #CALLING THE SKI    
        NODE[1].SKI()
        '''print("Connecting matrix")
        print(tabulate(NODE[1].S, tablefmt="fancy_grid"))
        check = True
        for a in range(NODE[1].NK):
            count  =0
            for b in range(NODE[1].NCHANL):
                if NODE[1].S[a][b] != 0:
                    count+=1
            if count != 2:
                check = False
        for a in range(NODE[1].NCHANL):
            count  =0
            for b in range(NODE[1].NK):
                if NODE[1].S[a][b] != 0:
                    count+=1
            if count != 2:
                check = False
        print("Test currently not working correctly please ignore below 2 messages")
        print("Check for connecting matrix: To see if each and and each column has exactly 2 non-zero values")
        if check == True:
            print("YES")
        else:
            print("NO")
        
        Product = matrix_multiply(NODE[1].ST,NODE[1].S)
        print(tabulate(Product, tablefmt="fancy_grid"))
        if check_zero_sums(Product):
            print("YES")
        else:
            print("NO")'''

        NODE[1].XD()
        NODE[1].XB()
        NODE[1].gauss()
        NODE[1].DCROSS()

        #Reversing the flow
        for K in range(NODE[1].NK):
            NODE[1].WIJ1[K] = - NODE[1].WIJ1[K]
        
        NODE[1].MASFLO()
        #copying the F1 in F11
        for I in range(NODE[1].NCHANL):
            NODE[1].F11[I] = NODE[1].F1[I]
        
        '''
        P1, WIJ1, F1, -- calculated from above functions respectively
        now introducing checks if P1, F1, is positive or not
        '''
        #Check for P1
        for I in range(NODE[1].NCHANL):
            if(NODE[1].P1[I] < 0 ):
                print(f"Negative pressure in P1 at node {i}")
                print(tabulate([[NODE[1].P1[I], NODE[1].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[1].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        #Check for F1
        for I in range(NODE[1].NCHANL):
            if(NODE[1].F1[I] < 0 ):
                print(f"Negative massflow rate in F1 at node {i}")
                print(tabulate([[NODE[1].P1[I], NODE[1].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                print(tabulate([[NODE[1].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                sys.exit()
        #print("All checks passes for P1 and F1 and WIj1, values are listed below")
        
        for I in range(NODE[1].NCHANL):
            NODE[1].ERROR[I] = abs((NODE[1].F11[I] - NODE[1].F1[I]) / NODE[1].F1[I])
        
        EMAX = max(NODE[1].ERROR)

        while EMAX > 10E-8:
            NODE[1].AXIMOM()
            for I in range(NODE[1].NCHANL):
                NODE.P1[I] = (NODE[1].DELTA *NODE[1].P1[I]) + ((1 - NODE[1].DELTA) * NODE[1].P0[I])
            NODE[1].DCROSS()
            for I in range(NODE[1].NCHANL):
                NODE.WIJ1[I] = (NODE[1].GAMA *NODE[1].WIJ1[I]) + ((1 - NODE[1].GAMA) * NODE[1].WIJ0[I])
            for I in range(NODE[1].NCHANL):
                NODE[1].F11[I] = NODE[1].F1[I]
            
            NODE[1].MASFLO()

            for I in range(NODE[1].NCHANL):
                NODE[1].ERROR[I] = abs((NODE[1].F11[I] - NODE[1].F1[I]) / NODE[1].F1[I])
            
            EMAX = max(NODE[1].ERROR)

        NODE[1].HM()

        if i%10 == 0:
            print(f"FOR NODE {i}:\n")
            print(f"Pressure {i}: {NODE[1].P1}\n")
            print(f"Enthalpy {i}: {NODE[1].H1}\n")
            print(f"WIJ{i}      : {NODE[1].WIJ1}\n")
            print(f"MassFlow {i}: {NODE[1].F1}")

        for chan in range(NODE[0].NCHANL):
            Enthalpy[chan].append(NODE[1].H1[chan])
            MassFlowRate[chan].append(NODE[1].F1[chan])
            Pressure[chan].append(NODE[1].P1[chan])

        for chan in range(NODE[0].NK):
            Crossflow[chan].append(NODE[1].WIJ1[chan])

        #DATA STORING
        direc2 = os.path.dirname(os.path.abspath(__file__)) + "\Subchannels"
        if i == 0:
            for channel in range(NODE[1].NCHANL):
                with open(direc2+f"\Channel {channel + 1}.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Node Number", "Pressure", "Enthalpy", "CrossFlow", "MassFlow"])
                    writer.writerow([0, NODE[1].P1[channel], NODE[1].H1[channel], NODE[1].WIJ1[channel], NODE[1].F1[channel]])

        else:
            for channel in range(NODE[1].NCHANL):
                with open(direc2+f"\Channel {channel + 1}.csv", 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([i, NODE[1].P1[channel], NODE[1].H1[channel], NODE[1].WIJ1[channel], NODE[1].F1[channel]])


        
        NODE[0] = copy.deepcopy(NODE[1])

    # DATA TABULATION
    Headings = ["Sub-Channel", "Inlet Mass Flow Rate [F0]", "Inlet Enthalpy [H0]",
          "Outlet Mass Flow Rate [F1 at last Node]",
          "Outlet Enthalpy [H1 at last Node]",
          "Heat Generated [C1 at last Node]", "H0 + C1"]
    SCs = [i + 1 for i in range(NODE_initial.NCHANL)]
    F0 = NODE_initial.F0
    H0 = NODE_initial.H0
    F1 = NODE[1].F1
    H1 = NODE[1].H1
    C1 = NODE[1].C1
    H0_C1 = [H0[i] + C1[i] for i in range(NODE_initial.NCHANL)]
    LAST_ROW = ["", sum(F0), "", sum(F1), sum(H1), sum(C1), sum(H0_C1)]

    datas = zip(SCs, F0, H0, F1, H1, C1, H0_C1)
    direc = os.path.dirname(os.path.abspath(__file__))
    
    with open(direc+r"\results.csv", "w", newline='') as datasheet:
        writer = csv.writer(datasheet)
        writer.writerow(Headings)
        writer.writerows(datas)

        writer.writerow(LAST_ROW)
        
    data_dict = {
        "Node": list(range(NODE[0].NNODE)),
        "Pressure (P1)": [NODE[1].P1 for i in range(NODE[0].NNODE)],
        "Enthalpy (H1)": [NODE[1].H1 for i in range(NODE[0].NNODE)],
        "Mass Flow Rate (F1)": [NODE[1].F1 for i in range(NODE[0].NNODE)],
        "Crossflow Rate (WIJ1)": [NODE[1].WIJ1 for i in range(NODE[0].NNODE)]
    }

    df = pd.DataFrame(data_dict)

    # Directory where you want to save the Excel file
    direc = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(direc, "results.xlsx")

    df.to_excel(excel_path, index=False)
    # PLOT CREATION
    for i in range(NODE[0].NCHANL):
        # Create a new figure for each subplot
        plt.figure()
        
        # Plot Pressure
        plt.subplot(1, 3, 1)
        plt.plot(Axial_length, Pressure[i], label="Pressure")
        plt.title(f"SUB-CHANNEL {i}")
        plt.xlabel("Axial Length")
        plt.ylabel("Pressure")
        plt.legend()

        # Plot Enthalpy
        plt.subplot(1, 3, 2)
        plt.plot(Axial_length, Enthalpy[i], label="Enthalpy")
        plt.title(f"SUB-CHANNEL {i}")
        plt.xlabel("Axial Length")
        plt.ylabel("Enthalpy")
        plt.legend()

        # Plot MassFlowRate
        plt.subplot(1, 3, 3)
        plt.plot(Axial_length, MassFlowRate[i], label="Mass Flow Rate")
        plt.title(f"SUB-CHANNEL {i}")
        plt.xlabel("Axial Length")
        plt.ylabel("Mass Flow Rate")
        plt.legend()

        plt.tight_layout()

    plt.figure()
    for i in range(NODE[0].NK):
        plt.plot(Axial_length, Crossflow[i], label=f"{i}")
        plt.title(f"Crossflow")
        plt.xlabel("Axial Length")
        plt.ylabel("Crossflow Rate")
        plt.legend()
        plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()