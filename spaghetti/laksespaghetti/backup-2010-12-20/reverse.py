from datetime import datetime

# reverserer en tag-fil

date0 = datetime(2008, 5,25, 13, 0, 0)
date1 = datetime(2008,11,12, 12, 0, 0)


f0 = open('tag83101.dat')
f1 = open('tag83101.reverse.dat', 'w')

lines = f0.readlines()

W = [l.split() for l in lines]
W1 = W[::-1]

outlines = [' '.join((w[0],w[1])) + "   " + ' '.join((u[2],u[3]))
            for w, u in zip(W,W1)]

for line in outlines:
    f1.write(line+'\n')

f1.close()
