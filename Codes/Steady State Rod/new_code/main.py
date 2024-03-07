from functions import FUNCTIONS
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
# calculations are being carried out from the Clad Surface to the Centreline of the Fuel Rod
def main():
    solver = FUNCTIONS()

    # grid solver
    solver.grid()
    col_names=["r","rw","re","drw","dre"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.r[i],solver.rw[i],solver.re[i],solver.drw[i],solver.dre[i]])

    print(tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex="always"))

    # coefficient maker
    solver.coefficient()
    col_names=["CAW","CAE","CAP","S","AQ"]
    data=[]
    for i in range(solver.NF+solver.NC):
        data.append([solver.CAW[i],solver.CAE[i],solver.CAP[i],solver.S[i],solver.AQ[i]])
        
    print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    # boundary conditions
    solver.conditioniser()
    col_names=["CAW","CAE","CAP","S","AQ"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.CAW[i],solver.CAE[i],solver.CAP[i],solver.S[i],solver.AQ[i]])
        
    print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    # TDMA solver
    solver.TDMA_ST()
    solver.T[solver.NT-1]=solver.Bi[solver.NT-1]
    for i in range(solver.NT-2,0,-1):
        T_exp=(solver.Ai[i]*solver.T[i+1])+(solver.Bi[i])
        solver.T[i]=T_exp  
        
    solver.T[0]=solver.T[1]       

    col_names=["T","r"]
    data=[]
    for i in range(0,solver.NF+solver.NC):
        data.append([solver.T[i],solver.r[i]])

    print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    #saving data
    df = pd.DataFrame(data, columns=col_names)
    df.to_excel(f'/Users/hiteshchoudhary2109/Desktop/mini-project/Subchannel-Analysis/Codes/Steady State Rod/results/Fig.xlsx', index=False)
    # plotting of data
    plt.plot(solver.r, solver.T, label='Temperature vs. Radius')
    plt.xlabel('Radius')
    plt.ylabel('Temperature')
    plt.title('Temperature Profile')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()