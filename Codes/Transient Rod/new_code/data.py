class DATA:
    def __init__(self):
        self.AE     = []    # (Re*Ke) / (Re - Rp)
        self.CAE    = []    # Ψ * AE
        self.AW     = []    # (Rw*Kw) / (Rp - Rw)
        self.CAW    = []    # Ψ * AW
        self.AQ     = []    # Q taking conductance in considerations
        self.CAQ    = []     # Ψ * AQ
        self.CAP    = []    # CAE + CAW + Transient Term (= 0 maybe but ut was written in steady state code)
        
        self.Ai     = []    # helper used in TDMA
        self.Bi     = []    # helper used in TDMA
        self.re     = []    # (ri + r(i+1))/2
        self.rw     = []    # (r(i-1) + ri)/2
        
        self.dre    = []    # delta Re
        self.drw    = []    # delta Rw
        
        self.R1     = 0.012
        self.R2     = 0.015
        self.GT     = self.R2 - self.R1
        
        self.HTC    = 7800  # Heat Transfer Coefficient (fuel - gap - clad)
        self.HTCC   = 3276  # Heat Transfer Coefficient (clad - coolant)
        
        self.kf     = []    # thermal conduvtivity of fuel rod
        
        self.NG     = 1  # Always take 1 node to solve for gap that is at intersection between fuel and clad
        self.NC     = 8     # Number of domanins in cladding
        self.NF     = 13    # Number of domains in fuel rods
        self.NT     = self.NF + self.NC # Total number of domains.
        
        self.qflux  = 0
        
        self.r      = []
        self.R3 = 0.021
        
        self.S      = []
        self.shi    = 1     # implicit factor
        
        self.T      = [0 for _ in range(0, self.NF + self.NC)]
        self.Tinf   = 400
        
        self.Dt     = 1e8
        self.t      = 1
        
        self.ATO    = []
        self.AT     = []
        self.C      = []
        
        self.C_O    = []
        self.Q      = []
        self.Rho    = []
        self.Rho_O  = []
        #kf=2.5  # thermal conductivity of fuel rod
        self.T_OLD  = [self.T[i] for i in range(self.NF + self.NC)]
        self.T_t    = []
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