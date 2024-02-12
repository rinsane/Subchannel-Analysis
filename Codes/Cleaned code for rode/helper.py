import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
class one_for_all:
    def __init__(self):
        
        self.AE=[]
        self.Ai=[]
        self.AQ=[]
        self.AW=[]
        self.AW_ex=[]
        
        self.Bi=[]
        
        self.CAE=[]
        self.CAP=[]
        self.CAQ=[]
        self.CAW=[]
        
        self.dre=[]
        self.drw=[]
        
        self.R1=0.012
        self.R2=0.015
        self.R3=0.021
        self.r=[]
        self.rw=[]
        self.re=[]
        
        self.GT = self.R2-self.R1
        
        self.HTC=7800
        self.HTCC=3840
        
        self.kf=2.5                                        ### thermal conduvtivity of fuel rod
        
        self.NF=13
        self.NC=8                                        ##### SOME PROBLEM LIES WITH NC
        self.NG=1                                        ### ALWAYS TAKE 1 NODE TO SOLVE FOR GAP THAT IS IT IS AT INTERSECTION BETWEEN FUEL AND CLAD  
        self.NT=self.NF+self.NC
        
        self.Q=10e6
        
        
        
        self.S=[]
        self.shi=1
        
        self.Tinf=400
        self.T=[0 for i in range(0,self.NF+self.NC)]
       
        self.qflux=0 
    
    def grid(self):
        #Code for Grid is running
        drf=self.R1/(self.NF-1)
        drc=(self.R3-self.R1-self.GT)/(self.NC-1)
        ### if r is fine the grid gen is automatically fine
        ##r
        for i in range(0,self.NF+self.NC):
            if(i==0):
                r_n=0
            elif(i<=self.NF-2):
                r_n=r_o+drf
            elif(i<=self.NF-1):
                r_n=self.R1
            elif(i==self.NF):
                r_n=self.R1+self.GT
            elif(i<=self.NF+self.NC-2):
                r_n=self.R1+drc*(i-(self.NF))+self.GT
            else:
                r_n=self.R3
            self.r.append(r_n)
            r_o=r_n                                                             #SOME PROBLEM LIES WITH NC JUST IDENTIFY NOT GIVING GOOD RESULTS
            #print(r_n)
            #some issue with last node
            if round(r_n) == self.R3:
                break
    
        #rw 
        for i in range(0,self.NF+self.NC):
            if(i==0):
                rw_n=0
            else:
                rw_n=0.5*(self.r[i]+self.r[i-1])
            self.rw.append(rw_n)
            #print(rw_n)
    
        #re
        for i in range(0,self.NF+self.NC):
            if(i<=self.NF-2):
                re_n=0.5*(self.r[i]+self.r[i+1])
            elif(i<=self.NF-1):
                re_n=self.R1
            elif(i<=self.NF+self.NC-2):
                re_n=0.5*(self.r[i]+self.r[i+1])
            else:
                re_n=self.R3
            self.re.append(re_n)
        #print(re_n)
    
        #drw
        for i in range(0,self.NF+self.NC):
            if(i==0):
                drw_n=0
            else:
                drw_n=self.r[i]-self.r[i-1]
            self.drw.append(drw_n)
            #print(drw)
    
        #dre
        for i in range(0,self.NF+self.NC):
            if(i<=self.NF+self.NC-2):
                dre_n=self.r[i+1]-self.r[i]
            else:
                dre_n=0                                                    
            #can be 
            self.dre.append(dre_n)
            #print(dre)
        #?print below
        
        col_names=["r","rw","re","drw","dre"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.r[i],self.rw[i],self.re[i],self.drw[i],self.dre[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    
    def coefff(self):
        #AW
        for i in range(0,self.NF+self.NC):
            if(i==0):
                AW_ex=0
            else:
                AW_ex=self.rw[i]*self.kf/self.drw[i]
            self.AW.append(AW_ex)
            #print("AW",AW_ex)
    
    
        #CAW
        for i in range(0,self.NF+self.NC):
            CAW_exp=self.shi*self.AW[i]
            self.CAW.append(CAW_exp)
            #print(CAW_exp)
    
        #AE
        for i in range(0,self.NF+self.NC):
            if(i<=self.NF+self.NC-2):
                AE_exp=self.re[i]*self.kf/self.dre[i]
            else:
                AE_exp=0
            self.AE.append(AE_exp)
            #print(AE_ex)
    
    
        #CAE
        for i in range(0,self.NF+self.NC):
            CAE_exp=self.shi*self.AE[i]
            self.CAE.append(CAE_exp)
            #print(CAE_exp)
    
        #AQ
        for i in range(0,self.NF+self.NC):
            if(i<self.NF):
                self.Q=10000000
            else:
                self.Q=0
            if(i<=self.NF+self.NC):
                AQ_exp=0.5*((self.re[i]*self.re[i]-self.rw[i]*self.rw[i])*self.Q) 
            else:
                AQ_exp=0
            self.AQ.append(AQ_exp)
            #print(AQ_exp)
    
        #//!CAQ == where?
   
        #CAE
        for i in range(0,self.NF+self.NC):
            CAQ_exp=self.shi*self.AQ[i]
            self.CAQ.append(CAQ_exp)
            #print(CAQ_exp)

        #S
        for i in range(0,self.NF+self.NC):
            S_exp=self.CAQ[i]
            self.S.append(S_exp)
            #print(S_exp)
        
        #CAP
        for i in range(0,self.NF+self.NC):
            if(i<=self.NF+self.NC-1):
                CAP_exp=self.CAE[i]+self.CAW[i]
            elif(i==self.NF+self.NC-1):
                CAP_exp=self.CAW[i]
            self.CAP.append(CAP_exp)
            #print(CAP_exp)

        
        col_names=["CAW","CAE","CAP","S","AQ"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.CAW[i],self.CAE[i],self.CAP[i],self.S[i],self.AQ[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    
    def bc(self):
        ####Nuemann Left Boundary    at centerline
        self.CAW[0] = 0
        self.S[0] = self.S[0] + (self.shi*self.r[0]*self.qflux)


        #########%Robin's Right Boundary            at fuel and gap surface
        self.CAE[self.NF]=self.CAE[self.NF]+self.shi*self.r[self.NF]*self.HTC
        self.CAP[self.NF] = self.CAP[self.NF] + self.shi*self.r[self.NF]*self.HTC
        self.S[self.NF] = self.S[self.NF] + (self.shi*self.r[self.NF]*self.HTC*((self.T[self.NF]+self.T[self.NF+1])/2))

        ##Robin's Left Boundary                    AT GAP AND CLAD SURFACE
        self.CAW[self.NF+1] = self.CAW[self.NF+1]+self.shi*self.r[self.NF+1]*self.HTC
        self.CAP[self.NF+1] = self.CAP[self.NF+1] + self.shi*self.r[self.NF+1]*self.HTC
        self.S[self.NF+1] = self.S[self.NF+1] + (self.shi*self.r[self.NF+1]*self.HTC*((self.T[self.NF]+self.T[self.NF+1])/2)) 



        #########%Robin's Right Boundary            at CLAD and COOLANT surface
        self.CAE[self.NF+self.NC-1] = 0
        self.CAP[self.NF+self.NC-1] = self.CAP[self.NF+self.NC-1] + self.shi*self.r[self.NF+self.NC-1]*self.HTCC
        self.S[self.NF+self.NC-1] = self.S[self.NF+self.NC-1] + (self.shi*self.r[self.NF+self.NC-1]*self.HTCC*self.Tinf)

        #?print
        
        col_names=["CAW","CAE","CAP","S","AQ"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.CAW[i],self.CAE[i],self.CAP[i],self.S[i],self.AQ[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always")) 
    
    def TDMA_ST(self):
        for i in range(0,self.NT):
            if(i==0):
                Ai_exp=self.CAE[i]/self.CAP[i]
                Bi_exp=self.S[i]/self.CAP[i]
                self.Ai.append(Ai_exp)
                self.Bi.append(Bi_exp)

            elif(i==self.NT):
                Ai_exp=self.CAW[i]/self.CAP[i]
                Bi_exp=self.S[i]/self.CAP[i]
                self.Ai.append(Ai_exp)
                self.Bi.append(Bi_exp)


            else:
                Ai_exp=self.CAE[i]/(self.CAP[i]-(self.CAW[i]*self.Ai[i-1]))
                Bi_exp=(self.S[i]+(self.CAW[i]*(self.Bi[i-1])))/(self.CAP[i]-(self.CAW[i]*self.Ai[i-1]))
                self.Ai.append(Ai_exp)
                self.Bi.append(Bi_exp)
        
        col_names=["Ai","Bi"]
        data=[]
        for i in range(0,self.NT):
            data.append([self.Ai[i],self.Bi[i]])
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
        self.T[self.NT-1]=self.Bi[self.NT-1]
        for i in range(self.NT-2,0,-1):
            T_exp=(self.Ai[i]*self.T[i+1])+(self.Bi[i])
            self.T[i]=T_exp  
        self.T[0]=self.T[1]       
                                                  ############## CENTERLINE BC ISSUE RESOLVED
        print("T: ",self.T)
        return self.T
    
    def run(self):
        self.grid()
        self.coefff()
        self.bc()
        self.TDMA_ST()
    
    def prnt(self):
        plt.plot(self.r, self.T, label='Temperature vs. Radius')
        plt.xlabel('Radius')
        plt.ylabel('Temperature')
        plt.title('Temperature Profile')
        plt.legend()
        plt.show()

        col_names=["T","r"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.T[i],self.r[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))  