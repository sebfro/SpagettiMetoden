# --- coding: utf-8 ---

import sys
import datetime
import numpy as np
from netCDF4 import Dataset

# USAGE:
# python merge2.py [setup_file]

# --------------------
# User settings
# --------------------

setup_file_default = './spaghetti.sup'

Dlim = 20.0   # Limiter for merging distance in km

verbose = True

# -------------------
# Utility functions
# -------------------

# Function for reading from setup file
def readln(f):
    """ Read a line from open file f, skipping blanks and comments"""
    for line in f:
        line = line.strip()
        if line and line[0] != '!': break
    return line


# ----------------------------
# Read set-up file
# ----------------------------


# Handle the command line argument for the setup file
if len(sys.argv) == 1:
    setup_file = setup_file_default
else:
    setup_file = sys.argv[1]

if verbose: print "setup file =", setup_file


# Open the set-up file
try:
    sup = open(setup_file, 'r')
except IOError:
    print "***ERROR, can not open setup-file " + setup_file
    sys.exit(1)

# Read start date
date0 = readln(sup).split()[0]                     # "yyyy-mm-dd"
date0 = datetime.date(*[int(d) for d in date0.split('-')])  # date(y, m, d)
if verbose: print "Start date = %s" % str(date0)

# Skip start position
readln(sup)
readln(sup)

# Read end date
date1 = readln(sup).split()[0]                     # "yyyy-mm-dd"
date1 = datetime.date(*[int(d) for d in date1.split('-')])  # date(y, m, d)
if verbose: print "End date   = %s" % str(date1)

# Skip end position and tag-file
readln(sup)
readln(sup)
readln(sup)

# Files
forward_file = readln(sup)
backward_file = readln(sup)
output_file = readln(sup)
if verbose: 
    print "Forward file  =", forward_file
    print "Backward file =", backward_file
    print "Output file   =", output_file


sup.close()

# ----------------------------------------
# First scan, find trajectories to merge
# ----------------------------------------

f1 = Dataset(forward_file)
f2 = Dataset(backward_file)

ndays = (date1-date0).days + 1
print "ndays = ", ndays

Ntraj = len(f1.dimensions['fish']) # Number of trajectories
if verbose: print "Ntraj = ", Ntraj


# ndays = odd = 2*k + 1, take k+1 forwards and k backwards
#   i.e. merge forward[:k+1] with backward[-k:]
# ndays = even = 2*k, take k each way
#   i.e. merge forward[:k] with backward[-k:]

k = (ndays)//2    # integer division, works in both cases
k0 = k + ndays % 2  # k+1 if ndays is odd, otherwise k

print "k, k0 = ", k, k0

# For each forward track fine nearest backwards at merging time
# distance forward[k0-1] to backwards[k-1]
# reject if not close enough
# merging forward[:k0] with backward[:k]
# as merged[:k0] = forward[:k0]         0, 1, ..., k0-1
#    merged[-k0:] = backward[k-1::-1]   k0, +1,  +k;   k-1, k-2, ..., 0

n = -1

# Life indicator at merging time
FWlife = f1.variables['life'][k0-1,:]
BWlife = f2.variables['life'][k-1,:]

# Forward position at merge time
X1 = f1.variables['X'][k0-1,:]
Y1 = f1.variables['Y'][k0-1,:]

# Backwards position at merge time
X2 = f2.variables['X'][k-1,:]
Y2 = f2.variables['Y'][k-1,:]


P = []  # List of merged forward trajectories
Q = []  # List of merged backward trajectories

n = 0   # Counter for merged trajectories

I, = np.nonzero(FWlife)     # Indices to active FW tracks
J, = np.nonzero(BWlife)     # Indices to active BW tracks

for p in I:            # Loop over active forwards tracks
    x, y = X1[p], Y1[p]
    lonfac = np.cos(y*np.pi/180.0)
    D = lonfac*lonfac*(X2[J]-x)**2 + (Y2[J]-y)**2 # Squared distance
    q0 = np.argmin(D)                             # Closest BW track
    Dq = np.sqrt(D[q0])*1.852*60                  # Distance in km to closest track
    if Dq < Dlim:
        n = n+1    
        P.append(p)
        q = J[q0]                                 # Index to closest track among all
        Q.append(q)
        print n, p, q, np.sqrt(D[q0])*1.852*60



N = len(P)  # Number of merged trajectories

if verbose: 
    print "First scan finished"
    print "Number of merged trajectories = ", N



# --------------------
# Create output file
# --------------------

fout = Dataset(output_file, 'w', format='NETCDF3_CLASSIC')
#fout = Dataset(output_file, 'w')

# Dimensions
fout.createDimension('time', ndays) 
fout.createDimension('tracknr', N)

# Coordinate variables
# Bedre å ikke ta med dimensjonsløs koord.variabel?
#v = fout.createVariable('tracknr', 'i', ('tracknr',))
#v.long_name = 'trajectory number'
#v[:] = np.arange(N, dtype='int')

v = fout.createVariable('time', 'd', ('time',))
v.long_name = 'time'
v.units = 'days since ' + str(date0)
v[:] = np.arange(ndays)

# Data variables

v = fout.createVariable('lon', 'f', ('time', 'tracknr'))
v.long_name = "longitude"
v.units = "degrees_east"

v = fout.createVariable('lat', 'f', ('time', 'tracknr'))
v.long_name = "latitude"
v.units = "degrees_north"

v = fout.createVariable('p', 'i', ('tracknr',))  # Indeks i første fil
v.long_name = "Forward index"
#v.units = 'nondimensional'

v = fout.createVariable('q', 'i', ('tracknr',))  # indeks i andre fil
v.long_name = "Backward index"


# Global attributes (not needed anymore)
# Virker ikke med NETCDF3_CLASSIC???
#fout.nTrack = N
fout.Conventions = 'CF-1.0'
fout.institution = 'Institute of Marine Research'
fout.source = "The spaghetti geolocation model by Bjørn Ådlandsvik, IMR"
fout.history = 'created %s by merge2.py from %s and %s' %          \
         (str(datetime.date.today()), forward_file, backward_file)

# ---------------------------------
# Merge and save the trajectories
# ---------------------------------

fout.variables['lon'][:k0, :] = f1.variables['X'][:k0, P]
fout.variables['lon'][k0:, :] = f2.variables['X'][k-1::-1, Q]

fout.variables['lat'][:k0, :] = f1.variables['Y'][:k0, P]
fout.variables['lat'][k0:, :] = f2.variables['Y'][k-1::-1, Q]

# Save forward and backwards indices
fout.variables['p'][:] = P
fout.variables['q'][:] = Q


# -------------
# Clean up
# -------------
            
f1.close()
f2.close()
fout.close()        
        


            
            
