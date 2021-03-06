#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-


# Extract a subgrid from etopo2 and put onto a GMT grd file
# May work on a subslice on etopo2
#
import Numeric
from Scientific.IO.NetCDF import *
import gmt
import os

# justerbare ting
#etopo_file = "etopo2_frode.nc"
etopo_file = "/backup/bjorn/data/barentstopo2.nc"
lon0, lon1 = 6, 70
lat0, lat1 = 68, 81
#lon0, lon1 = 4, 12
#lat0, lat1 = 55, 60
#angle = 60  # azimuth for light
debug = 1

def read_etopo2(fname, lon0, lon1, lat0, lat1):

    # algoritme:
    # �pne fil, finne indekser i0, i1
    # s.a lon[i0] <= lon0 < lon[i0+1] < .. < lon[i1-1] < lon1 <= lon[i1]
    # feilmelding dersom slikt ikke finnes.
    # h�ndterer ikke rund 180 deg

    # Read the etopo NetCDF file
    f = NetCDFFile(fname)
    x = f.variables['topo_lon'][:]
    y = f.variables['topo_lat'][:]

    # etopo2, 1/30 degree
    i0 = int(Numeric.floor((lon0-x[0])*30))
    i1 = int(Numeric.ceil( (lon1-x[0])*30))
    j0 = int(Numeric.floor((lat0-y[0])*30))
    j1 = int(Numeric.ceil( (lat1-y[0])*30))

    h = f.variables['topo'][j0:j1+1,i0:i1+1]

    f.close()

    return h

# Read topography from etopo2
h = read_etopo2(etopo_file, lon0, lon1, lat0, lat1)

# Settings for GMT ploting
grdfile  = "e.grd"
#cptfile  = "e.cpt"
#gradfile = "e_i.grd"
#psfile   = "a.ps"

#proj    = "JL%d/60/55/70/16c" % (0.5*(lon0+lon1),)
#proj    = "JM16c"
#bord    = 'B10g10/5g5.:"Etopo2":WSen'
#bord    = 'B2g2/1g1.:"Etopo2":WSen'
#dlevel  = 100
#dlevel  = 25
#hmin    = dlevel * (min(h.flat) // dlevel)


# Make a GMT grid file
gmt.grdwrite(grdfile, h,
             ("m", "topography", 1.0, 0.0, 0),
             (lon0, lon1, "Longitude in degrees"),
             (lat0, lat1, "Latitude in degrees"),
             "etopo2 topography")

# Interpolate to the Atlas-grid
outgrid = 'atlastopo.grd'
reg = '-R6/70/68/81'

gmtcommand = "grdsample -V %s -G%s -I0.5/0.2 %s" % (grdfile, outgrid, reg)
print gmtcommand
os.system(gmtcommand)

# Make NetCDF-file of the new grid

gr = NetCDFFile(outgrid)

# Get array dimension
nx , ny = gr.variables['dimension'][:]
# Read array
Z = gr.variables['z'][:]
# Make 2D and flip
Z = Numeric.reshape(Z, (ny, nx))
Z = Z[::-1,:]
gr.close()

# ------------------------

print "nx, ny = ", nx, ny

nc = NetCDFFile("atlas_bunn.nc", 'w')

nc.title = "Topography of the atlas domain"
nc.history = "Derived from etopo2 by GMT grdsample"

nc.createDimension('lon', nx)
nc.createDimension('lat', ny)

v = nc.createVariable('lon', 'f', ('lon',))
v.units = "degrees east"
v.long_name = "longitude"
londata = lon0 + 0.5*Numeric.arange(nx+1)
londata = londata.astype('f')
v.assignValue(londata)

v = nc.createVariable('lat', 'f', ('lat',))
v.units = "degrees north"
v.long_name = "latitude"
latdata = lat0 + 0.2*Numeric.arange(ny+1)
latdata = latdata.astype('f')
v.assignValue(latdata)

v = nc.createVariable('H', 'f', ('lat','lon'))
v.long_name = "topography"
v.units = "meter"
v.assignValue(Z)

nc.close()






