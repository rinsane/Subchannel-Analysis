def gauss(AG, XG, YG, IG):
    XG1 = XG.copy()  # Initialize XG1 with the initial values of XG
    ITER = 1

    while True:
        for I in range(IG):
            AP = YG[I]
            for J in range(IG):
                if I == J:
                    continue
                else:
                    AP -= AG[I][J] * XG[J]

            XG[I] = AP / AG[I][I]

        ERR = [abs(XG[i] - XG1[i]) / abs(XG[i]) for i in range(IG)]
        ERRMAX = max(ERR)

        if ERRMAX <= 1e-08:
            break

        XG1 = XG.copy()
        ITER += 1

    #print(f'ITERATION={ITER}')
    print('XG=', XG)
