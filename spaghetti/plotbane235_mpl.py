# -*- encoding: utf-8 -*-

from pylab import *
from Scientific.IO.NetCDF import *


#f = NetCDFFile('AA235_notemp.nc')
f = NetCDFFile('AA235_temp.nc')
#f = NetCDFFile('A235.nc')

# No temperature

N = 53    # temp
N = 242   # notemp

#N = 5184
#N = 1113

Nplot = 50

#N = f.nTrack[0]+1
#Nplot = min(100,N)
X = f.variables['X'][:,:N]
Y = f.variables['Y'][:,:N]


print N
#print X.shape

f.close()


print 'X-range = ', min(ravel(X)), max(ravel(X))
print 'Y-range = ', min(ravel(Y)), max(ravel(Y))

# Start position
# 106
xstart = 12.22
ystart = 67.32
xstop  = 23.22
ystop  = 71.09

x0 = 14.0
x1 = 30.0
y0 = 68.0
y1 = 77.0





#npaths = min(100,N)
#npaths = 10

clf()

for i in xrange(Nplot):
    plot(X[:,i], Y[:,i],'b')



# Finn middelbane
Xm = sum(X, axis=1)/N
Ym = sum(Y, axis=1)/N


plot(Xm, Ym, color='k')
        


# Kysten
nc = NetCDFFile('kyst.nc')
Xcoast = nc.variables['X'].getValue()
Ycoast = nc.variables['Y'].getValue()
S = nc.variables['S'].getValue()
nc.close()

#c.setFillColor((0.4, 0.8, 0.1))
for i in xrange(len(S)-1):
    fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.8,0.8,0.8))


axis([10,33,69, 75])

show()
savefig('a.pdf')

