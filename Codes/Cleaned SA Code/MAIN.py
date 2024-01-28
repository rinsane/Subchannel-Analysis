from FUNCTIONS import sub_routines

dum = sub_routines()

NODE = [sub_routines() for _ in range(dum.NNODE)]

for i in range(dum.NNODE):

    if i == 0:
        for I in range(dum.NCHANL):
            NODE[i].F1[I] = NODE[i].F0[I]
            NODE[i].P0[I] = NODE[i].PIN
            print(NODE[i].P0[I])
        print("FGfg")

        for K in range(dum.NK):
            NODE[i].WIJ0[K] = NODE[i].WIJIN
            NODE[i].WIJ1[K] = NODE[i].WIJIN

        NODE[i].XD()
        NODE[i].XB()
        NODE[i].YMULT(
            NODE[i].XMLT, NODE[i].S, NODE[i].XM, dum.NCHANL, dum.NK, dum.NCHANL
        )

        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM[I, J] = (
                    NODE[i].DELX * dum.SLP * NODE[i].XM[I, J] / NODE[i].A[I]
                )

        for II in range(dum.NCHANL):
            for JJ in range(dum.NCHANL):
                if II == JJ:
                    NODE[i].XMI[II, JJ] = dum.THETA * NODE[i].XM[II, JJ] + 1
                else:
                    NODE[i].XMI[II, JJ] = dum.THETA * NODE[i].XM[II, JJ]

        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM0[I, J] = NODE[i].XMI[I, J] - NODE[i].XM[I, J]

        for I in range(dum.NCHANL):
            SUM = 0
            for J in range(dum.NCHANL):
                PM = NODE[i].XM0[I, J] * NODE[i].P0[J]
            SUM = SUM + PM
            NODE[i].PM0[I] = SUM
            NODE[i].PB[I] = NODE[i].B[I] + NODE[i].PM0[I]

        NODE[i].gauss(NODE[i].XMI, NODE[i].P1, NODE[i].PB, dum.NCHANL)
        NODE[i].DCROSS()

        for K in range(dum.NK):
            NODE[i].WIJ1[K] = -NODE[i].WIJ1[K]

        for I in range(dum.NCHANL):
            NODE[i].F11[I] = NODE[i].F1[I]
        NODE[i].MASFLO()

        for I in range(dum.NCHANL):
            NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])

        if NODE[i].ERROR[I] >= 0.01:  ## CHECK ALIGNMENT HERE
            NODE[i].AXIMOM()
            for K in range(dum.NK):
                NODE[i].W2[K] = NODE[i].WIJ1[K]
            NODE[i].DCROSS()
            for K in range(dum.NK):
                NODE[i].WIJ1[K] = (
                    dum.GAMA * NODE[i].WIJ1[K] + (1 - dum.GAMA) * NODE[i].WIJ0[K]
                )
            for I in range(dum.NCHANL):
                NODE[i].F11[I] = NODE[i].F1[I]
            NODE[i].MASFLO()
            for I in range(dum.NCHANL):
                if NODE[i].F1[I] >= 0:
                    NODE[i].ERR[I] = abs(
                        (NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I]
                    )
                else:
                    break
        else:
            break

        NODE[i].HM()

    else:
        NODE[i].XD()
        NODE[i].XB()
        NODE[i].YMULT(
            NODE[i].XMLT, NODE[i].S, NODE[i].XM, dum.NCHANL, dum.NK, dum.NCHANL
        )

        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM[I, J] = (
                    NODE[i].DELX * dum.SLP * NODE[i].XM[I, J] / NODE[i].A[I]
                )

        for II in range(dum.NCHANL):
            for JJ in range(dum.NCHANL):
                if II == JJ:
                    NODE[i].XMI[II, JJ] = dum.THETA * NODE[i].XM[II, JJ] + 1
                else:
                    NODE[i].XMI[II, JJ] = dum.THETA * NODE[i].XM[II, JJ]

        for I in range(dum.NCHANL):
            for J in range(dum.NCHANL):
                NODE[i].XM0[I, J] = NODE[i].XMI[I, J] - NODE[i].XM[I, J]

        for I in range(dum.NCHANL):
            SUM = 0
            for J in range(dum.NCHANL):
                PM = NODE[i].XM0[I, J] * NODE[i].P0[J]
                SUM = SUM + PM  ## CHECK THIS ALLIGNMENT
            NODE[i].PM0[I] = SUM
            NODE[i].PB[I] = NODE[i].B[I] = +NODE[i].PM0[I]
        
        NODE[i].gauss(NODE[i].XMI, NODE[i].P1, NODE[i].PB, dum.NCHANL)
        NODE[i].DCROSS()

        for K in range(dum.NK):
            NODE[i].WIJ1[K] = -NODE[i].WIJ1[K]

        for I in range(dum.NCHANL):
            NODE[i].F11[I] = NODE[i].F1[I]
        NODE[i].MASFLO()

        for I in range(dum.NCHANL):
            NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])

        if NODE[i].ERROR[I] >= 0.01:  ## CHECK ALIGNMENT HERE
            NODE[i].AXIMOM()
            for K in range(dum.NK):
                NODE[i].W2[K] = NODE[i].WIJ1[K]
            NODE[i].DCROSS()
            for K in range(dum.NK):
                NODE[i].WIJ1[K] = (
                    dum.GAMA * NODE[i].WIJ1[K] + (1 - dum.GAMA) * NODE[i].WIJ0[K]
                )
            for I in range(dum.NCHANL):
                NODE[i].F11[I] = NODE[i].F1[I]
            NODE[i].MASFLO()
            for I in range(dum.NCHANL):
                if NODE[i].F1[I] >= 0:
                    NODE[i].ERR[I] = abs(
                        (NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I]
                    )
                else:
                    break
        else:
            break

        NODE[i].HM()
