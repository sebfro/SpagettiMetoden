#!/usr/bin/env python
# -*- coding: iso-latin-1 -*-


#
import Numeric
from Scientific.IO.NetCDF import *
import gmt
import os


# Settings for GMT ploting
grdfile  = "atlastopo.grd"
cptfile  = "e.cpt"
gradfile = "atlastopo_i.grd"
psfile   = "a.ps"

lon0 = 6
lon1 = 70
lat0 = 68
lat1 = 81

#proj    = "JL%d/60/68/81/16c" % (0.5*(lon0+lon1),)
proj    = "JM16c"
bord    = 'B10g10/5g5.:"Etopo2":WSen'
#bord    = 'B2g2/1g1.:"Etopo2":WSen'
region = '-R6/70/68/81'

angle = 60
debug=1


# ---------------------
# Make colour scale
# ---------------------

#use the old cpt-file from etopoplot



gmtcommand = "grdgradient %s -G%s -A%s -Nt1" % (grdfile, gradfile, angle)
if debug: print gmtcommand
os.system(gmtcommand)

#psbasemap -JM12c  -P -K > a.ps

gmtcommand = ( "grdimage %s -C%s -I%s -%s -%s -P > %s"
                % (grdfile, cptfile, gradfile, proj, bord, psfile) )
if debug: print gmtcommand
os.system(gmtcommand)

# clean up
#os.remove(grdfile)
#os.remove(cptfile)
os.remove(gradfile)

# ----------------------------
# Show the result
# ----------------------------
syscommand = "/usr/X11R6/bin/gv %s" % psfile
if debug: print syscommand
os.system(syscommand)
