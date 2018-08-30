# -*- coding: utf-8 -*-

# Versjon for 83100


import datetime
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------

# Merged netCDF-file
merged_file = 'merge_83100.nc'


# Geographical extent
lon0, lon1 =  10, 50
lat0, lat1 =  67, 78

# Maximum number of trajectories to plot
N0 = 5000

# Coast file
coast_file = 'kyst.nc'

# Topography file
topo_file = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'


# Startdate
date0 = datetime.date(2008,  5, 22)


geof = open('geoloc83100.dat')

geoloc = []
for line in geof:
    w = line.split()
    if not w: break
    d,m,y = [int(i) for i in w[0].split('/')]
    lon = float(w[1])
    lat = float(w[2])
    geoloc.append([y,m,d,lon,lat])

    





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

#print Xm


# -----------------------
# Functions
# -----------------------

def snap_plot(t):

    # t is number of days
    plt.plot(X[t,:N], Y[t,:N], '.', color=(0.0, 0.0, 1.0), alpha=0.01)
    #plt.plot(X[t,:N], Y[t,:N], '.', color=(0.0, 0.0, 1.0))
    # Plot mean of plot ensemble
    #plt.plot(Xm[t], Ym[t], marker='d', color='blue', ms=12)


    plt.title(str(date))

def plot_back():

    # Plot coast data
    for i in xrange(len(S)-1):
        plt.fill(Xcoast[S[i]:S[i+1]], Ycoast[S[i]:S[i+1]], 
        facecolor=(0.2,0.8,0.2))

    # Plot bottom contours
    plt.contour(lon, lat, H, levels=(100,200,400,800), 
                colors='0.3', lw=0.2)


def plot_ellipse(t):

    rad = np.pi / 180.0
    x0 = Xm[t]
    y0 = Ym[t]
    lonfac = np.cos(y0*rad)  

    # Scale so that x and y should be equivalent
    X0 = (X[t,:] - Xm[t]) * lonfac
    Y0 =  Y[t,:] - Ym[t]

    M = np.cov(X0, Y0)
    Mi = np.linalg.inv(M)


    A = np.arange(361) * rad
    C = np.cos(A)
    S = np.sin(A)

    r2 = np.zeros_like(A)
    for i in xrange(361):
        v = np.array([C[i],S[i]])
        r2[i] = np.dot(np.dot(v,Mi),v)

    r = 1.0/np.sqrt(r2)
    plt.fill(x0+r*C/lonfac, y0+r*S, color='blue',
             lw=0.4, edgecolor='black')
    
                       
        

#    v = np.array([C, S])
#
#    q = np.tensordot(v,M,(0,1))
#    r = np.tensordot(v,q,(1,0))

    #x0 = L[0]*np.cos(S)
    #y0 = L[1]*np.sin(S)

    #x = V[0,0]*x0 + V[0,1]*y0
    #y = V[1,0]*x0 + V[1,1]*y0

    # rescale x to the plot
    #x = x / np.cos(Ym[t]*rad)

    #z = np.cos(S)*X0 + np.sin(S)*Y0
    #z1 = 




#    plt.fill(Xm[t]+x, Ym[t]+y, color='yellow', 
#             linewidth=2, edgecolor='black')


# ---------------------------------

plt.figure(figsize=(6,8))

for n, loc in enumerate(geoloc):
    date = datetime.date(loc[0], loc[1], loc[2])

    print n, date

    t = (date-date0).days

    # Skru på for multi-ellipse
    #plt.clf()
    plt.subplot(6, 4, n+1)


    plot_back()
    
    # Plot GeoLoc
    plt.scatter(loc[4], loc[3], s=30, color='red', zorder=8,
                linewidths=(0.5,), edgecolor='black')


    # Mean position
    #plt.scatter(Xm[t], Ym[t], s=100, color='yellow', zorder=8, marker='^', 
    #            linewidths=(1,), edgecolor='black')


    # Standard deviation ellipse
    #print ' --- ', t
    plot_ellipse(t)

    plt.title(str(date) + (' (%d)' % (t,)), fontsize=6)

    # Labelling in multi-setting
    if n < 20: plt.xticks([])
    if n >= 20: plt.xticks(fontsize=5)
    if n % 4: 
        plt.yticks([])
    else:
        plt.yticks(fontsize=5)

    #snap_plot(t)



    # Limit plot area
    plt.axis([lon0, lon1, lat0, lat1])
    
    #plt.savefig("std_dev_ellipsis_no_%d.png" % (n+1), dpi=300)


#plt.show()
plt.savefig("multi_83100.png", dpi=300)





