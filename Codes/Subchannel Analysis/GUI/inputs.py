# Fi   -> F(i+1) (masflo)
# Hi   -> H(i+1) (HM)
# WIJi -> WIJ(i+1) (dcross)
# Pi -> P(i+1) (aximom)

class variables:

   ALPHA    = 0         # angle at which rods are inclined               
   AXLN     = 0         # axial length of fuel rod                       
   DELTA    = 0         # correction factor             
   FACK     = 0         # momentum correction factor             
   FT       = 0         # turbulent factor used to compensate imperfect analogy bw turbulent transport of enthalpy and momentum                      
   GAMA     = 0         # correction factor                 
   GC       = 0         # g: acceleration due to gravity               
   NCHANL   = 0         # no of subchannel               
   NK       = 0         # no of connections                    
   NNODE    = 0         # number of nodes                           
   RDIA     = 0         # diameter of fuel rod                    
   RHO      = 0         # density at given system pressure                      
   SLP      = 0         # (slip) ratio of length between subchannel centroids to the width of the control volume                                                          
   THETA    = 0         # implicit factor                              
   VISC     = 0         # viscosity
   PIN      = 0         # pressure input
   hf       = 0         # heat flux
   h0       = 0         # initial enthalpy

   # Gap between adjacent subchannel (NK items)
   GAP      = []
   # Hydraulic Diameter (NCHANL)
   HDIA     = []   
   # Heated Perimeter (NCHANL)
   HPERI    = []
   # representation of interconnections of different subchannels IC -- slef , JC -- adjacent (NK)
   IC       = []
   JC       = []
   # A -- Area constant of every subchannel (NCHANL)
   A        = []
   # F0 -- initial mass flow rate for 14 subchannels, F1 --final mass flow rate for 14 subchannels, temp variable for copying F11 (NCHANL)
   F0       = []
   # heat flux (constant)
   HF        = []
   # H0 - initial enthalpy of sub-channels,, H1 -final enthalpy of sub-channels,
   H0        = []

   #RHOF    =741.6198525                              #################### DENSITY OF liquid at given constant presure
   #RHOG    =35.90645107                              #################### DENSITY OF VAPOR AT GIVEN CONSTANT PRESSURE
            
   def init(self):
            
      self.DELX      = self.AXLN/(self.NNODE-1)
      
      # Matrix B -- used in XB sub rooutine, B0 and B1 support variables in XB
      self.B         = [0] * self.NCHANL
      self.B1        = [0] * self.NCHANL
      self.B2        = [0] * self.NCHANL

      # Used in HM -- c1,c2.c3
      self.C1        = [0] * self.NCHANL
      self.C2        = [0] * self.NCHANL
      self.C3        = [0] * self.NCHANL

      # rotine xd -- cij0, cij1
      self.CIJ0      = [0] * self.NK
      self.CIJ1      = [0] * self.NK

      # Matrix D -- calculated by XD
      self.D         = [0] * self.NK

      # Matrix DELH -- enthalpy diff between 2 adjacent subchannel
      self.DELH      = [0] * self.NK

      # General Purpose use -- size NK
      self.ERR       = [0] * self.NK
      self.ERROR     = [0] * self.NK
      self.F1        = [0] * self.NCHANL
      self.F11       = [0] * self.NK
      self.H1        = [0] * self.NK

      # Cross Flow enthalpy -- calculated in HM
      self.HSTAR     = [0] * self.NK

      '''P0 -- initial press, P1 -- outlet pressure, P11 -- temp var for copying P1
      PB - used in main file for calculating source of gauss sub routine
      PM0 -- used in main file can be removed 
      '''

      self.P0        = [0] * self.NK
      self.P1        = [0] * self.NK
      self.P11       = [0] * self.NK
      self.PB        = [0] * self.NK
      self.PM0       = [0] * self.NK

      # Heat generation inside the channel
      self.Q         = [0] * self.NCHANL

      # Reynold number
      self.RE        = [0] * self.NK

      # S -- connecting matrix , calculated by SKI, ST -- transpose of S calculated by SKI
      # temp vars
      self.S         = [[0] * self.NK for _ in range(self.NK)]
      self.S5        = [[0] * self.NK for _ in range(self.NK)]

      # defn moved in XB --  self.SAVE    = np.zeros(self.NK)
      self.SD        = [[0] * self.NK for _ in range(self.NK)]
      self.SS        = [0] * self.NCHANL
      self.ST        = [[0.0] * self.NK for _ in range(self.NK)]

      # USTAR0 -- initial velocity, USTAR1 -- final velocity, USTAR D1 -- temp VAR for USTD1
      self.USTAR0    = [0.0] * self.NK
      self.USTAR1    = [0.0] * self.NK
      self.USTD1     = [0] * self.NK

      # all used in D corss
      self.W2        = [0] * self.NK
      self.WIJ0      = [0] * self.NK
      self.WIJ1      = [0] * self.NK
      self.WIJIN     = 0.0

      # used in wprim routine
      self.WPR       = [0] * self.NK

      '''
      XA -- matrix a
      XDELH -- Sub-routine HM
      XH, XHS, XHST -- subroutine HM
      XM,XM0,XMI -- used in main for calculation M in main
      XMLT -- used in calculation of S, ST*Ustar1
      XUST0,XUST1 -- used in star sub-routine
      '''

      self.XA        = [0] * self.NCHANL
      self.XDELH     = [[0] * self.NK for _ in range(self.NK)]
      self.XH        = [[0] * self.NCHANL for _ in range(self.NCHANL)]
      self.XHS       = [[0] * self.NK for _ in range(self.NK)]
      self.XHST      = [[0] * self.NK for _ in range(self.NK)]
      self.XM        = [[0] * self.NK for _ in range(self.NK)]
      self.XM0       = [[0] * self.NK for _ in range(self.NK)]
      self.XMI       = [[0] * self.NK for _ in range(self.NK)]
      self.XMLT      = [[0] * self.NK for _ in range(self.NK)]
      self.XUST0     = [[0.0] * self.NK for _ in range(self.NK)]
      self.XUST1     = [[0.0] * self.NK for _ in range(self.NK)]
      self.XUSTD1    = [[0] * self.NK for _ in range(self.NK)]
      
      # matrix calculation for ft*stranspose*delu*wpr/area
      self.XY        = [0.0] * self.NCHANL
      
      # used in wprim routine
      self.XZ        = [0.0] * self.NK

      # used in AXIMOM
      self.YU1       = [[0] * self.NK for _ in range(self.NK)]

      # introduction of void fraction and real quality of system
      self.VOID0     = [0] * self.NCHANL
      self.VOID1     = [0] * self.NCHANL
      self.QUALITY0  = [0] * self.NCHANL
      self.QUALITY1  = [0] * self.NCHANL