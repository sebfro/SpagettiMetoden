# -*-coding: utf-8 -*-

# Merge the different merge-files

import datetime
import numpy as np
from netCDF4 import Dataset


date0 = datetime.datetime(2008,05,27,12,00,00)

nfiles = 9

mfiles = ["merge_sausage%1d.nc" % (i+1) for i in range(nfiles)]

output_file = "merge_sausage.nc"

N = 100

#print mfiles

# pre-scan

total_time =  -1  # start with initial
start_times = []  # inital leg start at beginning
ntimes_list = []


# Prescan
for i in range(nfiles):
    f = Dataset(mfiles[i])
    ntimes  = len(f.dimensions['time'])
    ntracks = len(f.dimensions['tracknr'])
    ntimes_list.append(ntimes)
    print i, ntimes, ntracks
    if ntracks < 100:
        print "Must have at least 100 tracks"
        print "ntracks = ", ntracs, " for leg nr. ", i+1
        import sys
        sys.exit(1)
    f.close()

# Start points
S = [0]
S.append(ntimes_list[0])
for i in range(2,nfiles+1):
    S.append(S[i-1] + ntimes_list[i-1] - 1)

print S

total_time = S[-1]

  
#print total_time
#print start_times
#for i in xrange(nfiles):
#    print start_times[i], start_times[i+1], start_times[i+1]-start_times[i]
#    #print range(start_times[i], start_times[i+1])

# --------------------
# Create output file
# --------------------

fout = Dataset(output_file, 'w', format='NETCDF3_CLASSIC')

# Dimensions
fout.createDimension('time', total_time) 
fout.createDimension('tracknr', N)

v = fout.createVariable('time', 'd', ('time',))
v.long_name = 'time'
v.units = 'days since ' + str(date0)
v[:] = np.arange(total_time)

# Data variables

lon_var = fout.createVariable('lon', 'f', ('time', 'tracknr'))
lon_var.long_name = "longitude"
lon_var.units = "degrees_east"

lat_var = fout.createVariable('lat', 'f', ('time', 'tracknr'))
lat_var.long_name = "latitude"
lat_var.units = "degrees_north"

# Global attributes (not needed anymore)
# Virker ikke med NETCDF3_CLASSIC???
#fout.nTrack = N
fout.Conventions = 'CF-1.0'
fout.institution = 'Institute of Marine Research'
fout.source = "The spaghetti geolocation model by Bjørn Ådlandsvik, IMR"
fout.history = 'created %s by sausage_merge.py' 

# Merge the merge-files
delta = 0
for i in xrange(nfiles):
    f = Dataset(mfiles[i])
    print i
    print S[i],S[i+1],S[i+1]-S[i]
    print f.variables['lon'][:,:N].shape
    lon_var[S[i]:S[i+1],:N] = f.variables['lon'][delta:,:N]
    lat_var[S[i]:S[i+1],:N] = f.variables['lat'][delta:,:N]
    delta = 1
    f.close()




fout.close()



