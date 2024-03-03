from inputs import*
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

class func(Variables):
    #i don't know;;''''''...//
    def grid(self):
        self.drf=self.R1/(self.NF-1)
        self.drc=(self.R3-self.R1-self.GT)/(self.NC-1)
        ### if r is fine the grid gen is automatically fine

        #r
        for i in range(0,self.NF+self.NC):
            if(i==0):
                r_n=0
            elif(i<=self.NF-2):
                r_n=r_o+self.drf
            elif(i<self.NF):
                r_n=self.R1
            elif(i==self.NF):
             r_n=self.R1+self.GT
            elif(i<=self.NF+self.NC-2):
                r_n=self.R1+self.GT+self.drc*(i-(self.NF))
            else:
                r_n=self.R3
            self.r.append(r_n)
            r_o=r_n                                                                                     ####SOME  PROBLEM LIES WITH NC JUST IDENTIFY NOT GIVING GOOD RESULTS
            print(r_n)                                                                         
            ## some issue with last node
            ## some issue with last node
    
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
                dre_n=0                                                                         ###  can be 
            self.dre.append(dre_n)
            #print(dre)
    
        col_names=["r","rw","re","drw","dre"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.r[i],self.rw[i],self.re[i],self.drw[i],self.dre[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    
    #for calculating all the coefficients
    def coeff_T(self):
        self.AE.clear()
        self.AW.clear()
        self.AT.clear()
        self.ATO.clear()
        self.AQ.clear()
        self.CAW.clear()
        self.CAE.clear()
        self.CAQ.clear()
        self.CAP.clear()
        self.S.clear()
    
    
        #AW
        for i in range(0,self.NF+self.NC):
            if(i==0):
                AW_ex=0
            else:
                AW_ex=self.rw[i]*self.kf[i]/self.drw[i]
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
                AE_exp=self.re[i]*self.kf[i]/self.dre[i]
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
            if(i<=self.NF+self.NC):
                AQ_exp=0.5*((self.re[i]*self.re[i]-self.rw[i]*self.rw[i])*self.Q[i]) 
            else:
                AQ_exp=0
            self.AQ.append(AQ_exp)
        
        #CAQ
        for i in range(0,self.NF+self.NC):
            CAQ_exp=self.shi*self.AQ[i]
            self.CAQ.append(CAQ_exp)


        #AT
        for i in range(0,self.NF+self.NC):
            AT_exp=(self.Rho[i]*self.C[i])*((self.re[i]**2)-(self.rw[i]**2))/(2*self.Dt)
            self.AT.append(AT_exp)
            # print("AT: ",AT)
        
        
        #ATO
        for i in  range(0,self.NF+self.NC):
            ATO_exp=(self.Rho_O[i]*self.C_O[i])*((self.re[i]**2)-(self.rw[i]**2))/(2*self.Dt)
            self.ATO.append(ATO_exp)
            #print("ATO",ATO)
        
        #S
        for i in range(0,self.NF+self.NC):
            S_exp=self.CAQ[i]+self.ATO[i]*self.T_OLD[i]
            self.S.append(S_exp)
            #print(S_exp)
            
        #CAP
        for i in range(0,self.NF+self.NC):
            if(i<=self.NF+self.NC-1):
                CAP_exp=self.CAE[i]+self.CAW[i]+self.AT[i]
            elif(i==self.NF+self.NC-1):
                CAP_exp=self.CAW[i]+self.AT[i]
            self.CAP.append(CAP_exp)
            #print(CAP_exp)
        
        col_names=["CAW","CAE","CAP","S","AQ","AT","ATO"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.CAW[i],self.CAE[i],self.CAP[i],self.S[i],self.AQ[i],self.AT[i],self.ATO[i]])
        
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))
    
    #for calculating coefficients for boundary condition coefficients
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

        col_names=["CAW","CAE","CAP","S","AQ","AT","ATO"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.CAW[i],self.CAE[i],self.CAP[i],self.S[i],self.AQ[i],self.AT[i],self.ATO[i]])
    
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))

    #Obviously to calculate Temperatures using TDMA
    def TDMA(self):
        for i in range(0,self.NT):
            if(i==0):
                    Ai_exp=self.CAE[i]/self.CAP[i]
                    Bi_exp=self.S[i]/self.CAP[i]
                    self.Ai.append(Ai_exp)
                    self.Bi.append(Bi_exp)
            else:
                    Ai_exp=self.CAE[i]/(self.CAP[i]-(self.CAW[i]*self.Ai[i-1]))
                    Bi_exp=(self.S[i]+(self.CAW[i]*(self.Bi[i-1])))/(self.CAP[i]-(self.CAW[i]*self.Ai[i-1]))
                    self.Ai.append(Ai_exp)
                    self.Bi.append(Bi_exp)
            
        print("Ai: ",self.Ai)
        print("Bi: ",self.Bi)
    
        self.T_OLD[self.NT-1]=self.Bi[self.NT-1]
        for i in range(self.NT-2,-1,-1):
            T_to=(self.Ai[i]*self.T_OLD[i+1])+(self.Bi[i])
            self.T_OLD[i]=T_to  
        # T[0]=T[1]       
                                              ############## CENTERLINE BC ISSUE RESOLVED
        print("T: ",self.T_OLD)
        col_names=["T","r"]
        data=[]
        for i in range(0,self.NF+self.NC):
            data.append([self.T_OLD[i],self.r[i]])
        print(tabulate(data,headers=col_names,tablefmt="fancy_grid",showindex="always"))


        plt.plot(self.r, self.T_OLD, label='Temperature vs. Radius')
        plt.xlabel('Radius')
        plt.ylabel('Temperature')
        plt.title('Temperature Profile')
        plt.legend()
        plt.show() 
        return (T_OLD)
    

    #runs all the functions in sequence and generates temperature profile for grid
    def run(self):
        self.grid()
        self.coeff_T()
        self.bc()
        self.TDMA()
        self.T_total=[]
        for i in range(0,(self.t*1)):
            self.Ai.clear()
            self.Bi.clear()
            if(i==1):
                self.T[self.NT-1]=0
                self.T_OLD[:]=self.T[:]
            else:
                #coeff_T()
                self.T_t[:]=self.TDMA_T()
                print("T: ",self.T_t)
                self.T_OLD[:]=self.T_t[:]
                print("T_old",self.T_OLD)
    
            ######saving results in an array####
            if(i==0):
                self.T_total.append(self.T[:])
            else:
                self.T_total.append(T_OLD[:])
            print("T_total: ",self.T_total)

        # col_names = ['time(sec)','temperature']
         # data = []
        # for i in range(0, (t*100)):
        #    data.append([i+1,T_total[i]])

        # print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))   
            #forming tabular form

        for i in range(0,(self.t*1)):
            if(i==0):
                print("T_steady: ",self.T_total[i])
            elif(i==(t)-1):
                print("T_last: ",self.T_total[i])
        for i in range(0,(self.t*1)):
            if(i==0):
                plt.plot(self.r,self.T_total[i],label='steady')
        else:
               plt.plot(self.r,self.T_total[i],label='transient')
        plt.xlabel('lenght')
        plt.ylabel('temperature')
        plt.title('temperature vs length')
        plt.legend()
        plt.show()