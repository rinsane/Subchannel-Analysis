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

   #RHOF    =741.6198525                              #################### DENSITY OF liquid at given constant presure
   #RHOG    =35.90645107                              #################### DENSITY OF VAPOR AT GIVEN CONSTANT PRESSURE
            
   def init(self):
      
      # heat flux (constant)
      self.HF        = [self.hf] * self.NCHANL
      # H0 - initial enthalpy of sub-channels,, H1 -final enthalpy of sub-channels,
      self.H0        = [self.h0] * self.NCHANL
      
      self.DELX      = self.AXLN/(self.NNODE-1)
      
      # Matrix B -- used in XB sub rooutine, B0 and B1 support variables in XB
      self.B         = [0] * variables.NCHANL
      self.B1        = [0] * variables.NCHANL
      self.B2        = [0] * variables.NCHANL

      # Used in HM -- c1,c2.c3
      self.C1        = [0] * variables.NCHANL
      self.C2        = [0] * variables.NCHANL
      self.C3        = [0] * variables.NCHANL

      # rotine xd -- cij0, cij1
      self.CIJ0      = [0] * variables.NK
      self.CIJ1      = [0] * variables.NK

      # Matrix D -- calculated by XD
      self.D         = [0] * variables.NK

      # Matrix DELH -- enthalpy diff between 2 adjacent subchannel
      self.DELH      = [0] * variables.NK

      # General Purpose use -- size NK
      self.ERR       = [0] * variables.NK
      self.ERROR     = [0] * variables.NK
      self.F1        = [0] * variables.NCHANL
      self.F11       = [0] * variables.NK
      self.H1        = [0] * variables.NK

      # Cross Flow enthalpy -- calculated in HM
      self.HSTAR     = [0] * variables.NK

      '''P0 -- initial press, P1 -- outlet pressure, P11 -- temp var for copying P1
      PB - used in main file for calculating source of gauss sub routine
      PM0 -- used in main file can be removed 
      '''

      self.P0        = [0] * variables.NK
      self.P1        = [0] * variables.NK
      self.P11       = [0] * variables.NK
      self.PB        = [0] * variables.NK
      self.PM0       = [0] * variables.NK

      # Heat generation inside the channel
      self.Q         = [0] * variables.NCHANL

      # Reynold number
      self.RE        = [0] * variables.NK

      # S -- connecting matrix , calculated by SKI, ST -- transpose of S calculated by SKI
      # temp vars
      self.S         = [[0] * variables.NK for _ in range(variables.NK)]
      self.S5        = [[0] * variables.NK for _ in range(variables.NK)]

      # defn moved in XB --  self.SAVE    = np.zeros(variables.NK)
      self.SD        = [[0] * variables.NK for _ in range(variables.NK)]
      self.SS        = [0] * variables.NCHANL
      self.ST        = [[0.0] * variables.NK for _ in range(variables.NK)]

      # USTAR0 -- initial velocity, USTAR1 -- final velocity, USTAR D1 -- temp VAR for USTD1
      self.USTAR0    = [0.0] * variables.NK
      self.USTAR1    = [0.0] * variables.NK
      self.USTD1     = [0] * variables.NK

      # all used in D corss
      self.W2        = [0] * variables.NK
      self.WIJ0      = [0] * variables.NK
      self.WIJ1      = [0] * variables.NK
      self.WIJIN     = 0.0

      # used in wprim routine
      self.WPR       = [0] * variables.NK

      '''
      XA -- matrix a
      XDELH -- Sub-routine HM
      XH, XHS, XHST -- subroutine HM
      XM,XM0,XMI -- used in main for calculation M in main
      XMLT -- used in calculation of S, ST*Ustar1
      XUST0,XUST1 -- used in star sub-routine
      '''

      self.XA        = [0] * variables.NCHANL
      self.XDELH     = [[0] * variables.NK for _ in range(variables.NK)]
      self.XH        = [[0] * variables.NCHANL for _ in range(variables.NCHANL)]
      self.XHS       = [[0] * variables.NK for _ in range(variables.NK)]
      self.XHST      = [[0] * variables.NK for _ in range(variables.NK)]
      self.XM        = [[0] * variables.NK for _ in range(variables.NK)]
      self.XM0       = [[0] * variables.NK for _ in range(variables.NK)]
      self.XMI       = [[0] * variables.NK for _ in range(variables.NK)]
      self.XMLT      = [[0] * variables.NK for _ in range(variables.NK)]
      self.XUST0     = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUST1     = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUSTD1    = [[0] * variables.NK for _ in range(variables.NK)]
      
      # matrix calculation for ft*stranspose*delu*wpr/area
      self.XY        = [0.0] * variables.NCHANL
      
      # used in wprim routine
      self.XZ        = [0.0] * variables.NK

      # used in AXIMOM
      self.YU1       = [[0] * variables.NK for _ in range(variables.NK)]

      # introduction of void fraction and real quality of system
      self.VOID0     = [0] * variables.NCHANL
      self.VOID1     = [0] * variables.NCHANL
      self.QUALITY0  = [0] * variables.NCHANL
      self.QUALITY1  = [0] * variables.NCHANL