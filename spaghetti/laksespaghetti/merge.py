# --- coding: utf-8 ---

#from Numeric import *
#from Scientific.IO.NetCDF import
import numpy as np
from netCDF4 import Dataset

# �Pne input filer



f1 = Dataset('FW.nc')
f2 = Dataset('BW.nc')
fout = Dataset('merged.nc', 'w')




rad = np.pi/180.0


Ntraj = 10000


T = f1.variables['time'][:]

ttime = 182  # Total number of days

mday = 91

FWlife = f1.variables['life'][mday+1,:]
BWlife = f2.variables['life'][ttime-mday,:]

X1 = f1.variables['X'][mday,:]
Y1 = f1.variables['Y'][mday,:]

X2 = f2.variables['X'][ttime-mday-1,:]
Y2 = f2.variables['Y'][ttime-mday-1,:]




# Lag output fil

fout.createDimension('time', None)
fout.createDimension('fish', Ntraj)

fout.createVariable('time', 'd', ('time',))
fout.createVariable('X', 'f', ('time', 'fish'))
fout.createVariable('Y', 'f', ('time', 'fish'))
fout.createVariable('P', 'i', ('fish',))  # Indeks i f�rste fil
fout.createVariable('Q', 'i', ('fish',))  # indeks i andre fil


for t in T:
    it = int(t)
    fout.variables['time'][it] = it


# Hvor n�rt skal det v�re f�r match, pr�ver 1 km
# lag litt statistikk p� avstand fra 1 dag til neste


# Finn n�reste levende partikkelQ

n = -1
Q = np.zeros(Ntraj) - 1  # undef = -1
for p in range(Ntraj):
    if FWlife[p]:
        x, y = (X1[p], Y1[p])
        lonfac = np.cos(y*rad)
        D = lonfac*lonfac*(X2-x)*(X2-x) + (Y2-y)*(Y2-y)
        D = np.where(BWlife, D, 1.0E32)
        q = np.argmin(D)
        Q[p] = q
#        if sqrt(D[q])*1.852*60 < 20: # 699
        if np.sqrt(D[q])*1.852*60 < 100:
            n = n + 1
            print (n, p, q, np.sqrt(D[q])*1.852*60)

            # logikken ikke helt bra
            fout.variables['X'][:mday+1, n] = f1.variables['X'][:mday+1, p]
            X = f2.variables['X'][:,q]
            #print  X[mday::-1].shape
            #print fout.variables['X'][mday:, n].shape
            fout.variables['X'][mday:, n] = X[mday::-1]

            fout.variables['Y'][:mday+1, n] = f1.variables['Y'][:mday+1, p]
            Y = f2.variables['Y'][:,q]
            fout.variables['Y'][mday:, n] = Y[mday::-1]
            fout.variables['P'][n] = p
            fout.variables['Q'][n] = q
            
f1.close()
f2.close()

fout.nTrack = n
        

fout.close()        
        


            
            
