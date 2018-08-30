# -*- coding: utf-8 -*-

from datetime import datetime
import numpy as np
from netCDF4 import Dataset

def sample_sst(fid, lon, lat, dtime):

    # Spatial discretization
    nlon, nlat = 60, 20
    dlon, dlat = 1.0, 1.0
    lon0, lat0 = -10.0, 60.0

    # Temporal discretization
    ntimes = 53    # kan variere mellom år



    d0 = datetime(dtime.year, 1, 1, 0, 0, 0)
    jday = (dtime-d0).days 
    
    days = fid.variables['time'][:]

    # Find l1 s.t. days[l1-1] <= jday < days[l1]
    # Obs problemer ved start på pr
    l1 = np.sum(days-jday < 0) 
    r = (jday - days[l1-1])/7.0
    print "r = ", r

    # Find spatial 
    # x = 0 i midt av første gridcelle
    x = (lon-lon0-0.5*dlon)/dlon
    y = (lat-lat0-0.5*dlat)/dlat
    i = int(x)
    j = int(y)
    p = x - i
    q = y - j

    # read data
    sst = fid.variables['sst'][l1-1:l1+1, j:j+2, i:i+2]
    #print sst
   
    # Testing interpolation of lon/lat
    #for lx in [0,1]:
    #    for jx in [0,1]:
    #        for ix in [0,1]:
    #            #sst[lx,jx,ix] = lon0 + (i+ix+0.5)*dlon
    #            sst[lx,jx,ix] = lat0 + (j+jx+0.5)*dlat





    v0 = (1-p)*(1-q)*sst[0,0,0] + (1-p)*q*sst[0,1,0] +  \
          p*(1-q)*sst[0,0,1] + p*q*sst[0,1,1]
    
    v1 = (1-p)*(1-q)*sst[1,0,0] + (1-p)*q*sst[1,1,0] +  \
          p*(1-q)*sst[1,0,1] + p*q*sst[1,1,1]
    
    print v0, v1
    return (1-r)*v0 + r*v1



if __name__ == '__main__':

    f = Dataset('./input/oisst_2008.nc')

#    lon = 24.09
#    lat = 74.05
    lon =  10.2
    lat =  69.7
    dtime = datetime(2008,7,30,0,0,0)
    
    print sample_sst(f, lon, lat, dtime)


    
