import math
import numpy as np
from inputs import variables

class sub_routines(variables):

    def AXIMOM(self):
        # Calls SKI before
        #print("STARTING OF AXIMOM")
        self.star()

        U1 = [self.F1[I] / (self.A[I] * self.RHO) for I in range(self.NCHANL)]
        XU1 = [
            [U1[I] if I == J else 0.0 for J in range(self.NCHANL)]
            for I in range(self.NCHANL)
        ]

        self.YU1 = self.YMULT(
            XU1, self.ST, self.YU1, self.NCHANL, self.NCHANL, self.NK
        )

        XXU1 = [[0.0] * self.NK for _ in range(self.NK)]
        XXU1 = self.XMULT(
            self.ST, self.XUST1, XXU1, self.NCHANL, self.NK, self.NK
        )

        Z1 = [0.0] * self.NK
        Z2 = [0.0] * self.NK

        for I in range(self.NCHANL):
            SUM1 = sum(self.YU1[I][K] * self.WIJ1[K] for K in range(self.NK))
            SUM2 = sum(XXU1[I][K] * self.WIJ1[K] for K in range(self.NK))

            Z1[I] = 2.0 * self.DELX * SUM1 / self.A[I]
            Z2[I] = self.DELX * SUM2 / self.A[I]

        for I in range(self.NCHANL):
            self.P1[I] = self.P0[I] + (self.DELTA * self.XA[I]) + Z1[I] - Z2[I]
            self.P1[I] = (self.DELTA * self.P1[I]) + ((1 - self.DELTA) * self.P0[I])

        '''for I, p in enumerate(self.P1):
            print(f"P1[{I}] = {p}")'''

        #print("END OF AXIMOM")

    def DCROSS(self):
        # Called Ski before DCROSS
        # fpr computation of diversion cross flow raTE AND AXIAL MASS FLOW F1
        #print("STARTING OF DCROSS")

        for K in range(self.NK):
            SP1 = self.USTAR0[K] * self.WIJ0[K] / self.DELX
            SP2 = self.SLP * (1 - self.THETA) * self.CIJ0[K] * self.WIJ0[K]
            SUM3 = 0
            SUM4 = 0

            for I in range(self.NCHANL):
                SP3 = self.S[K][I] * self.P1[I]
                SP4 = self.S[K][I] * self.P0[I]
                SUM3 += SP3
                SUM4 += SP4

            SP3 = self.SLP * self.THETA * SUM3
            SP4 = self.SLP * (1 - self.THETA) * SUM4

            self.WIJ1[K] = (SP1 - SP2 + SP3 + SP4) / self.D[K]                         

        #print("END OF DCROSS")

    def gauss(self):
        #Calculating the MJ
        self.XM = self.YMULT(
            self.XMLT, self.S, self.XM, self.NCHANL, self.NK,self.NCHANL
        )

        for I in range(self.NCHANL):
            for J in range(self.NCHANL):
               self.XM[I][J] = (
                    self.DELX * self.SLP * self.XM[I][J] / (self.A[I] *self.D[I] )
                )

        for II in range(self.NCHANL):
            for JJ in range(self.NCHANL):
                if II == JJ:
                    self.XMI[II][JJ] = self.THETA * self.XM[II][JJ] + 1
                else:
                    self.XMI[II][JJ] = self.THETA * self.XM[II][JJ]

        for I in range(self.NCHANL):
            for J in range(self.NCHANL):
                self.XM0[I][J] = self.XMI[I][J] - self.XM[I][J]

        for I in range(self.NCHANL):
            SUM = 0
            for J in range(self.NCHANL):
                PM = self.XM0[I][J] * self.P0[J]
                SUM += PM
            self.PM0[I] = SUM
            self.PB[I] = self.B[I] + self.PM0[I]


        # gauss(AG = XMI, XG = P1, YG = PB, IG = NCHANL)
        #print("calling GAUSS")
        XG1 = [0.12e8] * self.NCHANL  # Initialize self.P11 with the initial values of self.P1
        XG = [0] * self.NCHANL

        #print("P1: ")
        #print(self.P1)
        
        while True:
            for I in range(self.NCHANL):
                AP = self.PB[I]
                for J in range(self.NCHANL):
                    if I == J:
                        continue
                    else:
                        AP = AP - self.XMI[I][J] * self.P1[J]
 
                XG[I] = AP / self.XMI[I][I]
                
            self.ERR = [abs(XG[i] - XG1[i]) / abs(XG[i]) for i in range(self.NCHANL)]
            ERRMAX = max(self.ERR)

            if ERRMAX <= 1e-08:
                break
            XG1 = XG.copy()
        self.P1 = XG.copy()
        #print("GAUSS over")

    def HM(self):
        # SKI called before that
        #print("STARTING OF HMW")
        for K in range(self.NK):
            I = self.IC[K] - 1
            J = self.JC[K] - 1
            self.HSTAR[K] = 0.5 * (self.H0[I] + self.H0[J])
            self.DELH[K] = self.H0[I] - self.H0[J]

        for II in range(self.NK):
            for JJ in range(self.NK):
                if II == JJ:
                    self.XDELH[II][JJ] = self.DELH[II]
                    self.XHS[II][JJ] = self.HSTAR[II]
                else:
                    self.XDELH[II][JJ] = 0
                    self.XHS[II][JJ] = 0

        for II in range(self.NCHANL):
            for JJ in range(self.NCHANL):
                if II == JJ:
                    self.XH[II][JJ] = self.H0[I]
                else:
                    self.XH[II][JJ] = 0

        self.S5 = self.XMULT(
            self.ST, self.XHS, self.S5, self.NCHANL, self.NK, self.NK
        )
        self.SD = self.XMULT(
            self.ST, self.XDELH, self.SD, self.NCHANL, self.NK, self.NK
        )
        self.XHST = self.YMULT(
            self.XH, self.ST, self.XHST, self.NCHANL, self.NCHANL, self.NK
        )

        for I in range(self.NCHANL):
            self.Q[I] = self.HF[I] * self.HPERI[I]
            self.C1[I] = self.Q[I] * self.DELX / self.F1[I]
            
        for II in range(self.NCHANL):
            SUM3 = 0
            SUM4 = 0
            for KK in range(self.NK):
                S3 = self.XHST[II][KK] * self.WIJ1[KK]
                SS3 = self.S5[II][KK] * self.WIJ1[KK]
                S3 = S3 - SS3
                S4 = self.SD[II][KK] * self.WPR[KK]
                SUM3 += S3
                SUM4 += S4
                self.C2[II] = SUM4 * self.DELX / self.F1[II]
                self.C3[II] = SUM3 * self.DELX / self.F1[II]

        for I in range(self.NCHANL):
            self.H1[I] = self.H0[I] + self.C1[I] - self.C2[I] + self.C3[I]

        #print("END OF HMW")

    def MASFLO(self):
        # Called ski before using it
        #print("STARTING OF MASFLO")
        for I in range(self.NCHANL):
            SUM = 0
            for K in range(self.NK):
                SW = self.ST[I][K] * self.WIJ1[K]
                SUM += SW
            self.F1[I] = self.F0[I] - (self.DELX * SUM)

        #print("FTOTAL: ", sum(self.F1))
        #print("END OF MASFLO")

    def SKI(self):
        # Works on input variables only, called once before anything uses input variables
        #print("STARTING OF SKI")
        #Calculating the connecting matrix
        for K in range(self.NK):
            for I in range(self.NCHANL):
                self.S[K][I] = 0
                if I == self.IC[K]-1:
                    self.S[K][I] = 1
                if I == self.JC[K]-1:
                    self.S[K][I] = -1
        # Computation of transpose matrix ST
        for I in range(self.NCHANL):
            for K in range(self.NK):
                self.ST[I][K] = self.S[K][I]
        
        #print("END OF SKI")

    def star(self):
        # called ski before using
        #print("STARTING OF STAR")

        for K in range(self.NK):
            I = self.IC[K] - 1
            J = self.JC[K] - 1
            if self.WIJ1[J] < 0:
                self.USTAR1[K] = self.F1[J] / (self.A[J] * self.RHO)
            elif self.WIJ1[K] == 0:
                self.USTAR1[K] = 0.5 * (
                    (self.F1[I] / (self.A[I] * self.RHO))
                    + (self.F1[J] / (self.A[J] * self.RHO))
                )
            else:
                self.USTAR1[K] = self.F1[I] / (self.A[I] * self.RHO)

        for K in range(self.NK):
            I = self.IC[K] - 1
            J = self.JC[K] - 1
            if self.WIJ0[J] < 0:
                self.USTAR0[K] = self.F0[J] / (self.A[J] * self.RHO)
            elif self.WIJ0[K] == 0:
                self.USTAR0[K] = 0.5 * (
                    (self.F0[I] / (self.A[I] * self.RHO))
                    + (self.F0[J] / (self.A[J] * self.RHO))
                )
            else:
                self.USTAR0[K] = self.F0[I] / (self.A[I] * self.RHO)

        for KK in range(self.NK):
            for II in range(self.NK):
                if KK == II:
                    self.XUST0[KK][II] = self.USTAR0[KK]
                    self.XUST1[KK][II] = self.USTAR1[KK]
                else:
                    self.XUST0[KK][II] = 0.0
                    self.XUST1[KK][II] = 0.0
        #print("END OF STAR")

    def wprim(self):
        # called ski before using
        # computation of turbulent cross flow W ij'
        # F1 = [0] * 20 ### check it
        # wpr= beta*gap*avg mass flux

        #print("STARTING OF WPRIM")
        AVRE = [0] * self.NK
        BETA = [0] * self.NK
        AHDIA = [0] * self.NK
        
        for K in range(self.NK):
            I = self.IC[K] - 1
            J = self.JC[K] - 1

            AHDIA[K] = 0.5 * (
                self.HDIA[I] + self.HDIA[J]
            )  ### avg hdia of adjacent subchannel
            AVRE[K] = (
                0.5
                * ((self.F1[I] / self.A[I]) + (self.F1[J] / self.A[J]))
                * AHDIA[K]
                / self.VISC
            )  ## avg re of adjacent subchannel
            BETA[K] = (
                0.0018
                * (abs(AVRE[K]) ** (-0.1))
                * (AHDIA[K] / self.GAP[K])
                * ((self.GAP[K] / self.RDIA) ** (1 - 0.4))
            )  ### correlation for beta taken from finding


            self.WPR[K] = (
                BETA[K] * self.GAP[K] * AVRE[K] * self.VISC / AHDIA[K]
            )  ## wpr is turbulent cross flow
            
            self.XZ[K] = (self.F1[I]/self.A[I] - self.F1[J]/self.A[J]) * self.WPR[K] / self.RHO

        for I in range(self.NCHANL):
            SUM = 0.0
            for K in range(self.NK):
                SUM += self.ST[I][K] * self.XZ[K]
            self.XY[I] = self.FT * SUM / self.A[I]

        #print("END OF WPRIM")

    def xxa(self):
        # Calls Ski before
        # COMMON block variables

        # Variables from COMMON/A2/
        FACF = np.zeros(self.NCHANL)

        # Variables from COMMON/A5/
        # S = [[0.0] * NK for _ in range(NCHANL)]
        # ST = [[0.0] * NCHANL for _ in range(NK)]

        #print("STARTING OF XXA")

        # Call to WPRIM (assuming it's another subroutine)
        self.wprim()

        for I in range(self.NCHANL):
            self.RE[I] = (
                self.F0[I] * self.HDIA[I] / (self.A[I] * self.VISC)
            )  ## calculation of reynold no
            FACF[I] = 0.186 * (abs(self.RE[I]) ** (-0.2))  ## calculation of friction factor
            X4 = self.XY[I]
            X1 = (self.F0[I] / self.A[I]) ** 2  ## ratio of mass flow rate to area
            X2 = (
                0.5 * FACF[I] / (self.HDIA[I] * self.RHO)
            )  ## pressure drop  due to friction
            X3 = (
                self.GC * self.RHO * math.cos(self.ALPHA * math.pi / 180)
            )  ## role of gravity
            self.XA[I] = -(X1 * X2) - X3 - X4

        #print("END OF XXA")

    def XD(self):
        #Calculating D matrix
        # print(self.DELX)
        #print("STARTING OF XD")
        self.star()

        for K in range(self.NK):
            I = self.IC[K] - 1
            J = self.JC[K] - 1
            self.CIJ0[K] = (
                0.5 * self.FACK * abs(self.WIJ0[K]) / (self.RHO * self.GAP[K] ** 2)
            )
            self.CIJ1[K] = (
                0.5 * self.FACK * abs(self.WIJ1[K]) / (self.RHO * self.GAP[K] ** 2)
            )
            self.D[K] = (self.USTAR1[K] / self.DELX) + (
                self.SLP * self.THETA * self.CIJ1[K]
            )
            self.USTD1[K] = self.USTAR1[K] / self.D[K]  ### OTHER MATRIX
            
        for KK in range(self.NK):
            for II in range(self.NK):
                if KK == II:
                    self.XUSTD1[KK][II] = self.USTD1[KK]
                else:
                    self.XUSTD1[KK][II] = 0.0
        
        #print("END OF XD")

    def XB(self):
        #calculating B matrix
        # Calls ski before
        #print("STARTING OF XB")
        SAVE    = np.zeros(self.NK)
        self.XMLT = self.XMULT(
            self.ST, self.XUSTD1, self.XMLT, self.NCHANL, self.NK, self.NK
        )

        for K in range(self.NK):
            SAVE1 = self.USTAR0[K] * self.WIJ0[K] / self.DELX
            SAVE2 = self.SLP * (1 - self.THETA) * self.CIJ0[K] * self.WIJ0[K]
            SAVE[K] = SAVE1 - SAVE2

        for I in range(self.NCHANL):
            SUM = 0.0
            for K in range(self.NK):
                SUM += self.XMLT[I][K] * SAVE[K]
            self.SS[I] = SUM

        self.xxa()

        for I in range(self.NCHANL):
            self.B1[I] = self.DELX * self.SS[I] / self.A[I]
            self.B2[I] = (
                2.0
                * (self.F1[I] - self.F0[I])
                * (self.F1[I] / (self.A[I] * self.RHO))
                / self.A[I]
            )
            self.B[I] = self.DELX * self.XA[I] - self.B1[I] - self.B2[I]

        #print("END OF XB")
    
    #Simple Matrix multiplication
    def XMULT(self, A, B, C, MM, NN, LL):
        #print("Calling XMULT: ")
        #print(f"Dimensions of A: {np.array(A).shape}")
        #print(f"Dimensions of B: {np.array(B).shape}")
        #print(f"Dimensions of C: {np.array(C).shape}")

        for M in range(0, MM):
            for L in range(0, LL):
                sum_value = 0
                for N in range(0, NN):
                    sum_value += A[M][N] * B[N][L]
                C[M][L] = sum_value
        #print("Ending XMULT...")
        return C
   
    #Simple Matrix multiplication
    def YMULT(self, A, B, C, MM, NN, LL):
        #print("Calling YMULT: ")
        #print(f"Dimensions of A: {np.array(A).shape}")
        #print(f"Dimensions of B: {np.array(B).shape}")
        #print(f"Dimensions of C: {np.array(C).shape}")

        for M in range(0, MM):
            for L in range(0, LL):
                sum_value = 0
                for N in range(0, NN):
                    sum_value += A[M][N] * B[N][L]
                C[M][L] = sum_value
        #print("Ending YMULT...")
        return C