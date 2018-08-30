# -*- coding: utf-8 -*-

"""Read the OIv2 land mask"""

import numpy as np

lonmax = 360
latmax = 180

#tagls = np.zeros((latmax, lonmax), dtype='float32')

#f = open('lstag.onedeg.dat', 'rb')

tagls = np.fromfile('lstags.onedeg.dat', dtype='>f4')

tagls.shape = (latmax, lonmax)

