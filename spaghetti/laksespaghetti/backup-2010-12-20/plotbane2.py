# -*- coding: utf-8 -*-

# Plot tracks from a spaghetti model run
# Adapted to improved output format


import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
#merged_file = 'mergeA.nc'
merged_file = 'merge_29-08.nc'

# Geographical extent
#lon0, lat0 =   5, 65
#lon1, lat1 =  45, 78
lon0, lon1 =  10, 40
lat0, lat1 =  68, 76

# Maximum number of trajectories to plot
N0 = 200

# Coast file
coast_file = 'kyst.nc'

# Topography file
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
#topo_file = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# Optic geolocation file
geoloc_file = "geoloc.dat"


# -----------------------------------
# Read data
# -----------------------------------


# Get merged tracks
f = Dataset(merged_file)

#Ntrack = f.nTrack
Ntrack = len(f.dimensions['tracknr'])
N = min(N0, Ntrack)         # Number of tracks to plot
X = f.variables['lon'][:,:Ntrack]
Y = f.variables['lat'][:,:Ntrack]
 
f.close()

print 'Number of tracks ', Ntrack
print 'Lon range = ', X.min(), X.max()
print 'Lat range = ', Y.min(), Y.max()



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

# Get geolocation data

fid = open(geoloc_file)
Xgeo = []
Ygeo = []
for line in fid:
    w = line.split()
    Xgeo.append(float(w[2]))
    Ygeo.append(float(w[1]))



# -----------------------
# Computations
# -----------------------

# Compute average trajectory
Xm = X.sum(axis=1) / Ntrack
Ym = Y.sum(axis=1) / Ntrack

# -----------------------
# Plot
# -----------------------

#plt.clf()

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))


# Plot merged tracks
for i in xrange(N):
    plt.plot(X[:,i], Y[:,i], color='blue', alpha=0.1)
#    plt.plot(X[:,i], Y[:,i], alpha=0.4)

# Plot mean of plot ensemble
plt.plot(Xm, Ym, color='red', lw=2)
plt.plot(Xm[::10], Ym[::10], 'bo', markersize=4, markerfacecolor='white')

# Plot start stop
#plt.plot([X[0,0],X[-1,0]], [Y[0,0], Y[-1,0]], 'xb', 
#          markersize=4)

# Plot bottom contours
plt.contour(lon, lat, H, levels=(100,200,400,800), colors='0.7')


# Plot geolocation
#plt.plot(Xgeo, Ygeo, color=(0,1,1), lw=2)
#plt.plot(Xgeo, Ygeo, 'o', color=(0,1,1))


# Limit plot area
plt.axis([lon0, lon1, lat0, lat1])

# Display the plot
#plt.savefig('a.pdf')
#plt.savefig('mergeB.png', dpi=400)
plt.savefig('mergeA.png', dpi=400)
#plt.show()

