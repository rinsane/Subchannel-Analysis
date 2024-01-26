import numpy as np
from consta import*
from grid import*
from coefff import*


####Nuemann Left Boundary    at centerline
CAW[0] = 0
S[0] = S[0] + (shi*r[0]*qflux)


#########%Robin's Right Boundary            at fuel and gap surface
CAE[NF]=CAE[NF]+shi*r[NF]*HTC
CAP[NF] = CAP[NF] + shi*r[NF]*HTC
S[NF] = S[NF] + (shi*r[NF]*HTC*((T[NF]+T[NF+1])/2))

##Robin's Left Boundary                    AT GAP AND CLAD SURFACE
CAW[NF+1] = CAW[NF+1]+shi*r[NF+1]*HTC
CAP[NF+1] = CAP[NF+1] + shi*r[NF+1]*HTC
S[NF+1] = S[NF+1] + (shi*r[NF+1]*HTC*((T[NF]+T[NF+1])/2)) 



#########%Robin's Right Boundary            at CLAD and COOLANT surface
CAE[NF+NC-1] = 0
CAP[NF+NC-1] = CAP[NF+NC-1] + shi*r[NF+NC-1]*HTCC
S[NF+NC-1] = S[NF+NC-1] + (shi*r[NF+NC-1]*HTCC*Tinf)

col_names=["CAW","CAE","CAP","S","AQ"]
data=[]
for i in range(0,NF+NC):
    data.append([CAW[i],CAE[i],CAP[i],S[i],AQ[i]])
    
print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))