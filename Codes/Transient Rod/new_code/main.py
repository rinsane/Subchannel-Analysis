from functions import FUNCTIONS
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
import os

def main(solver, curr):

    # grid solver
    solver.grid()
    col_names=["r","rw","re","drw","dre"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.r[i],solver.rw[i],solver.re[i],solver.drw[i],solver.dre[i]])

    #print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    # coefficient maker
    solver.coefficient()
    col_names=["CAW","CAE","CAP","S","AQ","AT","ATO"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.CAW[i],solver.CAE[i],solver.CAP[i],solver.S[i],solver.AQ[i],solver.AT[i],solver.ATO[i]])
    
    #print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    # boundary conditions
    solver.conditioniser()
    col_names=["CAW","CAE","CAP","S","AQ","AT","ATO"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.CAW[i],solver.CAE[i],solver.CAP[i],solver.S[i],solver.AQ[i],solver.AT[i],solver.ATO[i]])

    #print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    # TDMA solver
    solver.TDMA()
    col_names=["T","r"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.T_OLD[i],solver.r[i]])
    
    #print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    
    '''
    # Write T and r data to Excel
    dirr = os.getcwd()
    df = pd.DataFrame(data, columns=col_names)
    df.to_excel(dirr+r'/Fig4.xlsx', index=False)
    '''

    # plotting of data
    plt.plot(solver.r, solver.T_OLD, label=f'T vs. R at t = {round(curr, 2)} sec')
    plt.xlabel('Radius')
    plt.ylabel('Temperature')
    plt.title('Temperature Profile')
    plt.legend()

    return solver.T_OLD


if __name__ == "__main__":
    curr = 0

    while curr <= 1:
        solver = FUNCTIONS()
        if curr == 0:
            solver.T = [curr for _ in range(solver.NF + solver.NC)]
        else:
            solver.T = OLD_T.copy()
        solver.T_OLD = solver.T.copy()
        OLD_T = main(solver, curr)
        print(f"curr:{curr}")
        curr += 0.1
    
    plt.show()