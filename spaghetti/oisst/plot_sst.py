# -*- coding: utf-8 -*-

"""Plot SST field at given date"""

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# 2009-10-21
# -----------------------------------

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ------------------
# User setting
# ------------------

year, month, day = 2008, 5, 17

# ------------------
# Read the data
# ------------------

# Open the netCDF SST file

fname = 'oisst_%4d.nc' % year  # file name
f = Dataset(fname)

# Find the week index t, containing the date
# correct week is given by closest Wednesday
days = f.variables['time'][:]   # days in year
jday = (dt.date(year,month,day)-dt.date(year,1,1)).days # day in year
t = np.argmin(np.abs(days-jday))

# Read the data
sst = f.variables['sst'][t,:,:]
mask = f.variables['landmask'][:,:]
lon = f.variables['lon'][:]
lat = f.variables['lat'][:]

f.close()

# ------------------
# Modify the data
# ------------------

# Mask out land cells
sst = np.ma.masked_where(mask < 1, sst)

# Compute lon, lat of grid cell corners
lonp = np.arange(lon[0]-0.5, lon[-1]+1.5)
latp = np.arange(lat[0]-0.5, lat[-1]+1.5)

# ----------------
# Plotting
# ----------------

plt.pcolor(lonp, latp, sst)
#plt.contourf(lon, lat, sst)
plt.colorbar()

plt.show()



