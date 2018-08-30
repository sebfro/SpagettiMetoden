# Removes non-used tracks

import numpy as np
from netCDF4 import Dataset

in_file = 'FWA.nc'
out_file = 'FWAA.nc'



f0 = Dataset(in_file)

time_lim = len(f0.variables['time'][:]) // 2   

life1 = f0.variables['life'][time_lim, :]
Nlife = life1.sum()

f1 = Dataset(out_file, 'w', format='NETCDF3_CLASSIC')




