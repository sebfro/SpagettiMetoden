# -*- encoding: utf-8 -*-

import os
from Numeric import *
from Scientific.IO.NetCDF import *

from vjuplot import *

f = NetCDFFile('AA235_notemp.nc')
#f = NetCDFFile('AA235_temp.nc')
#f = NetCDFFile('A235.nc')

# No temperature

N = 53    # temp
N = 242   # notemp

N = 5190
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

width = 800
height = 600

c = Canvas('a235.pdf', (width, height))

xoff = 50
yoff = 50
xsize = width - 2*xoff
ysize = height - 2*yoff


v = RectView(c, xoff, yoff, xsize, ysize, x0, y0, x1, y1)



c.setLineWidth(1.5)




c.setStrokeColor((0.5, 0.5, 0.5))
c.setLineWidth(0.1)

for i in xrange(Nplot):
    v.polyline(X[:,i], Y[:,i])



        

# Finn middelbane
Xm = sum(X, axis=1)/N
Ym = sum(Y, axis=1)/N

c.setLineWidth(2)
c.setStrokeColor('black')

v.polyline(Xm, Ym)
        

## c.setLineWidth(2)
## c.setStrokeColor('red')
## xa, ya = v.rmap(xstart, ystart)
## c.line(xa-5,ya-5,xa+5,ya+5)
## c.line(xa-5,ya+5,xa+5,ya-5)

## xa, ya = v.rmap(xstop, ystop)
## c.line(xa-5,ya-5,xa+5,ya+5)
## c.line(xa-5,ya+5,xa+5,ya-5)


# Kysten
nc = NetCDFFile('kyst.nc')
Xcoast = nc.variables['X'].getValue()
Ycoast = nc.variables['Y'].getValue()
S = nc.variables['S'].getValue()
nc.close()

#c.setFillColor((0.4, 0.8, 0.1))
c.setFillColor((0.8, 0.8, 0.8))
for i in xrange(len(S)-1):
    v.polygon(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]])


# Blank out land outside plot frame
c.setFillColor('white')
c.polygon([0.0, width, width, 0.0], [0.0, 0.0, yoff, yoff])
c.polygon([0.0, xoff, xoff, 0.0], [0.0, 0.0, height, height])
c.polygon([width-xoff, width, width, width-xoff],
          [0.0, 0.0, height, height])
c.polygon([0.0, width, width,0.0],
          [height-yoff,height-yoff,height,height])



# Kartramme
c.setStrokeColor('black')
c.setFillColor('black')
frame(v, x0, y0, x1, y1)




c.save()


os.system('gv a235.pdf')
