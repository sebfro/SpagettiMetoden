# -*- coding: utf-8 -*-

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
 
f.close()

print 'Number of tracks ', Ntrack
print 'Lon range = ', X.min(), X.max()
print 'Lat range = ', Y.min(), Y.max()


# -----------------------
# Computations
# -----------------------

# Compute average trajectory
Xm = X.sum(axis=1) / Ntrack
Ym = Y.sum(axis=1) / Ntrack

# -----------------------
# Output
# -----------------------


f2 = open(out_file, 'w')

for t in xrange(len(X)):
    f2.write('%3d %6.3f %6.3f\n' % (t, Xm[t], Ym[t]))

f2.close()
    

