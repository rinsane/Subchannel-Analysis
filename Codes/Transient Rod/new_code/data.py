import numpy as np

class Variables:
    def __init__(self):
        self.AE = []
        self.AQ = []
        self.ATO = []
        self.AT = []
        self.AW = []
        self.Bi = []
        self.C = []
        self.CAP = []
        self.CAQ = []
        self.CAW = []
        self.CAE=[]
        self.C_O = []
        self.Dt = 1e4
        self.GT = 0.003
        self.HTC = 7800
        self.HTCC = 3276
        self.NC = 400
        self.NF = 5000
        self.NG = 1  # Always take 1 node to solve for gap that is at intersection between fuel and clad
        self.NT = self.NF + self.NC
        self.Q = []
        self.R1 = 0.012
        self.R2 = 0.015
        self.R3 = 0.021
        self.Rho = []
        self.Rho_O = []
        self.S = []
        self.qflux = 0
        self.r = []
        self.re = []
        self.rw = []
        self.shi = 1
        self.t = 1
        self.Ai = []

        #kf=2.5  # thermal conductivity of fuel rod
        self.Tinf = 400
        self.dre = []
        self.drw = []
        self.kf = []
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
