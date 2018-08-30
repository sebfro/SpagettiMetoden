import numpy as np


fname = 'terminateBW.dat'

f = open(fname)


A = np.loadtxt(fname)

S = A[:,0]

S0 = np.unique(S)

L = []
for s in S0:
    L.append(len(S[S==s]))


M = zip(L, S0)

M.sort()

print M
