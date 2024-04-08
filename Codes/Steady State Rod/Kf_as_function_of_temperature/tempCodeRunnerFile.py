for i in range(solver.NT-2,0,-1):
        T_exp=(solver.Ai[i]*solver.T[i+1])+(solver.Bi[i])
        solver.T[i]=T_exp  
        
    solver.T[0]=solver.T[1]