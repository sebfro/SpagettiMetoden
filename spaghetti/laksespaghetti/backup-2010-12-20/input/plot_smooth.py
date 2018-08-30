# -*- coding: utf-8 -*-

# Plot input time series of depth and temperature
# from a pop-up tag

# B.Å. 2010-02-23

from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


# Original hourly data
#tag_file1 = 'tag83101.dat'
#tag_file2 = 'tag83101s.dat'
tag_file1 = 'tag83100.dat'
tag_file2 = 'tag83100s.dat'

jan1  = datetime(2008,1,1,0,0,0)
date0 = datetime(2008,05,25,13,0,0)
td = date0-jan1
toff = td.days + td.seconds / 86400.0

# start of  months
mstarts = [datetime(2008, m, 1, 0, 0, 0) for m in range(5,13)]
# approx middle of months
#mmid = [datetime(2008, m, 15, 0, 0, 0) for m in range(5,12)]
numstarts = [(d-jan1).days for d in mstarts]

# Add blanks before month string, to obtain an offset
mnames = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', '']
mnames = [17*" " + m for m in mnames]

    

f1 = open(tag_file1)


temp = []
depth = []

for line in f1:
    w = line.split()
    x = float(w[2])
    if x > 4000.: x = np.NaN
    temp.append(x)

    y = float(w[-1])
    if y > 4000.: y = np.NaN
    depth.append(y)
    



# smoothed

f2 = open(tag_file2)


btemp = []

for line in f2:
    w = line.split()
    x = float(w[2])
    btemp.append(x)

btemp = np.array(btemp)

T = np.arange(len(temp))
T = T / 24.0
Tmax = T.max()

T = T + toff

#plt.figure(figsize=(8,4))

plt.subplot(2,1,1)

plt.ylabel(u'Temperature (\u00B0C)')

plt.plot(T,  temp, lw=1.0, label='hourly data')
plt.plot(T, btemp, color='red', lw=2.0, label='moving average')

#plt.plot(T, btemp+1.2, 'r', lw=0.5)
#plt.plot(T, btemp-1.2, 'r', lw=0.5)

plt.xlim(numstarts[0], numstarts[-1])

plt.xticks(numstarts, [])

plt.grid(True)


#plt.legend(loc='best')
plt.legend(bbox_to_anchor=(0.6,0.4))

# -----------------

plt.subplot(2,1,2)

plt.plot(T, depth, lw=1, color='blue')

plt.ylim(500, 0)

plt.ylabel('Depth (m)')


plt.xticks(numstarts, mnames)


plt.xlim(numstarts[0], numstarts[-1])

plt.grid(True)

plt.savefig('tag83100_smooth.png', dpi=400)
plt.show()




    
    
