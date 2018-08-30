# -*- coding: utf-8 -*-

"""Reproduce the standard output in the README file"""

import gzip
import struct
import numpy as np

date = "1993-08-04"

nlon = 360
nlat = 180

# Read land mask
tagls = np.fromfile('lstags.onedeg.dat', dtype='>f4')
tagls.shape = (nlat, nlon)

# Open the file, try uncompressed first, thereafter gzipped
fname = 'oisst.' + "".join(date.split('-'))
try: 
    f = open(fname, 'rb')
except IOError:
    fname = fname + '.gz'
    f = gzip.open(fname)

# Read header
# dummy values are fortran start and end of record markers
header = f.read(40)
dummy0, year0, mnd0, day0, year1, mnd1, day1, ndays, index, dummy1 = \
      struct.unpack('>10i4', header)

# Print header info

print "start date", "%4d-%2.2d-%2.2d" % (year0, mnd0, day0)
print "end date  ", "%4d-%2.2d-%2.2d" % (year1, mnd1, day1)
print "ndays = ", ndays
print "index = ", index

# Read data
nwords = 1 + nlon*nlat + 1
format1 = '>%df4' % nwords  # sst, err 
format2 = '%db' % nwords    # cice

sst  = np.array(struct.unpack(format1, f.read(4*nwords)))
err  = np.array(struct.unpack(format1, f.read(4*nwords)))
cice = np.array(struct.unpack(format2, f.read(nwords)))

# Get rid of fortran dummy values and reshape to 2D
sst  =  sst[1:-1].reshape((nlat,nlon))
err  =  err[1:-1].reshape((nlat,nlon))
cice = cice[1:-1].reshape((nlat,nlon))

# Choose a longitude
i = 180
xlon = i + 0.5

formatlist = ["lon = %5.1f", "lat = %5.1f", "sst = %5.1f",
              "nev = %5.3f", "ice = %3d", "tagls = %2.0f"]
format = "    ".join(formatlist)

# Choose a sequence of latitudes
for j in xrange(179, 148, -1):
    xlat = j - 89.5
    print format % (xlon, xlat, sst[j,i], err[j,i], cice[j,i], tagls[j,i])

