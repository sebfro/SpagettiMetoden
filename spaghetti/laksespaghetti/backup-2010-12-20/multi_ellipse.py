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
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'


# Startdate
date0 = datetime.date(2008,  5, 27)

geoloc = [
  [2008,    8,       29,      71.87,   25.63,   83101],
  [2008,    9,       1,       72.49,   22.14,   83101],
  [2008,    9,       12,      70.74,   23.90,   83101],
  [2008,    9,       19,      73.78,   22.12,   83101],
  [2008,    10,      2,       72.92,   23.09,   83101],
  [2008,    10,      7,       72.92,   22.84,   83101],
  [2008,    10,      21,      74.08,   30.59,   83101],
  [2008,    11,      19,      73.59,   30.50,   83101]
]


# -----------------------------------
# Read data
# -----------------------------------


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



# -----------------------
# Computations
# -----------------------

# Compute average trajectory, based on all tracks
Xm = np.mean(f.variables['lon'][:,:Ntrack], axis=1)
Ym = np.mean(f.variables['lat'][:,:Ntrack], axis=1)
#Xm = X.sum(axis=1) / N
#Ym = Y.sum(axis=1) / N


# -----------------------
# Functions
# -----------------------

def snap_plot(t):

    # t is number of days
    plt.plot(X[t,:N], Y[t,:N], '.', color=(0.0, 0.0, 1.0), alpha=0.01)
    #plt.plot(X[t,:N], Y[t,:N], '.', color=(0.0, 0.0, 1.0))
    # Plot mean of plot ensemble
    #plt.plot(Xm[t], Ym[t], marker='d', color='blue', ms=12)


    plt.title(str(date))

def plot_back():

    # Plot coast data
    for i in xrange(len(S)-1):
        plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], 
        facecolor=(0.2,0.8,0.2), lw=0.2)

    # Plot bottom contours
    plt.contour(lon, lat, H, levels=(100,200,400,800), 
                colors='0.3', lw=0.01)


def plot_ellipse(t):

    rad = np.pi / 180.0
    x0 = Xm[t]
    y0 = Ym[t]
    lonfac = np.cos(y0*rad)  

    # Scale so that x and y should be equivalent
    X0 = (X[t,:] - Xm[t]) * lonfac
    Y0 =  Y[t,:] - Ym[t]

    M = np.cov(X0, Y0)
    Mi = np.linalg.inv(M)


    A = np.arange(361) * rad
    C = np.cos(A)
    S = np.sin(A)

    r2 = np.zeros_like(A)
    for i in xrange(361):
        v = np.array([C[i],S[i]])
        r2[i] = np.dot(np.dot(v,Mi),v)

    r = 1.0/np.sqrt(r2)
    plt.fill(x0+r*C/lonfac, y0+r*S, color='blue',
             lw=1, edgecolor='black')
    
                       

# ---------------------------------

plt.figure(figsize=(6,10))

for n, loc in enumerate(geoloc):
    date = datetime.date(loc[0], loc[1], loc[2])

    t = (date-date0).days

    # Skru på for multi-ellipse
    #plt.clf()
    plt.subplot(4, 2, n+1)


    plot_back()
    
    # Plot GeoLoc
    plt.scatter(loc[4], loc[3], s=80, color='red', zorder=8,
                linewidths=(1,), edgecolor='black')


    # Mean position
    #plt.scatter(Xm[t], Ym[t], s=100, color='yellow', zorder=8, marker='^', 
    #            linewidths=(1,), edgecolor='black')


    # Standard deviation ellipse
    plot_ellipse(t)

    plt.title(str(date), fontsize=7)

    # Labelling in multi-setting
    if n < 6 : 
        plt.xticks([])
    else:
        plt.xticks(fontsize=6)
    if n % 2: 
        plt.yticks([])
    else:
        plt.yticks(fontsize=6)

    #snap_plot(t)



    # Limit plot area
    plt.axis([lon0, lon1, lat0, lat1])
    
    #plt.savefig("std_dev_ellipsis_no_%d.png" % (n+1), dpi=300)


#plt.show()
plt.savefig("multi_ellipse.png", dpi=300)





