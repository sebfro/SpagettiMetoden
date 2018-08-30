# -*- coding: utf-8 -*-

"""Map a year of SST on a subdomain to a netCDF file"""


# -----------------------------------
# Bjørn Ådlandsvik <bjorn@imr.no>
# Institute of Marine Research
# 2009-10-21
# -----------------------------------

import datetime
import gzip
import struct
import numpy as np
from netCDF4 import Dataset

# -------------------
# User settings
# -------------------

# First date
date0 = datetime.date(2008,1,2)    # First date of year

# Subdomain
lon0, lon1 = -10, 50
lat0, lat1 = 60, 80

# ---------------------

i0, i1 = lon0, lon1
j0, j1 = 90 + lat0, 90 + lat1

# -----------------------
# Land mask
# -----------------------

# Read land mask, and restrict to subdomain
tagls = np.fromfile('lstags.onedeg.dat', dtype='>f4')
tagls.shape = (180, 360)
mask = np.concatenate((tagls[j0:j1, i0:], tagls[j0:j1, :i1]), axis=1)

# ----------------------------
# Create output netCDF file
# ----------------------------

ncname = 'oisst_' + str(date0.year) + '.nc'
nc = Dataset(ncname, 'w', format='NETCDF3_CLASSIC')
# Global attributes
nc.history = "Created by sst2nc.py"
nc.source = "NOAA Optimum Interpolation (OI) Sea Surface Temperature (SST) V2"
nc.source_url = "http://www.esrl.noaa.gov/psd/data/gridded/data.noaa.oisst.v2.html"
nc.Conventions = "CF-1.0"
# Dimensions
nc.createDimension('lon', lon1-lon0)
nc.createDimension('lat', lat1-lat0)
nc.createDimension('time', None)
# Coordinate variables
v = nc.createVariable('lon', 'f', ('lon',))
v.long_name = "Longitude"
v.units = "degree_east"
v = nc.createVariable('lat', 'f', ('lat',))
v.long_name = "Latitude"
v.units = "degree_north"
v = nc.createVariable('time', 'int', ('time',))
v.long_name = 'time'
v.units = 'days since %4d-01-01' % date0.year
# Data variables
v = nc.createVariable('landmask', 'f', ('lat', 'lon'))
v.long_name = "land mask"
v = nc.createVariable('sst', 'f', ('time', 'lat', 'lon'))
v.long_name = "Sea Surface Temperature"
v.unit = "degree_Celcius"
v = nc.createVariable('err', 'f', ('time', 'lat', 'lon'))
v.long_name = "Normalized Error Variance"
# Variables not depending on time
nc.variables['lon'][:] = np.arange(i0,i1) + 0.5
nc.variables['lat'][:] = np.arange(j0,j1) - 89.5
nc.variables['landmask'][:,:] = mask

# --------------
# Time loop
# --------------

date = date0
t = 0
while date.year == date0.year:

    # Open the file, try uncompressed first, thereafter gzipped
    fname = 'oisst.' + "".join(str(date).split('-'))
    try: 
        f = open(fname, 'rb')
    except IOError:
        fname = fname + '.gz'
        f = gzip.open(fname)
    print fname

    # --- Read header ---
    # dummy values are fortran start and end of record markers
    header = f.read(40)
    dummy0, year0, mnd0, day0, year1, mnd1, day1, ndays, index, dummy1 = \
            struct.unpack('>10i4', header)

    # --- Read data ---
    nwords = 360*180 + 2
    format1 = '>%df4' % nwords  # sst, err 

    sst  = np.array(struct.unpack(format1, f.read(4*nwords)))
    err  = np.array(struct.unpack(format1, f.read(4*nwords)))

    # Get rid of fortran dummy values and reshape to 2D
    sst  =  sst[1:-1].reshape((180, 360))
    err  =  err[1:-1].reshape((180, 360))

    # Extract the subdomain
    sst = np.concatenate((sst[j0:j1, i0:], sst[j0:j1, :i1]), axis=1)
    err = np.concatenate((err[j0:j1, i0:], err[j0:j1, :i1]), axis=1)

    # --- Write output ---
    nc.variables['time'][t] = (date-datetime.date(date0.year,1,1)).days
    nc.variables['sst'][t,:,:] = sst
    nc.variables['err'][t,:,:] = err
    
    # Update the date
    date = date + datetime.timedelta(days=7)  # Next week
    t = t + 1                                 # Next record

nc.close()










