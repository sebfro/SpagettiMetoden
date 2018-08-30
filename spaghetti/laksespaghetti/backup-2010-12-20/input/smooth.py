import numpy as np

fname0 = 'tag83100.dat'
fname1 = 'tag83100s.dat'


# -------------------
# read input data
# -------------------

f0 = open(fname0)

dates = []
times = []
temp = []
depth = []

for line in f0:

    w = line.split()

    dates.append(w[0])
    times.append(w[1])

    d = float(w[3])
    depth.append(d)

    x = float(w[2])
    if x > 4000.: x = np.NaN
    temp.append(x)

atemp = np.array(temp)

# Fill in missing data, linear interpolation
# Assumes first and last value exists

#t0 = temp[0]
#t1 = temp[-1]

oldtemp = temp[0]
mode = 'valid'

for i in xrange(len(temp)):
    x = temp[i]
    if mode == 'valid': 
        if np.isnan(x):
            i0 = i
            mode = 'nan'
        else:
            oldtemp = x
    else:  # nan - modus
        if not np.isnan(x):
            i1 = i
            mode = 'valid'
            # constant at mean, could be improved
            atemp[i0:i1] = 0.5*(oldtemp + x)


# smooth
#btemp = atemp.copy()

nhours = 120  # 5 days

K = np.array([0.5] + nhours*[1] + [0.5]) / float(nhours)

# pad (more than enough)
aatemp = np.array(nhours*[temp[0]] + list(atemp) + nhours*[temp[-1]])


bbtemp = np.convolve(aatemp, K, mode='same')

btemp = bbtemp[nhours:-nhours]


# ----------

f1 = open(fname1, 'w')

for w in zip(dates, times, btemp, depth):

    #print '%s %s %7.2f %7.2f' % w
    f1.write('%s %s %7.2f %7.2f\n' % w)

f1.close()



    
        

