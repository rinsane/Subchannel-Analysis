from data import *

class FUNCTIONS(DATA):

    def grid(self):
        #Exactly same in steady and transient
        # drf and drc
        drf=self.R1/(self.NF-1)
        drc=(self.R3-self.R1-self.GT)/(self.NC-1)
        # if r is fine then the grid generation is automatically fine

        # r : radius maker for all dicrete domains
        for i in range(0, self.NF + self.NC):
            if i == 0:
                r_n = 0
            elif i <= self.NF - 2:
                r_n = r_o + drf
            elif i == self.NF - 1:
                r_n = self.R1
            elif i == self.NF:
                r_n = self.R1 + self.GT
            elif i <= self.NF + self.NC - 2:
                r_n = self.R1  + self.GT + drc * (i - self.NF)
            else:
                r_n = self.R3
            self.r.append(r_n)
            r_o = r_n
    
        # rw : list for Rw
        for i in range(0, self.NF + self.NC):
            if i == 0:
                rw_n = 0
            else:
                rw_n = 0.5 * (self.r[i] + self.r[i - 1])
            self.rw.append(rw_n)

        # re : list for Re
        for i in range(0, self.NF + self.NC):
            if i <= self.NF - 2:
                re_n = 0.5 * (self.r[i] + self.r[i + 1])
            elif i <= self.NF - 1:
                re_n = self.R1
            elif i <= self.NF + self.NC - 2:
                re_n = 0.5 * (self.r[i] + self.r[i + 1])
            else:
                re_n = self.R3
            self.re.append(re_n)

        # drw : list for Delta Rw
        for i in range(0, self.NF + self.NC):
            if i == 0:
                drw_n = 0
            else:
                drw_n = self.r[i] - self.r[i - 1]
            self.drw.append(drw_n)

        # dre : list for Delta Re
        for i in range(0, self.NF + self.NC):
            if i <= self.NF + self.NC - 2:
                dre_n = self.r[i + 1] - self.r[i]
            else:
                dre_n = 0
            self.dre.append(dre_n)


    def coefficient(self):
        # AW : (Rw*Kw) / (Rp - Rw)
        for i in range(0, self.NF + self.NC):
            if i == 0:
                AW_ex = 0
            else:
                AW_ex = self.rw[i] * self.kf[i] / self.drw[i]
            self.AW.append(AW_ex)      
        
        # CAW : Ψ * AW
        for i in range(0, self.NF + self.NC):
            CAW_exp = self.shi * self.AW[i]
            self.CAW.append(CAW_exp)
        
        # AE : (Re*Ke) / (Re - Rp)
        for i in range(0, self.NF + self.NC):
            if i <= self.NF + self.NC - 2:
                AE_exp = self.re[i] * self.kf[i] / self.dre[i]
            else:
                AE_exp = 0
            self.AE.append(AE_exp)      
        
        # CAE : Ψ * AE
        for i in range(0, self.NF + self.NC):
            CAE_exp = self.shi * self.AE[i]
            self.CAE.append(CAE_exp)
        
        # AQ : list of heat generation terms (conductance included)
        for i in range(0, self.NF + self.NC):
            if i <= self.NF + self.NC:  # Q taking conductance in considerations
                AQ_exp = 0.5 * ((self.re[i] * self.re[i] - self.rw[i] * self.rw[i]) * self.Q[i])
            else:                       # gap conductance
                AQ_exp = 0
            self.AQ.append(AQ_exp)

        # CAQ : Ψ * AQ
        for i in range(0, self.NF + self.NC):
            CAQ_exp = self.shi * self.AQ[i]
            self.CAQ.append(CAQ_exp)

        # AT : new Transient Term
        for i in range(0,self.NF+self.NC):
            AT_exp=(self.Rho[i]*self.C[i])*((self.re[i]**2)-(self.rw[i]**2))/(2*self.Dt)
            self.AT.append(AT_exp)
        
        
        # ATO : new Transient Term
        for i in  range(0,self.NF+self.NC):
            ATO_exp=(self.Rho_O[i]*self.C_O[i])*((self.re[i]**2)-(self.rw[i]**2))/(2*self.Dt)
            self.ATO.append(ATO_exp)
        
        # S : source terms
        for i in range(0, self.NF + self.NC):
            S_exp = self.CAQ[i] + self.ATO[i] * self.T_OLD[i]
            self.S.append(S_exp)

        # CAP : CAE + CAW + Transient Term (!= 0)
        for i in range(0, self.NF + self.NC):
            if i <= self.NF + self.NC - 1:
                CAP_exp = self.CAE[i] + self.CAW[i] + self.AT[i]
            elif i == self.NF + self.NC - 1:
                CAP_exp = self.CAW[i] + self.AT[i]
            self.CAP.append(CAP_exp)


    def conditioniser(self):
        # Nuemann Left Boundary [at CENTERLINE in FUEL ROD]
        self.CAW[0] = 0
        self.S[0] = self.S[0] + (self.shi*self.r[0]*self.qflux)

        # Robin's Right Boundary [at FUEL and GAP SURFACE]
        self.CAE[self.NF]=self.CAE[self.NF]+self.shi*self.r[self.NF]*self.HTC
        self.CAP[self.NF] = self.CAP[self.NF] + self.shi*self.r[self.NF]*self.HTC
        self.S[self.NF] = self.S[self.NF] + (self.shi*self.r[self.NF]*self.HTC*((self.T[self.NF]+self.T[self.NF+1])/2))

        # Robin's Left Boundary [at GAP and CLAD SURFACE]
        self.CAW[self.NF+1] = self.CAW[self.NF+1]+self.shi*self.r[self.NF+1]*self.HTC
        self.CAP[self.NF+1] = self.CAP[self.NF+1] + self.shi*self.r[self.NF+1]*self.HTC
        self.S[self.NF+1] = self.S[self.NF+1] + (self.shi*self.r[self.NF+1]*self.HTC*((self.T[self.NF]+self.T[self.NF+1])/2)) 

        # Robin's Right Boundary [at CLAD and COOLANT SURFACE]
        self.CAE[self.NF+self.NC-1] = 0
        self.CAP[self.NF+self.NC-1] = self.CAP[self.NF+self.NC-1] + self.shi*self.r[self.NF+self.NC-1]*self.HTCC
        self.S[self.NF+self.NC-1] = self.S[self.NF+self.NC-1] + (self.shi*self.r[self.NF+self.NC-1]*self.HTCC*self.Tinf)

        
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

        self.T_OLD[self.NT-1]=self.Bi[self.NT-1]
        for i in range(self.NT-2,-1,-1):
            T_to=(self.Ai[i]*self.T_OLD[i+1])+(self.Bi[i])
            self.T_OLD[i]=T_to  
        
        return self.T_OLD