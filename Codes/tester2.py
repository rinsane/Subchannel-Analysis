import math
import sys
sys.set_int_max_str_digits(100000)
def generator(string, k):
    n = len(string)
    res = []

    def gen(curr, idx):
        if len(curr) == k:
            res.append(curr)
            return

        for i in range(idx, n):
            gen(curr + string[i], i + 1)

    gen("", 0)
    return res

s = "123456"
has = {}

for i in range(1, 6 + 1):
    for j in generator(s, i):
        has[j] = 0

print(has)

fac = [0, 1]

for i in range(2, 5001):
    fac.append(fac[i-2] * i)
print(fac)
print(len(fac))