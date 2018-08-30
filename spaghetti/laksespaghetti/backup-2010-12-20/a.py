# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = 'mergeA.nc'

# output file
out_file = "meanpath.dat"


# -----------------------------------
# Read data
# -----------------------------------


# Get merged tracks
f = Dataset(merged_file)

Ntrack = f.nTrack
X = f.variables['X'][:,:Ntrack]
Y = f.variables['Y'][:,:Ntrack]
 

#print 'Number of tracks ', Ntrack
#print 'Lon range = ', X.min(), X.max()
#print 'Lat range = ', Y.min(), Y.max()

P = f.variables['P'][:]
Q = f.variables['Q'][:]

f.close()

Q2 = Q[Q > 0]
P2 = P[P > 0]

print len(P2)
print len(Q2)

A = []
for q in np.unique(Q2):
    A.append(len(Q[Q==q]))


A.sort()

print A






#f2 = open(out_file, 'w')

#for t in xrange(len(X)):
#    f2.write('%3d %6.3f %6.3f\n' % (t, Xm[t], Ym[t]))
#
#f2.close()
    

