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
lon0, lon1 =  14, 32
lat0, lat1 =  70, 75

# Maximum number of trajectories to plot
N0 = 1000

# Coast file
coast_file = 'kyst.nc'

# Topography file
#topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# Optic geolocation file
geoloc_file = "geoloc.dat"
geoloc_number = 8          # Counting from 1


# Date 
#date = datetime.date(2008,10,21)
# Startdate
date0 = datetime.date(2008,5,27)

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

print "N = ", N

 
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
geodate = []
for line in fid:
    w = line.split()
    Xgeo.append(float(w[2]))
    Ygeo.append(float(w[1]))
    d, m, y = [int(s) for s in w[0].split('/')]
    geodate.append(datetime.date(y,m,d))
    



# -----------------------
# Computations
# -----------------------



# Compute average trajectory
Xm = X.sum(axis=1) / N
Ym = Y.sum(axis=1) / N



# -----------------------
# Plot
# -----------------------

def snap_plot(geoloc_number):

    # t is number of days
    t = (geodate[geoloc_number-1]-date0).days
    plt.plot(X[t,:N], Y[t,:N], '.', color='blue')
    # Plot mean of plot ensemble
    plt.plot(Xm[t], Ym[t], marker='d', color='blue', ms=12)

    # Plot geolocation
    plt.plot(Xgeo[geoloc_number-1], Ygeo[geoloc_number-1], color=(1.0,0.0,0.2),
         marker='o', markersize=12)

    plt.title('geoloc # %d, date %s' % 
              (geoloc_number, str(geodate[geoloc_number-1])))

def plot_back():

    # Plot coast data
    for i in xrange(len(S)-1):
        plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], 
        facecolor=(0.2,0.8,0.2))

    # Plot bottom contours
    plt.contour(lon, lat, H, levels=(100,200,400,800), 
                colors='0.7')





for geoloc_number in range(1,9):

    plt.clf()
    plot_back()
    snap_plot(geoloc_number)

    # Limit plot area
    plt.axis([lon0, lon1, lat0, lat1])

    plt.savefig('figure5_%s.png' % geoloc_number)
    


#plt.savefig('snapshots2.png', dpi=300)
#plt.show()


