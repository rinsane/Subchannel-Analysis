from consta import *
from grid import *
from coefff import *
from bc import*
from TDMA_ST import*
import matplotlib.pyplot as plt

TDMA_ST()

plt.plot(r, T, label='Temperature vs. Radius')
plt.xlabel('Radius')
plt.ylabel('Temperature')
plt.title('Temperature Profile')
plt.legend()
plt.show()

col_names=["T","r"]
data=[]
for i in range(0,NF+NC):
    data.append([T[i],r[i]])
    
print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))