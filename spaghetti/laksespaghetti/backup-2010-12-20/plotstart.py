import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

lon0, lon1 = 21.0, 25.0
lat0, lat1 = 69.5, 71.5

xpos = [22.3, 23.08,  23.5, 22.7]
ypos = [70.4, 70.204, 70.7, 70.9]


# Get coast data
nc = Dataset('kyst.nc')
Xcoast = nc.variables['X'][:]
Ycoast = nc.variables['Y'][:]
S = nc.variables['S'][:]
nc.close()


# ----------------------
# Plot
# ---------------------

# Plot coast data
for i in xrange(len(S)-1):
    plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], facecolor=(0.2,0.8,0.2))


plt.plot(xpos, ypos, 'o', markersize=10, color='red')


for i in range(4):
    plt.text(xpos[i]+0.02, ypos[i]+0.03, "ABCD"[i])


plt.axis([lon0, lon1, lat0, lat1])


plt.show()


