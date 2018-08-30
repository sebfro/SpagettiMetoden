import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# Get coast data
nc = Dataset('kyst.nc')
Xcoast = nc.variables['X'][:]
Ycoast = nc.variables['Y'][:]
S = nc.variables['S'][:]
nc.close()

# Get topography data
imax, jmax = 2101, 481
H0 = - np.loadtxt('input/etopo2_codyssey.dat')
H = np.transpose(H0.reshape((imax, jmax)))
lon0, lon1, dlon = 0., 70., 1./30.
lat0, lat1, dlat = 65., 81., 1./30.
lon = np.arange(lon0, lon1+dlon, dlon)
lat = np.arange(lat0, lat1+dlat, dlat)



# ----------------------
# Plot
# ---------------------

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))


plt.contour(lon, lat, H, levels=(0,), colors='red')

plt.contour(lon+1./60, lat+1./60, H, levels=(0,), colors='blue')

plt.contour(lon-1./60, lat-1./60, H, levels=(0,), colors='green')



# Limit plot area
plt.axis((-0,30,66,72))


plt.show()
