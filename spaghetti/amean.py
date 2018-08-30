# -*- encoding: iso-latin-1 -*-
# TAr inn temperaturatlas og lager klimatologi

from Numeric import *
from Scientific.IO.NetCDF import *

f0 = NetCDFFile('atlas.nc')

imax = 129
jmax = 66
kmax = 101
lmax = 108
nyear = 108/4

UNDEF = -999.999

Count = zeros((4, kmax, jmax, imax), Int16)
Tmean = zeros((4, kmax, jmax, imax), Float32)
Tstd  = zeros((4, kmax, jmax, imax), Float32)

# Slice along i to reduce memory usage
for i in xrange(imax):
#for i in xrange(2):
    print "%5d" % i
    T0 = f0.variables['Temp'][:,:,:,i]
    for m in xrange(4):
        T1 = T0[m:lmax:4,:,:]  # all values from quarter m
        M = T1 > -2.0
        C  = sum(M, axis=0)
        ST = sum(T1*M, axis=0)
        STT = sum(M*T1*T1, axis=0) 
        eps = 1.0**(-32)
        MT = where(C > 2, ST/(C+eps), UNDEF) # mean
        TV = where(C > 3, STT/(C+eps) - MT*MT, UNDEF)
        A = TV > 0
        TS = where(A, sqrt(A*TV), UNDEF)

        Count[m,:,:,i] = C.astype(Int16)
        Tmean[m,:,:,i] = MT.astype(Float32)
        Tstd[m,:,:,i] = TS.astype(Float32)
        




# --------------------------------------------------

f1 = NetCDFFile('amean.nc', 'w')

f1.createDimension('X', imax)
f1.createDimension('Y', jmax)
f1.createDimension('Z', kmax)
f1.createDimension('T', 4)

print "definert dimensjoner"

v = f1.createVariable('X', Float32, ('X',))
v.units = 'degrees E'

v = f1.createVariable('Y', Float32, ('Y',))
v.units = 'degrees N'

v = f1.createVariable('Z', Float32, ('Z',))
v.units = 'meter'
v.positive = 'down'

v = f1.createVariable('T', Float32, ('T',))
v.units = 'days since 0000-01-01 00:00:00'

v = f1.createVariable('Temp', Float32, ('T', 'Z', 'Y', 'X'))
v.long_name = 'Temperature'
v.units = 'degrees C'
#v._FillValue = UNDEF  # Skjærer seg ???? (hvorfor)

v = f1.createVariable('count', Int16, ('T', 'Z', 'Y', 'X'))
v.long_name = 'number of defined values'

v = f1.createVariable('Tstd', Float32, ('T', 'Z', 'Y', 'X'))
v.long_name = 'Standard deviation of temperature'
v.units = 'degrees C'


print "definert variable"

# ------------------------------------------------

times = array([365.25/24, 365.25*7/24,
               365.25*13/24, 365.25*19/24], Float32)

f1.variables['X'][:] = f0.variables['X'][:]
f1.variables['Y'][:] = f0.variables['Y'][:]
f1.variables['Z'][:] = f0.variables['Z'][:]
f1.variables['T'][:] = times

f0.close()

f1.variables['count'].assignValue(Count)
f1.variables['Temp'].assignValue(Tmean)
f1.variables['Tstd'].assignValue(Tstd)
        
    
f1.close()





#for m in xrange(4):
#    C    = zeros((kmax, jmax, imax), 'l')  # Counter
#    T1   = zeros((kmax, jmax, imax), 'f')
#    for y  in xrange(nyear):
#        t = m + y*4
#        T0 = f0.variables['Temp'][t,:,:,:]
#        M = T0 > -2.0
#        C = C + M
#        T1 = where(M, T1+T0, T1)
#        # Ha med det som trengs for å beregne standardavvik underveis
#    Temp = where(C > 2, T1/C, UNDEF)
    

