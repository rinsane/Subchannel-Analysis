from inputs import*
print(' SKI')

    # Check if the length of IC and JC is NK
if len(IC) != NK or len(JC) != NK:
    print("Error: Length of IC or JC is not equal to NK.")
    
   

    # Computation of S matrix
for K in range(NK):
    if 1 <= IC[K] <= NCHANL and 1 <= JC[K] <= NCHANL:
        IK = IC[K] - 1
        JK = JC[K] - 1
        S[K][IK] = 1
        S[K][JK] = -1
    else:
        print(f"Error: IC[K] or JC[K] out of bounds at K = {K + 1}.")
            

for K in range(NK):
    print(' '.join(map(str, S[K])))

print('TRANSPOSE OF MATRIX')

    # Computation of transpose matrix ST
for I in range(NCHANL):
    for K in range(NK):
        ST[I][K] = S[K][I]
        print(ST[I][K])
for I in range(NCHANL):
        print(' '.join(map(str, ST[I])))

# Call the subroutine
