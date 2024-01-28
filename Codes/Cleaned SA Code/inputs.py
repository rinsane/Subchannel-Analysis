import numpy as np

class variables:

   ALPHA   = 90 # (ANGLE )
   AXLN    = 5.9436
   DELTA   = 0.5
   FACK    = 0.5
   FT      = 0.1 # turbulent factor used to compensate imperfect analogy bw turbulent transport of enthalpy and momentum
   GAMA    = 0.1
   GC      = 9.81 # g
   NCHANL  = 14 # no of subchannel
   NK      = 19 # no of connections
   NNODE   = 97
   RDIA    = 0.01308  
   RHO     = 817.4  
   SLP     = 0.5                                
   THETA   = 0.5 # IMPLICIT FAV
   VISC    = 0.000011

   def __init__(self):

      self.A       = [.000014451,.000014451,.000043225,.000028903,.000043225,.000043225,.000038516000,.000048387,.000038516,.000043225,.000035806,.000071612,.000071612,.000035806]
      
      self.B       = np.zeros(variables.NCHANL)
      self.B1      = np.zeros(variables.NCHANL)
      self.B2      = np.zeros(variables.NCHANL)
      
      self.C1      = np.zeros(variables.NCHANL)
      self.C2      = np.zeros(variables.NCHANL)
      self.C3      = np.zeros(variables.NCHANL)
      self.CIJ0    = [0] * variables.NK
      self.CIJ1    = [0] * variables.NK
      
      self.D       = np.zeros(variables.NK)
      self.DELH    = np.zeros(variables.NK)
      self.DELX    = variables.AXLN/(variables.NNODE-1)
      self.DELX    = variables.AXLN/(variables.NNODE-1)
      
      self.ERR     = np.zeros(variables.NK)
      self.ERROR   = np.zeros(variables.NK)
      
      self.F0      = [.090576301,.090576301,.331301059,.1810780788,.331301059,.331301059,.27866318100,.39238281,.278663181,.331301059,.250849063,.501698126,.501698126,.25084906] 
      self.F1      = [0] * 14  
      self.F11     = np.zeros(variables.NK)
      
      self.GAP     = [.0018034,.0009,.0009,.0018034,.0018034,.0009,.0018034,.0009,.0018034,.004140000,.00414,.0018034,.000991,.0019558,.0019558,.000991,.00194,.00194,.00194]  
      
      self.H0      = [1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7,1100.7000,1100.7,1100.7,1100.7]
      self.H1      = np.zeros(variables.NK)
      self.HDIA    = [.0056277,.0056277,.0084154,.005627,.0084154,.0084154,.0074985,.0094202,.0074485,.0084154,.0070309,.0070309,.0070309,.0070309] 
      self.HF      = [607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59,607.59000,607.59,607.59,607.59]
      self.HPERI   = [.010272,.010272,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020546,.020371,.040742,.040742,.020371]
      self.HSTAR   = np.zeros(variables.NK)
      
      self.IC      = [1, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 9, 6, 7, 9, 10, 11, 12, 13] # representation of interconnections of different subchannels
      self.JC      = [2, 3, 5, 4, 5, 6, 8, 10, 7, 8, 9, 10, 11, 12, 13, 14, 12, 13, 14]
            
      self.P0      = np.zeros(variables.NK)
      self.P1      = np.zeros(variables.NK)
      self.P11     = np.zeros(variables.NK)
      self.PB      = np.zeros(variables.NK)
      self.PIN     = 12262500
      self.PM0     = np.zeros(variables.NK)
      
      self.Q       = np.zeros(variables.NCHANL)
      
      self.RE      = [0] * 20 
      
      self.S       = np.zeros((variables.NK, variables.NK))
      self.S5      = np.zeros((variables.NK, variables.NK))
      self.SAVE    = np.zeros(variables.NK)
      self.SD      = np.zeros((variables.NK, variables.NK))
      self.SS      = np.zeros(variables.NCHANL)
      self.ST      = [[0.0] * 20 for _ in range(20)]  
      
      
      self.USTAR0  = [0.0] * variables.NK
      self.USTAR1  = [0.0] * variables.NK
      self.USTD1   = [0] * variables.NK
      
      self.W2      = np.zeros(variables.NK)
      self.WIJ0    = [0] * variables.NK
      self.WIJ1    = [0] * variables.NK
      self.WIJIN   = 0.0
      self.WPR     = np.zeros(variables.NK)
      
      self.X       = 0
      self.XA      = np.zeros(variables.NCHANL)
      self.XDELH   = np.zeros((variables.NK, variables.NK))
      self.XH      = np.zeros((variables.NCHANL, variables.NCHANL))
      self.XHS     = np.zeros((variables.NK, variables.NK))
      self.XHST    = np.zeros((variables.NK, variables.NK))
      self.XM      = np.zeros((variables.NK, variables.NK))
      self.XM0     = np.zeros((variables.NK, variables.NK))
      self.XMI     = np.zeros((variables.NK, variables.NK))
      self.XMLT    = np.zeros((variables.NK, variables.NK))
      self.XUST0   = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUST1   = [[0.0] * variables.NK for _ in range(variables.NK)]
      self.XUSTD1  = np.zeros((variables.NK, variables.NK), dtype=np.float64)
      self.XY      = [0.0] * variables.NCHANL # matrix calculation for ft*stranspose*delu*wpr/area
      self.XZ      = [0.0] * variables.NK
      
      self.YU1     = np.zeros((variables.NK, variables.NK))

'''
if X==0:
    for I in range(variables.NCHANL):
       F1[I]=F0[I] ##############   WHY THIS BC IS NOT UPDATING
       P0[I]=PIN
    
    for K in range(variables.NK):
       WIJ0[K]=WIJIN
       WIJ1[K]=WIJIN
'''