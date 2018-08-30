# -*- coding: utf-8 -*-

"""Plot a snapshot of particles"""

# -----------------------------------
# plotcloud.py                      
#                                   
# Bjørn Ådlandsvik, <bjorn@imr.no>  
# Institute of Marine Research      
# 2009-11-01                        
# -----------------------------------

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ----------------------
# User settings
# ----------------------

# Particle file name
fname = "FW.nc"
#fname = "BW.nc"

# Time frame
tframe = 1

# Geographical extent
lon0, lat0 = -10, 60
lon1, lat1 =  60, 80


# ------------------------
# Read data
# ------------------------

# Particle data

f = Dataset(fname)

X = f.variables['X'][tframe,:]
Y = f.variables['Y'][tframe,:]
life = f.variables['life'][tframe,:]

X = X[life==1]
Y = Y[life==1]

f.close()


# Get coast data
nc = Dataset('kyst.nc')
Xcoast = nc.variables['X'][:]
Ycoast = nc.variables['Y'][:]
S = nc.variables['S'][:]
nc.close()

# Get topography data
i0 = (lon0+180)*60
j0 = (lat0+90)*60
imax = (lon1-lon0)*60 + 1
jmax = (lat1-lat0)*60 + 1
f = Dataset('/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd')
H = -f.variables['z'][j0:j0+jmax, i0:i0+imax]
lon = f.variables['lon'][i0:i0+imax]
lat = f.variables['lat'][j0:j0+jmax]
f.close()




# ----------------------
# Plot
# ---------------------

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))

# Plot bottom contours
plt.contour(lon, lat, H, levels=(100,200,400), colors='r')

# Plot cloud of particle tracks
plt.plot(X, Y, 'b.')

# Limit plot area
plt.axis((lon0, lon1, lat0, lat1))

plt.show()

