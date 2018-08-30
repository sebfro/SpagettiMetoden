# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file

#merged_file = 'merge_83100.nc'
#merged_file = 'mergeA.nc'
merged_file = 'merge_sausage.nc'

# Geographical extent
lon0, lon1 =  10, 40
lat0, lat1 =  68, 78

# Maximum number of trajectories to plot
N0 = 5000

# Coast file
coast_file = 'kyst.nc'

# Topography file
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# Geoloc-file 
geoloc_file = None
geoloc_file = "geoloc.dat"


def plot_ellipse(t):

    rad = np.pi / 180.0
    x0 = Xm[t]
    y0 = Ym[t]
    lonfac = np.cos(y0*rad)  

    # Scale so that x and y should be equivalent
    X0 = (X[t,:] - Xm[t]) * lonfac
    Y0 =  Y[t,:] - Ym[t]

    M = np.cov(X0, Y0)
    try:
        Mi = np.linalg.inv(M)
    except np.linalg.linalg.LinAlgError:
        return


    A = np.arange(361) * rad
    C = np.cos(A)
    S = np.sin(A)

    r2 = np.zeros_like(A)
    for i in xrange(361):
        v = np.array([C[i],S[i]])
        r2[i] = np.dot(np.dot(v,Mi),v)

    r = 1.0/np.sqrt(r2)
    plt.fill(x0+r*C/lonfac, y0+r*S, color='blue', lw=0, alpha=0.1)
    #plt.plot(x0+r*C/lonfac, y0+r*S, color='blue', lw=0.2, alpha=1.0)
    


# ----------------

# Get merged tracks
f = Dataset(merged_file)

#Ntrack = f.nTrack
Ntrack = len(f.dimensions['tracknr'])
N = min(N0, Ntrack)         # Number of tracks to plot
X = f.variables['lon'][:,:N]
Y = f.variables['lat'][:,:N]
 
#f.close()

print 'Number of tracks ', Ntrack
print 'Lon range = ', X.min(), X.max()
print 'Lat range = ', Y.min(), Y.max()



# Get coast data
f1 = Dataset(coast_file)
Xcoast = f1.variables['X'][:]
Ycoast = f1.variables['Y'][:]
S = f1.variables['S'][:]
f1.close()

# Get topography data
i0 = (lon0+180)*60
j0 = (lat0+90)*60
imax = (lon1-lon0)*60 + 1
jmax = (lat1-lat0)*60 + 1
f2 = Dataset(topo_file)
H = -f2.variables['z'][j0:j0+jmax, i0:i0+imax]
lon = f2.variables['lon'][i0:i0+imax]
lat = f2.variables['lat'][j0:j0+jmax]
f2.close()


# Get geolocation data

if geoloc_file:
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

# Compute average trajectory, based on all tracks
Xm = np.mean(f.variables['lon'][:,:Ntrack], axis=1)
Ym = np.mean(f.variables['lat'][:,:Ntrack], axis=1)
#Xm = X.sum(axis=1) / N
#Ym = Y.sum(axis=1) / N



plt.clf()

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))


# Plot merged tracks
#for i in xrange(N):
#    plt.plot(X[:,i], Y[:,i], color='blue', alpha=0.1)
#    plt.plot(X[:,i], Y[:,i], alpha=0.4)



for t in range(1, len(Xm)-1):
#for t in range(10, len(Xm)-1, 10):
    plot_ellipse(t)

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
if geoloc_file:
    plt.plot(Xgeo, Ygeo, '*', color=(1,1,0), markersize=15)


# Limit plot area
plt.axis([lon0, lon1, lat0, lat1])

# Display the plot
#plt.savefig('ellipse_track_83100_2.png', dpi=400)
#plt.savefig('ellipse_sausage.png', dpi=400)
plt.show()

