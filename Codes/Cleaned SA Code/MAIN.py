from FUNCTIONS import sub_routines


def main():
    
    NODE = [sub_routines() for _ in range(sub_routines().NNODE)]

    for i in range(NODE[0].NNODE):

        if i == 0:
            for I in range(NODE[i].NCHANL):
                NODE[i].F1[I] = NODE[i].F0[I]
                NODE[i].P0[I] = NODE[i].PIN
                print(NODE[i].P0[I])
            print("FGfg")

            for K in range(NODE[i].NK):
                NODE[i].WIJ0[K] = NODE[i].WIJIN
                NODE[i].WIJ1[K] = NODE[i].WIJIN

            NODE[i].XD()
            NODE[i].XB()
            NODE[i].YMULT(
                NODE[i].XMLT, NODE[i].S, NODE[i].XM, NODE[i].NCHANL, NODE[i].NK, NODE[i].NCHANL
            )

            for I in range(NODE[i].NCHANL):
                for J in range(NODE[i].NCHANL):
                    NODE[i].XM[I, J] = (
                        NODE[i].DELX * NODE[i].SLP * NODE[i].XM[I, J] / NODE[i].A[I]
                    )

            for II in range(NODE[i].NCHANL):
                for JJ in range(NODE[i].NCHANL):
                    if II == JJ:
                        NODE[i].XMI[II, JJ] = NODE[i].THETA * NODE[i].XM[II, JJ] + 1
                    else:
                        NODE[i].XMI[II, JJ] = NODE[i].THETA * NODE[i].XM[II, JJ]

            for I in range(NODE[i].NCHANL):
                for J in range(NODE[i].NCHANL):
                    NODE[i].XM0[I, J] = NODE[i].XMI[I, J] - NODE[i].XM[I, J]

            for I in range(NODE[i].NCHANL):
                SUM = 0
                for J in range(NODE[i].NCHANL):
                    PM = NODE[i].XM0[I, J] * NODE[i].P0[J]
                SUM = SUM + PM
                NODE[i].PM0[I] = SUM
                NODE[i].PB[I] = NODE[i].B[I] + NODE[i].PM0[I]

            NODE[i].gauss(NODE[i].XMI, NODE[i].P1, NODE[i].PB, NODE[i].NCHANL)
            NODE[i].DCROSS()

            for K in range(NODE[i].NK):
                NODE[i].WIJ1[K] = - NODE[i].WIJ1[K]

            for I in range(NODE[i].NCHANL):
                NODE[i].F11[I] = NODE[i].F1[I]
            NODE[i].MASFLO()

            for I in range(NODE[i].NCHANL):
                NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])

            if NODE[i].ERROR[I] >= 0.01:  ## CHECK ALIGNMENT HERE
                NODE[i].AXIMOM()
                for K in range(NODE[i].NK):
                    NODE[i].W2[K] = NODE[i].WIJ1[K]
                NODE[i].DCROSS()
                for K in range(NODE[i].NK):
                    NODE[i].WIJ1[K] = (
                        NODE[i].GAMA * NODE[i].WIJ1[K] + (1 - NODE[i].GAMA) * NODE[i].WIJ0[K]
                    )
                for I in range(NODE[i].NCHANL):
                    NODE[i].F11[I] = NODE[i].F1[I]
                NODE[i].MASFLO()
                for I in range(NODE[i].NCHANL):
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
                NODE[i].XMLT, NODE[i].S, NODE[i].XM, NODE[i].NCHANL, NODE[i].NK, NODE[i].NCHANL
            )

            for I in range(NODE[i].NCHANL):
                for J in range(NODE[i].NCHANL):
                    NODE[i].XM[I, J] = (
                        NODE[i].DELX * NODE[i].SLP * NODE[i].XM[I, J] / NODE[i].A[I]
                    )

            for II in range(NODE[i].NCHANL):
                for JJ in range(NODE[i].NCHANL):
                    if II == JJ:
                        NODE[i].XMI[II, JJ] = NODE[i].THETA * NODE[i].XM[II, JJ] + 1
                    else:
                        NODE[i].XMI[II, JJ] = NODE[i].THETA * NODE[i].XM[II, JJ]

            for I in range(NODE[i].NCHANL):
                for J in range(NODE[i].NCHANL):
                    NODE[i].XM0[I, J] = NODE[i].XMI[I, J] - NODE[i].XM[I, J]

            for I in range(NODE[i].NCHANL):
                SUM = 0
                for J in range(NODE[i].NCHANL):
                    PM = NODE[i].XM0[I, J] * NODE[i].P0[J]
                    SUM = SUM + PM  ## CHECK THIS ALLIGNMENT
                NODE[i].PM0[I] = SUM
                NODE[i].PB[I] = NODE[i].B[I] = +NODE[i].PM0[I]
            
            NODE[i].gauss(NODE[i].XMI, NODE[i].P1, NODE[i].PB, NODE[i].NCHANL)
            NODE[i].DCROSS()

            for K in range(NODE[i].NK):
                NODE[i].WIJ1[K] = -NODE[i].WIJ1[K]

            for I in range(NODE[i].NCHANL):
                NODE[i].F11[I] = NODE[i].F1[I]
            NODE[i].MASFLO()

            for I in range(NODE[i].NCHANL):
                NODE[i].ERROR[I] = abs((NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I])

            if NODE[i].ERROR[I] >= 0.01:  ## CHECK ALIGNMENT HERE
                NODE[i].AXIMOM()
                for K in range(NODE[i].NK):
                    NODE[i].W2[K] = NODE[i].WIJ1[K]
                NODE[i].DCROSS()
                for K in range(NODE[i].NK):
                    NODE[i].WIJ1[K] = (
                        NODE[i].GAMA * NODE[i].WIJ1[K] + (1 - NODE[i].GAMA) * NODE[i].WIJ0[K]
                    )
                for I in range(NODE[i].NCHANL):
                    NODE[i].F11[I] = NODE[i].F1[I]
                NODE[i].MASFLO()
                for I in range(NODE[i].NCHANL):
                    if NODE[i].F1[I] >= 0:
                        NODE[i].ERR[I] = abs(
                            (NODE[i].F11[I] - NODE[i].F1[I]) / NODE[i].F1[I]
                        )
                    else:
                        break
            else:
                break

            NODE[i].HM()


if __name__ == '__main__':
    main()