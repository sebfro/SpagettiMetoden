# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = 'mergeA.nc'

# Geographical extent
lon0, lon1 =  10, 40
lat0, lat1 =  68, 78

# Maximum number of trajectories to plot
N0 = 5000

# Coast file
coast_file = 'kyst.nc'

# Topography file
#topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
topo_file = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# Startdate
date0 = datetime.date(2008,  5, 27)

geoloc = [
  [2008,    8,       29,      71.87,   25.63,   83101],
  [2008,    9,       9,       65.05,   34.68,   83101],
  [2008,    9,       12,      70.74,   23.90,   83101],
  [2008,    10,      2,       72.92,   23.09,   83101],
  [2008,    10,      7,       72.92,   22.84,   83101],
  [2008,    10,      21,      74.08,   30.59,   83101]]


# -----------------------------------
# Read data
# -----------------------------------


# Get merged tracks
f = Dataset(merged_file)

Ntrack = f.nTrack
N = min(N0, Ntrack)         # Number of tracks to plot
X = f.variables['X'][:,:N]
Y = f.variables['Y'][:,:N]
 
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



# -----------------------
# Computations
# -----------------------

# Compute average trajectory, based on all tracks
Xm = np.mean(f.variables['X'][:,:Ntrack], axis=1)
Ym = np.mean(f.variables['Y'][:,:Ntrack], axis=1)
#Xm = X.sum(axis=1) / N
#Ym = Y.sum(axis=1) / N


# -----------------------
# Functions
# -----------------------

def snap_plot(t):

    # t is number of days
    plt.plot(X[t,:N], Y[t,:N], '.', color=(0.2, 0.2, 1.0))
    # Plot mean of plot ensemble
    #plt.plot(Xm[t], Ym[t], marker='d', color='blue', ms=12)


    plt.title(str(date))

def plot_back():

    # Plot coast data
    for i in xrange(len(S)-1):
        plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], 
        facecolor=(0.2,0.8,0.2))

    # Plot bottom contours
    plt.contour(lon, lat, H, levels=(100,200,400,800), 
                colors='0.3', lw=0.5)



# ---------------------------------

plt.figure(figsize=(6,8))

for n, loc in enumerate(geoloc):
    date = datetime.date(loc[0], loc[1], loc[2])

    t = (date-date0).days


    plt.subplot(3, 2, n+1)


    plot_back()
    
    # Plot GeoLoc
    plt.scatter(loc[4], loc[3], s=100, color='red', zorder=8,
                linewidths=(1,), edgecolor='black')


    # Mean position
    plt.scatter(Xm[t], Ym[t], s=100, color='yellow', zorder=8, marker='^', 
                linewidths=(1,), edgecolor='black')


    snap_plot(t)

    



    # Limit plot area
    plt.axis([lon0, lon1, lat0, lat1])
    



plt.show()
#plt.savefig("multi_validate.png", dpi=300)





