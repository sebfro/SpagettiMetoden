# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = 'mergeA.nc'

# Geographical extent
lon0, lon1 =  10, 40
lat0, lat1 =  68, 78

# Maximum number of trajectories to plot
N0 = 5000

# Coast file
coast_file = 'kyst.nc'

# Topography file
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
#topo_file = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'

# Startdate
date0 = datetime.date(2008,  5, 27)

geoloc = [
  [2008,    8,       29,      71.87,   25.63,   83101],
  [2008,    9,       9,       65.05,   34.68,   83101],
  [2008,    9,       12,      70.74,   23.90,   83101],
  [2008,    10,      2,       72.92,   23.09,   83101],
  [2008,    10,      7,       72.92,   22.84,   83101],
  [2008,    10,      21,      74.08,   30.59,   83101]]


# -----------------------------------
# Read data
# -----------------------------------


# Get merged tracks
f = Dataset(merged_file)

#Ntrack = f.nTrack
Ntrack = len(f.dimensions['tracknr'])
N = min(N0, Ntrack)         # Number of tracks to plot
X = f.variables['lon'][:,:N]
Y = f.variables['lat'][:,:N]
 
#f.close()

print 'Number of tracks ', Ntrack
print 'Lon range = ', X.min(), X.max()
print 'Lat range = ', Y.min(), Y.max()



# Get coast data
f1 = Dataset(coast_file)
Xcoast = f1.variables['X'][:]
Ycoast = f1.variables['Y'][:]
S = f1.variables['S'][:]
f1.close()

# Get topography data
i0 = (lon0+180)*60
j0 = (lat0+90)*60
imax = (lon1-lon0)*60 + 1
jmax = (lat1-lat0)*60 + 1
f2 = Dataset(topo_file)
H = -f2.variables['z'][j0:j0+jmax, i0:i0+imax]
lon = f2.variables['lon'][i0:i0+imax]
lat = f2.variables['lat'][j0:j0+jmax]
f2.close()



# -----------------------
# Computations
# -----------------------

# Compute average trajectory, based on all tracks
Xm = np.mean(f.variables['lon'][:,:Ntrack], axis=1)
Ym = np.mean(f.variables['lat'][:,:Ntrack], axis=1)
#Xm = X.sum(axis=1) / N
#Ym = Y.sum(axis=1) / N

t = 100



# -----------------------
# Functions
# -----------------------

def snap_plot(t):

    # t is number of days
    plt.plot(X[t,:N], Y[t,:N], '.', color=(0.2, 0.2, 1.0))
    # Plot mean of plot ensemble
    #plt.plot(Xm[t], Ym[t], marker='d', color='blue', ms=12)


    #plt.title(str(date))

def plot_back():

    # Plot coast data
    for i in xrange(len(S)-1):
        plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], 
        facecolor=(0.2,0.8,0.2))

    # Plot bottom contours
    plt.contour(lon, lat, H, levels=(100,200,400,800), 
                colors='0.3', lw=0.5)



# ---------------------------------





plt.clf()

plot_back()
    


# Mean position
plt.scatter(Xm[t], Ym[t], s=100, color='yellow', zorder=8, marker='^', 
            linewidths=(1,), edgecolor='black')


snap_plot(t)

rad = np.pi / 180.0
X0 = (X[t,:Ntrack] - Xm[t])*np.cos(Ym[t]*rad)   # Relative position
X00 = (X[t,:Ntrack] - Xm[t])   # Relative position
Y0 =  Y[t,:Ntrack] - Ym[t]
    

M = np.cov(X0, Y0)
Mi = np.linalg.inv(M)
#M2 = np.matrix(M)
#M = M2


L, V = np.linalg.eig(M)

S = np.arange(361) * rad

#v = np.array([np.cos(S), np.sin(S)])

#r = 1/np.dot(np.dot(v.T,M),v)

#x = r*np.cos(S)
#y = r*np.sin(S)



x0 = L[0]*np.cos(S)
y0 = L[1]*np.sin(S)

x = V[0,0]*x0 + V[0,1]*y0
y = V[1,0]*x0 + V[1,1]*y0

x = x / np.cos(Ym[t]*rad)


plt.fill(Xm[t]+x, Ym[t]+y, color='yellow', 
         linewidth=2, edgecolor='black')

plt.plot([Xm[t]-X00.std(), Xm[t]+X00.std()],[Ym[t],Ym[t]], 'r', lw=3)
plt.plot([Xm[t], Xm[t]],[Ym[t]-Y0.std(),Ym[t]+Y0.std()], 'r', lw=3)

x0, y0 = Xm[t], Ym[t]

a = X00.std()
b = Y0.std()

#plt.plot([x0-a,x0+a,x0+a,x0-a,x0-a], [y0-b,y0-b,y0+b,y0+b,y0-b], 'g', lw=3)

Z = []
for v in np.linspace(0,360,361):
    v = v*rad
    c = np.cos(v)
    s = np.sin(v)
    z = X0*c + Y0*s
    #print z.mean()
    zstd = z.std()
    Z.append(zstd)
    #zstd = z.max()
    # Må strekke for plott
    xz = zstd*c/np.cos(Ym[t]*rad)
    #xz = zstd*np.cos(v)
    yz = zstd*s
#    plt.plot(x0+xz,y0+yz, 'g*')


    v = np.array([c, s])
    r = np.sqrt(np.dot(np.dot(v,M),v))
#    plt.plot(x0+r*c/np.cos(Ym[t]*rad), y0 + r*s, 'r*')
    # Dette gir det samme, 2 bulker    
    plt.plot(x0+r*c/np.cos(Ym[t]*rad), y0 + r*s, 'g*')

    r = 1./np.sqrt(np.dot(np.dot(v,Mi),v))
    plt.plot(x0+r*c/np.cos(Ym[t]*rad), y0 + r*s, 'r*')
    






# Limit plot area
plt.axis([lon0, lon1, lat0, lat1])
    



plt.show()
#plt.savefig("multi_validate.png", dpi=300)





