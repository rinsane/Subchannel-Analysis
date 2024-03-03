import numpy as np

class Variables:
    def __init__(self):
        self.AE = [] # (Re*Ke) / (Re - Rp)
        self.AQ = [] # Q taking conductance in considerations
        self.ATO = [] #
        self.AT = []
        self.AW = [] # (Rw*Kw) / (Rp - Rw)
        self.Bi = []
        self.C = []
        self.CAP = [] # CAE + CAW + Transient Term (= 0)
        self.CAQ = []   # Ψ * AQ
        self.CAW = [] # Ψ * AW
        self.CAE=[] # Ψ * AE
        self.C_O = []
        self.Dt = 1
        self.GT = 0.003
<<<<<<< HEAD:Codes/Transient/new code/inputs.py
        self.HTC = 7800 # Heat Transfer Coefficient (fuel - gap - clad)
        self.HTCC = 3276 # Heat Transfer Coefficient (clad - coolant)
        self.NC = 400  # Number of domanins in cladding
        self.NF = 5000 # Number of domains in fuel rods
=======
        self.HTC = 7800
        self.HTCC = 3276
        self.NC = 400
        self.NF = 5000
>>>>>>> 9cbfc5161ed5998bf3d70c04b6e4604ae862f365:Codes/Transient Rod/new_code/data.py
        self.NG = 1  # Always take 1 node to solve for gap that is at intersection between fuel and clad
        self.NT = self.NF + self.NC
        self.Q = []
        self.R1 = 0.012
        self.R2 = 0.015
        self.R3 = 0.021
        self.Rho = []
        self.Rho_O = []
        self.S = []
        self.T_OLD = []
        self.qflux = 0
        self.r = [] 
        self.re = []    #(ri + r(i+1))/2
        self.rw = []    # (r(i-1) + ri)/2
        self.shi = 1  # implicit factor
        self.t = 1
        self.Ai = []

        #kf=2.5  # thermal conductivity of fuel rod
        self.Tinf = 400
        self.dre = []   # delta Re
        self.drw = []   # delta Rw
        self.kf = [] # thermal conduvtivity of fuel rod
        self.T = [0 for _ in range(0, self.NF + self.NC)]
        self.T_OLD = [self.T[i] for i in range(self.NF + self.NC)]
        self.T_t = []

        for i in range(0, self.NF + self.NC):
            if i <= self.NF:
                self.Q.append(1e7)
                self.Rho.append(18900)
                self.Rho_O.append(18900)
                self.C.append(120)
                self.C_O.append(120)
                self.kf.append(10)
            else:
                self.Q.append(0)
                self.Rho.append(6510)
                self.Rho_O.append(6510)
                self.C.append(270)
                self.C_O.append(270)
                self.kf.append(20)
