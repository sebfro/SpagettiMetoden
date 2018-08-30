# -*- coding: utf-8 -*-

#from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date


week = 30

#nlon, nlat = 60, 20
dlon, dlat = 1.0, 1.0
lon0, lat0 = -10.0, 60.0


f = Dataset('./input/oisst_2008.nc')
    

sst = f.variables['sst'][week,:,:]
tvar = f.variables['time']

dtime = num2date(tvar[week], tvar.units)

jmax, imax = sst.shape

lon = lon0 + (np.arange(imax) + 0.5) * dlon
lat = lat0 + (np.arange(jmax) + 0.5) * dlat



plt.contourf(lon, lat, sst)
plt.colorbar()

plt.title(str(dtime)[:10])

plt.grid(True)

plt.show()


    
