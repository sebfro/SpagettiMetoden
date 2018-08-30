# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = 'merged.nc'

# Geographical extent
lon0, lat0 = -10, 60
lon1, lat1 =  60, 80

# Maximum number of trajectories
N0 = 50

# Coast file
coast_file = 'kyst.nc'

# Topography file
#topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
topo_file = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# -----------------------------------
# Read data
# -----------------------------------


# Get merged tracks
f = Dataset(merged_file)

Ntrack = f.nTrack
N = min(N0, Ntrack)         # Number of tracks to plot
X = f.variables['X'][:,:N]
Y = f.variables['Y'][:,:N]
 
f.close()

print ('Number of tracks ', Ntrack)
print ('Lon range = ', X.min(), X.max())
print ('Lat range = ', Y.min(), Y.max())



# Get coast data
f = Dataset(coast_file)
Xcoast = f.variables['X'][:]
Ycoast = f.variables['Y'][:]
S = f.variables['S'][:]
f.close()

# Get topography data
i0 = (lon0+180)*60
j0 = (lat0+90)*60
imax = (lon1-lon0)*60 + 1
jmax = (lat1-lat0)*60 + 1
f = Dataset(topo_file)
H = -f.variables['z'][j0:j0+jmax, i0:i0+imax]
lon = f.variables['lon'][i0:i0+imax]
lat = f.variables['lat'][j0:j0+jmax]
f.close()

# -----------------------
# Computations
# -----------------------

# Compute average trajectory
Xm = X.sum(axis=1) / N
Ym = Y.sum(axis=1) / N

# -----------------------
# Plot
# -----------------------

#plt.clf()

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))

# Plot bottom contours
plt.contour(lon, lat, H, levels=(100,200,400,800), colors='red')

# Plot merged tracks
for i in xrange(N):
    plt.plot(X[:,i], Y[:,i], color='blue')

# Plot mean of plot ensemble
plt.plot(Xm, Ym, color='black', lw=2)
        
# Limit plot area
plt.axis([lon0, lon1, lat0, lat1])

# Display the plot
plt.show()
#plt.savefig('a.pdf')

