# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = ['mergeA.nc', 'mergeA2.nc', 'mergeA3.nc',
               'mergeB.nc', 'mergeC.nc', 'mergeD.nc']

label = ['A', 'A2', 'A3', 'B', 'C', 'D']


# Geographical extent
#lon0, lat0 =   5, 65
#lon1, lat1 =  45, 78

# Geographical extent
lon0, lon1 =  14, 32
lat0, lat1 =  70, 75

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



# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))


# Plot bottom contours
plt.contour(lon, lat, H, levels=(100,200,400,800), colors='0.7')

h = []

for c in range(6):

    

    # Get merged tracks
    f = Dataset(merged_file[c])

    #Ntrack = f.nTrack
    Ntrack = len(f.dimensions['tracknr'])

    X = f.variables['lon'][:,:]
    Y = f.variables['lat'][:,:]
 
    f.close()

    print 'Number of tracks ', Ntrack


    # -----------------------
    # Computations
    # -----------------------
    
    # Compute average trajectory
    Xm = X.sum(axis=1) / Ntrack
    Ym = Y.sum(axis=1) / Ntrack



    # Plot mean of plot ensemble
    l, = plt.plot(Xm, Ym, lw=2)
    h.append(l)
    plt.plot(Xm[::10], Ym[::10], 'bo', markersize=4, 
      markerfacecolor='white')




    #plt.text(lon0+1, lat0+0.3,  label[c])


# Limit plot area
plt.axis([lon0, lon1, lat0, lat1])


plt.legend(h, label)


plt.savefig('plotsens2.png', dpi=300)
#plt.show()

