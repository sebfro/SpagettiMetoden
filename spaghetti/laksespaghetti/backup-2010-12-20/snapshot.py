# -*- coding: utf-8 -*-

import datetime
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
N0 = 500

# Coast file
coast_file = 'kyst.nc'

# Topography file
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
#topo_file = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'


# Date 
date1 = datetime.date(2008, 11, 21)
# Startdate
date0 = datetime.date(2008,  5, 27)


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



# -----------------------
# Computations
# -----------------------

# Compute average trajectory
Xm = X.sum(axis=1) / N
Ym = Y.sum(axis=1) / N



# -----------------------
# Plot
# -----------------------

def snap_plot(t):

    # t is number of days
    plt.plot(X[t,:N], Y[t,:N], '.', color='blue')
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


ndays = (date1-date0).days

for t in range(ndays):

    date = date0 + datetime.timedelta(days=t)

    plt.clf()

    plot_back()
    snap_plot(t)

    # Limit plot area
    plt.axis([lon0, lon1, lat0, lat1])
    

    t = (date-date0).days
    plt.savefig('snapshot_%3.3d.png' % t, dpi=100)




