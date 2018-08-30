#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-

"""Make an animated gif from ROMS output

Ferret is used in batch mode to produce a sequence of gif images
This images are then turned into an animated gif with the program gifsicle

Ferret   - available from http://ferret.wrc.noaa.gov/Ferret/
gifsicle - available from http://www.lcdf.org/gifsicle/
"""

# Bjørn Ådlandsvik, bjorn@imr.no
# Institute of Marine Research, Bergen
# 20 May 2004


import os
import glob



files = glob.glob('snapshot_???.png')
files.sort()


for f in files:
    g = 'tmp' + f.replace('png', 'gif')
    os.system('convert %s %s' % (f, g))


# Make the animated gif with gifsicle
#os.system("gifsicle --loop -d 10 --colors 256 tmp*.gif > a.gif")
os.system("gifsicle --loop -d 20 --colors 8 tmp*.gif > a.gif")

# Clean up
#os.system("rm -f auda.eps")
os.system("rm -f tmp*gif")
    
