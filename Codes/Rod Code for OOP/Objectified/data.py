class DATA:
    def __init__(self):
        self.AE     = []
        self.Ai     = []
        self.AQ     = []
        self.AW_ex  = []
        self.AW     = []

        self.Bi     = []
         
        self.CAE    = []
        self.CAP    = []
        self.CAQ    = []
        self.CAW    = []
        
        self.dre    = []
        self.drw    = []
        
        self.R1     = 0.012
        self.R2     = 0.015
        self.GT     = self.R2 - self.R1
        
        self.HTC    = 7800
        self.HTCC   = 3840
        
        self.kf     = 2.5   # thermal conduvtivity of fuel rod
        
        self.NG     = 1     # ALWAYS TAKE 1 NODE TO SOLVE FOR GAP THAT IS IT IS AT INTERSECTION BETWEEN FUEL AND CLAD  
        self.NC     = 8                                   
        self.NF     = 13
        self.NT     = self.NF + self.NC
         
        self.Q      = 10e6
        self.qflux  = 0
        
        self.r      = []
        self.R3     = 0.021
        self.re     = []
        self.rw     = []
        
        self.S      = []
        self.shi    = 1
        
        self.T      = [0 for i in range(self.NF + self.NC)]
        print(self.T)
        self.Tinf   = 400