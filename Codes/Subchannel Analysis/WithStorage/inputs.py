# Fi   -> F(i+1) (masflo)
# Hi   -> H(i+1) (HM)
# WIJi -> WIJ(i+1) (dcross)
# Pi -> P(i+1) (aximom)

class variables:

   '''
   ALPHA   = 90         # angle at which rods are inclined                                                       
   AXLN    = 0.1        # axial length of fuel rod                                                    
   DELTA   = 0.5        # correction factor                                                  
   FACK    = 0.01       # momentum correction factor                                                              
   FT      = 0.1        # turbulent factor used to compensate imperfect analogy                                 
                        # bw turbulent transport of enthalpy and momentum                                      
   GAMA    = 0.5        # correction factor                                                                                
   GC      = 9.81       # g                                                                                 
   NCHANL  = 14         # no of subchannel                                                      
   NK      = 19         # no of connections                                                        
   NNODE   = 500        # number of nodes                                                    
   RDIA    = 0.01308    # diameter of fuel rod                                               
   RHO     = 817.4      # density at given system pressure                                            
   SLP     = 0.5        # (slip) ratio of length between subchannel centroids                                                 
                        # to the width of the control volume                                                
   THETA   = 0.5        # implicit factor                                                                
   VISC    = 0.000011   # viscosity  
                        # Pressure input                                                             
   '''

   ALPHA   = 90                     
   AXLN    = 0.01                                     
   DELTA   = 0.5                          
   FACK    = 0.01                      
   FT      = 0.02                            

   GAMA    = 0.5                          
   GC      = 9.81                         
   NCHANL  = 65                        
   NK      = 109                             
   NNODE   = 20                                    
   RDIA    = 0.0094                             
   RHO     = 841.31                                
   SLP     = 0.5   
                                                                       
   THETA   = 0.5                                      
   VISC    = 0.000120838
   DELX    = AXLN/(NNODE-1)

   # gap between adjacent subchannel (NK items)
   GAP     = [0.00335,0.00335,0.00335,0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335,	0.00335,	0.00335,	0.001675,	0.00335]
   #Hydraulic Diameter (NCHANL)
   HDIA    = [0.007508595	,0.007508595,	0.007508595,	0.007508595,	0.007508595,	0.007508595,	0.007508595,	0.007508595	,0.007508595,	0.007508595,	0.005445763,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042	,0.00868042	,0.00868042,	0.00868042,	0.00868042	,0.00868042,	0.00868042,	0.005445763	,0.00868042,	0.00868042,	0.00868042	,0.00868042	,0.00868042,	0.00868042,	0.00868042,	0.005445763,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.00868042,	0.005445763,	0.00868042,	0.00868042	,0.00868042,	0.00868042,	0.00868042,	0.005445763,	0.00868042,	0.00868042,	0.00868042,	0.00868042	,0.005445763,	0.00868042,	0.00868042,	0.00868042,	0.005445763,	0.00868042,	0.00868042,	0.005445763,	0.00868042,	0.005445763,	0.005445763]

   #Heat Generation per unit volume  might be kw/m^2
   
   #Heated Perimeter (NCHANL)
   HPERI   = [0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.024815485,	0.034215485,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.034215485,	0.042930971,	0.042930971,	0.042930971,	0.042930971	,0.042930971,	0.042930971,	0.042930971,	0.034215485,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.042930971,	0.034215485	,0.042930971	,0.042930971,	0.042930971,	0.042930971,	0.042930971	,0.034215485,	0.042930971,	0.042930971	,0.042930971,	0.042930971	,0.034215485,	0.042930971,	0.042930971,	0.042930971,	0.034215485	,0.042930971,	0.042930971	,0.034215485,	0.042930971	,0.034215485	,0.034215485]
   # representation of interconnections of different subchannels IC -- slef , JC -- adjacent (NK)
   IC      = [1,	2,	2,	3,	3,	4,	4,	5,	5,	6,	6,	7,	7,	8,	8,	9,	9,	10,	10,	11,	12,	13,	13,	14,	14,	15,	15,	16,	16,	17,	17,	18,	18,	19,	19,	20,	20,	29,	21,	22,	22,	23,	23,	24,	24,	25,	25,	26,	26,	27,	27,	28,	28,	37,	30,	31,	31,	32,	32,	33,	33,	34,	34,	35,	35,	36,	36,	44,	38,	39,	39,	40,	40,	41,	41,	42,	42,	43,	43,	50,	45,	46,	46,	47,	47,	48,	48,	49,	49,	55,	51,	52,	52,	53,	53,	54,	54,	59,	56,	57,	57,	58,	58,	62,	60,	61,	61,	64,	63] 
   JC      = [12,	12,	13,	13,	14,	14,	15,	15,	16,	16,	17,	17,	18,	18,	19,	19,	20,	20,	11,	29,	21,	21,	22,	22,	23,	23,	24,	24,	25,	25,	26,	26,	27,	27,	28,	28,	29,	37,	30,	30,	31,	31,	32,	32,	33,	33,	34,	34,	35,	35,	36,	36,	37,	44,	38,	38,	39,	39,	40,	40,	41,	41,	42,	42,	43,	43,	44,	50,	45,	45,	46,	46,	47,	47,	48,	48,	49,	49,	50,	55,	51,	51,	52,	52,	53,	53,	54,	54,	55,	59,	56,	56,	57	,57,	58,	58,	59,	62,	60,	60,	61,	61,	62,	64,	63,	63,	64,	65,	65]
   
   # pressure input
   PIN     = 11000000
   #RHOF    =741.6198525                              #################### DENSITY OF liquid at given constant presure
   #RHOG    =35.90645107                              #################### DENSITY OF VAPOR AT GIVEN CONSTANT PRESSURE

   #A -Area -- constant of every subchannel (NCHANL)
   A       = [3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,3.56907E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,9.31647E-05,4.65824E-05,9.31647E-05,4.65824E-05,4.65824E-05]
   # input mass flow rate
   # F0 -- initial mass flow rate for 14 subchannels, F1 --final mass flow rate for 14 subchannels, temp variable for copying F11 (NCHANL)
   F0 = [0.025757576,	0.025757576	,0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.025757576,	0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152,	0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152	,0.051515152,	0.051515152,	0.051515152	,0.051515152,	0.025757576,	0.051515152,	0.051515152,	0.051515152	,0.051515152,	0.051515152	,0.051515152,	0.051515152,	0.025757576	,0.051515152,	0.051515152,	0.051515152,	0.051515152,	0.051515152,	0.051515152,	0.025757576,	0.051515152,	0.051515152,	0.051515152,	0.051515152,	0.051515152	,0.025757576,	0.051515152,	0.051515152,	0.051515152,	0.051515152,	0.025757576	,0.051515152	,0.051515152,	0.051515152,	0.025757576	,0.051515152,	0.051515152	,0.025757576	,0.051515152,	0.025757576	,0.025757576]
   # heat flux (constant)
   HF = [286.4522984] * NCHANL
   # H0 - initial enthalpy of sub-channels,, H1 -final enthalpy of sub-channels,
   # inlet enthalpy (KJ/kg)
   H0 = [969] * NCHANL
            
   def __init__(self):

      # Matrix B -- used in XB sub rooutine, B0 and B1 support variables in XB
      self.B = [0] * variables.NCHANL
      self.B1 = [0] * variables.NCHANL
      self.B2 = [0] * variables.NCHANL

      # Used in HM -- c1,c2.c3
      self.C1 = [0] * variables.NCHANL
      self.C2 = [0] * variables.NCHANL
      self.C3 = [0] * variables.NCHANL
      # rotine xd -- cij0, cij1
      self.CIJ0 = [0] * variables.NK
      self.CIJ1 = [0] * variables.NK

      # Matrix D -- calculated by XD
      self.D = [0] * variables.NK
      # Matrix DELH -- enthalpy diff between 2 adjacent subchannel
      self.DELH = [0] * variables.NK

      # General Purpose use -- size NK
      self.ERR = [0] * variables.NK
      self.ERROR = [0] * variables.NK

      self.F1 = [0] * variables.NCHANL
      self.F11 = [0] * variables.NK

      self.H1 = [0] * variables.NK

      # Cross Flow enthalpy -- calculated in HM
      self.HSTAR = [0] * variables.NK

      '''P0 -- initial press, P1 -- outlet pressure, P11 -- temp var for copying P1
      PB - used in main file for calculating source of gauss sub routine
      PM0 -- used in main file can be removed 
      '''
      self.P0 = [0] * variables.NK
      self.P1 = [0] * variables.NK
      self.P11 = [0] * variables.NK
      self.PB = [0] * variables.NK
      self.PM0 = [0] * variables.NK

      # Heat generation inside the channel
      self.Q = [0] * variables.NCHANL

      # Reynold number
      self.RE = [0] * variables.NK

      # S -- connecting matrix , calculated by SKI, ST -- transpose of S calculated by SKI
      # temp vars
      self.S = [[0] * variables.NK for _ in range(variables.NK)]
      self.S5 = [[0] * variables.NK for _ in range(variables.NK)]
      # defn moved in XB --  self.SAVE    = np.zeros(variables.NK)
      self.SD = [[0] * variables.NK for _ in range(variables.NK)]
      self.SS = [0] * variables.NCHANL
      self.ST = [[0.0] * variables.NK for _ in range(variables.NK)]

      # USTAR0 -- initial velocity, USTAR1 -- final velocity, USTAR D1 -- temp VAR for USTD1
      self.USTAR0 = [0.0] * variables.NK
      self.USTAR1 = [0.0] * variables.NK
      self.USTD1 = [0] * variables.NK

      # all used in D corss
      self.W2 = [0] * variables.NK
      self.WIJ0 = [0] * variables.NK
      self.WIJ1 = [0] * variables.NK
      self.WIJIN = 0.0
      # used in wprim routine
      self.WPR = [0] * variables.NK

      '''
      XA -- matrix a
      XDELH -- Sub-routine HM
      XH, XHS, XHST -- subroutine HM
      XM,XM0,XMI -- used in main for calculation M in main
      XMLT -- used in calculation of S, ST*Ustar1
      XUST0,XUST1 -- used in star sub-routine

      '''
      self.XA = [0] * variables.NCHANL
      self.XDELH = [[0] * variables.NK for _ in range(variables.NK)]
      self.XH = [[0] * variables.NCHANL for _ in range(variables.NCHANL)]
      self.XHS = [[0] * variables.NK for _ in range(variables.NK)]
      self.XHST = [[0] * variables.NK for _ in range(variables.NK)]
      self.XM = [[0] * variables.NK for _ in range(variables.NK)]
      self.XM0 = [[0] * variables.NK for _ in range(variables.NK)]
      self.XMI = [[0] * variables.NK for _ in range(variables.NK)]
      self.XMLT = [[0] * variables.NK for _ in range(variables.NK)]
      self.XUST0 = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUST1 = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUSTD1 = [[0] * variables.NK for _ in range(variables.NK)]
      # matrix calculation for ft*stranspose*delu*wpr/area
      self.XY = [0.0] * variables.NCHANL
      # used in wprim routine
      self.XZ = [0.0] * variables.NK

      # used in AXIMOM
      self.YU1 = [[0] * variables.NK for _ in range(variables.NK)]

      ## introduction of void fraction and real quality of system
      self.VOID0 = [0] * variables.NCHANL
      self.VOID1 = [0] * variables.NCHANL
      self.QUALITY0 = [0] * variables.NCHANL
      self.QUALITY1 = [0] * variables.NCHANL

