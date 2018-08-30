# -*- coding: utf-8 -*-

"""Sample the SST field"""

# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# 2009-10-22
# -----------------------------------

import datetime as dt
import numpy as np
from netCDF4 import Dataset

# ------------------
# User setting
# ------------------

lon, lat = 5.4, 70.2
year, month, day = 2008, 10, 22

lon0 = -10
lat0 = 60

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

# Find spatial indices to grid cells
i = int(np.floor(lon-lon0))
j = int(np.floor(lat-lat0))

# Read the data

print t, j, i
print days[t]

sst = f.variables['sst'][t,j,i]
err = f.variables['err'][t,j,i]
mask = f.variables['landmask'][j,i]
xlon = f.variables['lon'][i]
xlat = f.variables['lat'][j]
xtime = f.variables['time'][t]

f.close()

print "lon, lat = ", lon, lat
print "date = ", dt.date(2008,month,day)
print "sst = ", sst
print "err = ", err
print "mask = ", mask
print "lon = ", xlon
print "lat = ", xlat
print "week time = ", dt.date(2008,1,1) + dt.timedelta(days=int(xtime))



