import numpy as np


fname = 'terminateBW.dat'

f = open(fname)


A = np.loadtxt(fname)

S = A[:,0]

print S
