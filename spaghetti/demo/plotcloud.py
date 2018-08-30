import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

fname = "A235FW.nc"

tframe = 24

f = Dataset(fname)

X = f.variables['X'][tframe,:]
Y = f.variables['Y'][tframe,:]
life = f.variables['life'][tframe,:]

X = X[life==1]
Y = Y[life==1]

print len(X), len(Y)

plt.plot(X,Y,'.')
plt.show()
