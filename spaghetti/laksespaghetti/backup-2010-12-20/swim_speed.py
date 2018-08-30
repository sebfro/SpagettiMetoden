# -*- coding: utf-8 -*-

# Versjon for 83100


import datetime
import numpy as np
from mathgrid import dist
#import matplotlib.pyplot as plt
#from netCDF4 import Dataset

# ---------------------
# Settings
# ---------------------



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


a = geoloc[0]
d = datetime.date(a[0],a[1],a[2])
t_old = (d - date0).days
lon_old = a[3]
lat_old = a[4]

for a in geoloc[1:]:
    d = datetime.date(a[0],a[1],a[2])
    t = (d - date0).days      # antall dager siden start
    lon = a[3]
    lat = a[4]
    avstand = dist(lon, lat, lon_old, lat_old)
    dt = t - t_old
    print "%s  %d  %5.1f   %4.2f" % (d, dt, avstand, avstand / (dt*86.4))
    lon_old = lon
    lat_old = lat
    t_old = t



    





