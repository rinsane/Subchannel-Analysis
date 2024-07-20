class DATA:
    def __init__(self):
        self.AE     = []    # (Re*Ke) / (Re - Rp)
        self.CAE    = []    # Ψ * AE
        self.AW     = []    # (Rw*Kw) / (Rp - Rw)
        self.CAW    = []    # Ψ * AW
        self.AQ     = []    # Q taking conductance in considerations
        self.CAQ    = []    # Ψ * AQ
        self.CAP    = []    # CAE + CAW + Transient Term (= 0)

        self.Ai     = []    # helper used in TDMA
        self.Bi     = []    # helper used in TDMA 
        self.re     = []    # (ri + r(i+1))/2
        self.rw     = []    # (r(i-1) + ri)/2
        
        self.dre    = []    # delta Re
        self.drw    = []    # delta Rw
        
        self.R1     = 0.006
        self.R2     = 0.0062
        self.GT     = self.R2 - self.R1
        
        self.HTC    = 5500  # Heat Transfer Coefficient (fuel - gap - clad)
        self.HTCC   = 3840  # Heat Transfer Coefficient (clad - coolant)
        
        self.kf     = 5.88   # thermal conductivity of fuel rod
        self.kc     = 16   # thermal conductivity of clad
        
        self.NG     = 1     # ALWAYS TAKE 1 NODE TO SOLVE FOR GAP THAT IS AT INTERSECTION BETWEEN FUEL AND CLAD  
        self.NC     = 4     # Number of domanins in cladding
        self.NF     = 8     # Number of domains in fuel rods
        self.NT     = self.NF + self.NC # Total number of domains.
         
        self.qflux  = 34285.71
        
        self.r      = []
        self.R3     = 0.0072
        
        self.S      = []
        self.shi    = 1     # implicit factor
        
        self.T      = [0 for _ in range(self.NF + self.NC)]
        print(self.T)
        self.Tinf   = 590