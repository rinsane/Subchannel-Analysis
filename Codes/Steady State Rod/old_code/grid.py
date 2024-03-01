from consta import*
import numpy as np
from tabulate import tabulate

drf=R1/(NF-1)
drc=(R3-R1-GT)/(NC-1)
### if r is fine the grid gen is automatically fine

#r
for i in range(0,NF+NC):
    if(i==0):
        r_n=0
    elif(i<=NF-2):
        r_n=r_o+drf
    elif(i<=NF-1):
        r_n=R1
    elif(i==NF):
        r_n=R1+GT
    elif(i<=NF+NC-2):
        r_n=R1+drc*(i-(NF))+GT
    else:
        r_n=R3
    r.append(r_n)
    r_o=r_n                                                                                   ####SOME PROBLEM LIES WITH NC JUST IDENTIFY NOT GIVING GOOD RESULTS
    #print(r_n)                                                                                  ## some issue with last node
    if round(r_n) == R3:
        break
    
#rw 
for i in range(0,NF+NC):
    if(i==0):
        rw_n=0
    else:
        rw_n=0.5*(r[i]+r[i-1])
    rw.append(rw_n)
    #print(rw_n)
    
#re
for i in range(0,NF+NC):
    if(i<=NF-2):
        re_n=0.5*(r[i]+r[i+1])
    elif(i<=NF-1):
        re_n=R1
    elif(i<=NF+NC-2):
        re_n=0.5*(r[i]+r[i+1])
    else:
        re_n=R3
    re.append(re_n)
    #print(re_n)
    
#drw
for i in range(0,NF+NC):
    if(i==0):
        drw_n=0
    else:
        drw_n=r[i]-r[i-1]
    drw.append(drw_n)
    #print(drw)
    
#dre
for i in range(0,NF+NC):
    if(i<=NF+NC-2):
        dre_n=r[i+1]-r[i]
    else:
        dre_n=0                                                                         ###  can be 
    dre.append(dre_n)
    #print(dre)
    
col_names=["r","rw","re","drw","dre"]
data=[]
for i in range(0,NF+NC):
    data.append([r[i],rw[i],re[i],drw[i],dre[i]])
    
print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))