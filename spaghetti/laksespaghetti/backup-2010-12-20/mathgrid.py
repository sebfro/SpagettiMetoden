# -*- coding: iso-latin-1 -*-

# Make a ROMS NetCDF grid file from a mathematical description
#
#

# x, y = ROMS grid coordinates
# x = i, gives i-th rho-point (counting from 0 to L)
# similarly for j

from numpy import *
#from Scientific.IO.NetCDF import NetCDFFile

R_earth = 6378.137 # Earth radius   [km] 
rad     = pi/180.0
deg     = 180.0/pi


# Compute distances on a spherical earth with Haversine formula
# OBS, gir meningsløse verdier om utenfor området
# tatt fra m_lldist.m i Pawlowicz m_map pakke for Matlab
def dist(lon0, lat0, lon1, lat1):
    phi0    = lat0*rad
    phi1    = lat1*rad
    dphi    = phi1 - phi0
    dlambda = (lon1 - lon0) * rad
    a = sin(0.5*dphi)**2 + cos(phi0)*cos(phi1)*sin(0.5*dlambda)**2
    return 2 * R_earth * arctan2(sqrt(a), sqrt(1-a))

# Rett fram beregning: beregner lengden på korden = a
# deretter buen langs storesirkel
# Gir nøyaktig samme svar !!!
def dist2(lon0, lat0, lon1, lat1):
    cp0    = cos(lat0*rad)
    sp0    = sin(lat0*rad)
    cp1    = cos(lat1*rad)
    sp1    = sin(lat1*rad)
    cl0    = cos(lon0*rad)
    sl0    = sin(lon0*rad)
    cl1    = cos(lon1*rad)
    sl1    = sin(lon1*rad)
    a = sqrt(   (cl0*cp0 - cl1*cp1)**2
              + (sl0*cp0 - sl1*cp1)**2
              + (sp0 - sp1)**2 )
    return 2 * R_earth * arcsin(0.5*a)

def dist2b(lon0, lat0, lon1, lat1):
    x0 = cos(lon0*rad)*cos(lat0*rad)
    y0 = sin(lon0*rad)*cos(lat0*rad)
    z0 = sin(lat0*rad)
    x1 = cos(lon1*rad)*cos(lat1*rad)
    y1 = sin(lon1*rad)*cos(lat1*rad)
    z1 = sin(lat1*rad)
    a = sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2)
    return 2 * R_earth * arcsin(0.5*a)



def dist3(lon0, lat0, lon1, lat1):
    # Beregner vinkelen ved indreproduktet
    # => mer beregning, identisk resultat
    cp0    = cos(lat0*rad)
    sp0    = sin(lat0*rad)
    cp1    = cos(lat1*rad)
    sp1    = sin(lat1*rad)
    cl0    = cos(lon0*rad)
    sl0    = sin(lon0*rad)
    cl1    = cos(lon1*rad)
    sl1    = sin(lon1*rad)
    a01 = cl0*cp0*cl1*cp1 + sl0*cp0*sl1*cp1 + sp0*sp1
    a00 = cl0*cp0*cl0*cp0 + sl0*cp0*sl0*cp0 + sp0*sp0
    a11 = cl1*cp1*cl1*cp1 + sl1*cp1*sl1*cp1 + sp1*sp1
    return R_earth * arccos(a01/sqrt(a00*a11))

def dist3b(lon0, lat0, lon1, lat1):
    # Beregner vinkelen ved indreproduktet
    # => mer beregning, identisk resultat
    x0 = cos(lon0*rad)*cos(lat0*rad)
    y0 = sin(lon0*rad)*cos(lat0*rad)
    z0 = sin(lat0*rad)
    x1 = cos(lon1*rad)*cos(lat1*rad)
    y1 = sin(lon1*rad)*cos(lat1*rad)
    z1 = sin(lat1*rad)
    a00 = x0*x0 + y0*y0 + z0*z0
    a01 = x0*x1 + y0*y1 + z0*z1
    a11 = x1*x1 + y1*y1 + z1*z1
    return R_earth * arccos(a01/sqrt(a00*a11))


# --- Square mercator grid ---

class square_mercator:
    def __init__(self, lon0, lat0, dlon):
        self.lon0 = lon0
        self.lat0 = lat0
        self.dlon = dlon

    def grid2ll(self, x, y):
        h = self.dlon*rad
        phi0 = self.lat0*rad
        return ( self.lon0 + x*self.dlon,
                 (0.5*pi - 2*arctan(tan(0.25*pi-0.5*phi0)*exp(-y*h)))*deg
               )

    def ll2grid(self, lon, lat):
        h       = self.dlon*rad
        lambda0 = self.lon0*rad
        phi0    = self.lat0*rad
        phi     = lat*rad
        return ( (lon*rad - lambda0)/h,
                  log( tan(0.25*pi-0.5*phi0) / tan(0.25*pi-0.5*phi) ) / h
               )

    def angle(self, x, y):
        return 0.0


# --- Polarstereografisk "feltfile" grid

class square_stereographic:
    def __init__(self, xp, yp, dx, ylon):
        self.xp   = xp         
        self.yp   = yp
        self.dx   = dx
        self.ylon = ylon

   
    def grid2ll(self, x, y):
        phi0    = 60.0*rad
        lambda0 = self.ylon*rad
        xp  = self.xp
        yp  = self.yp
        dx  = self.dx
        lon = lambda0 + arctan2(x - xp, yp - y)
        r   = dx * sqrt((x-xp)*(x-xp) + (y-yp)*(y-yp))
        lat = 0.5*pi - 2*arctan(r / (R_earth*(1+sin(phi0))))
        return (lon*deg, lat*deg)
        
    def ll2grid(self, lon, lat):
        phi0    = 60.0*rad
        lambda0 = self.ylon*rad
        lambda_ = lon*rad
        phi     = lat*rad
        xp  = self.xp
        yp  = self.yp
        dx  = self.dx
        r = R_earth * cos(phi) * (1+sin(phi0)) / (1+sin(phi))
        x = xp + r*sin(lambda_ - lambda0)/dx
        y = yp - r*cos(lambda_ - lambda0)/dx
        return (x, y)

    # Er denne riktig ??, skifte tegn på begge argument
    #def angle(self, x, y):
    #    return arctan2(x-self.xp, y-self.yp)
    def angle(self, x, y):
        return 0.5*pi - arctan2(self.yp-y, self.xp-x)



# Polatsterographic square polar coordinates
# Bedre navn ?
# Gitt ved data:
# lengde, bredde for sentrum  S
# lengde, bredde for origo    O
# vinkelsteglengde, dangle    

class stereographic_wedge:
    def __init__(self, lonS, latS, lonO, latO, dangle):
        self.lonS = lonS
        self.latS = latS
        self.lonO = lonO
        self.latO = latO
        self.dangle = dangle

    def grid2ll(self, x, y):
        # Forenkler formlene med kompleks aritmetikk
        phi0    = 60.0*rad
        lambdaS = self.lonS*rad
        phiS    = self.latS*rad
        lambdaO = self.lonO*rad
        phiO    = self.latO*rad
        alpha   = self.dangle*rad

        rS = R_earth * cos(phiS) * (1+sin(phi0)) / (1+sin(phiS))
        rO = R_earth * cos(phiO) * (1+sin(phi0)) / (1+sin(phiO))
        j = complex(0, 1)
        zS = rS*exp(j*lambdaS)
        zO = rO*exp(j*lambdaO)
        d0 = abs(zS+zO)
                
        theta = y * alpha
        d = d0 * exp(alpha*x)

        #print "d0, d = ", d0, d
        #print "theta = ", theta

        zP = zS + (zO-zS)*d*exp(j*theta)/d0
        rP = abs(zP)
        lambdaP = arctan2(zP.imag, zP.real)
        phiP = 0.5*pi - 2*arctan(rP / (R_earth*(1+sin(phi0))))
        return (lambdaP*deg, phiP*deg)

    def ll2grid(self, lon, lat):
        lambda_ = lon*rad
        phi     = lat*rad
        phi0    = 60.0*rad
        lambdaS = self.lonS*rad
        phiS    = self.latS*rad
        lambdaO = self.lonO*rad
        phiO    = self.latO*rad
        alpha   = self.dangle*rad
        
        r =  R_earth * cos(phi) * (1+sin(phi0)) / (1+sin(phi))
        rS = R_earth * cos(phiS) * (1+sin(phi0)) / (1+sin(phiS))
        rO = R_earth * cos(phiO) * (1+sin(phi0)) / (1+sin(phiO))
        j = complex(0, 1)
        w  = r  * exp(j*lambda_)
        wS = rS * exp(j*lambdaS)
        wO = rO * exp(j*lambdaO)

        # exp(a(x+j*y)) = (w-wS)/(wO-wS)
        z1 = (w - wS)/(wO - wS)
        #x1 = z1.real
        #y1 = z1.imag
        #x  = log(sqrt(x1*x1 + y1*y1))/alpha
        #y  = arctan2(y1,x1)/alpha
        z = log(z1)/alpha
        return (z.real, z.imag)
        
# ---------------------------------------

# lon0 = minimum longitude
# lat0 = minimum latitiude
# dlon = step-lengde i longitude
# dlat = step-lengde i latitude

class spherical:
    def __init__(self, lon0, lat0, dlon, dlat):
        self.lon0 = lon0
        self.lat0 = lat0
        self.dlon = dlon
        self.dlat = dlat

    def grid2ll(self, x, y):
        return (self.lon0 + x*self.dlon, self.lat0 + y*self.dlat)

    def ll2grid(self, lon, lat):
        return ((lon - self.lon0)/self.dlon, (lat-self.lat0)/self.dlat)
    
        
    
    
