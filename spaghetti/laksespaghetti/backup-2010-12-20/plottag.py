# -*- coding: utf-8 -*-

# Plot input time series of depth and temperature
# from a pop-up tag

# B.Å. 2010-02-23


import numpy as np
import matplotlib.pyplot as plt


#tag_file = './input/tag83101.dat'
tag_file = './input/tag83100.dat'
#tag_file = './input/a.dat'

f = open(tag_file)


temp = []
depth = []

for line in f:
    w = line.split()
    d = float(w[3])
    if d > 4000. : d = np.NaN
    depth.append(d)

    x = float(w[2])
    if x > 4000.: x = np.NaN
    temp.append(x)


T = np.arange(len(temp))
T = T / 24.0
Tmax = T.max()


plt.subplot(2,1,1)

plt.plot(T, depth)
# Reverse the depth axis
#y0, y1 = plt.ylim()
#plt.ylim(y1,y0)
# Alternative, one call
plt.gca().invert_yaxis()
plt.ylabel('Depth [m]')
plt.xlim(0, Tmax)
plt.grid(True)

plt.subplot(2,1,2)

plt.plot(T, temp)
plt.ylabel(u'Sea surface temperature [deg C]')
plt.xlim(0, Tmax)
plt.xlabel('Time [days]')
plt.grid(True)

plt.show()



    
    
