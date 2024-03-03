import numpy as np
##MATRIX MULTIPLICATION [A(M,N)*B(N,L)=C(M,L)],MATRIX [B] INTEGE
def YMULT(A, B, C, MM, NN, LL):
    print(f"Dimensions of A: {np.array(A).shape}")
    print(f"Dimensions of B: {np.array(B).shape}")
    print(f"Dimensions of C: {np.array(C).shape}")

    for M in range(0,MM):
        for L in range(0,LL):
            sum_value = 0
            for N in range(0,NN):
                sum_value += A[M][N] * B[N][L]
            C[M][L] = sum_value

