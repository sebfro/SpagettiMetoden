module tempatlas

  use grid, only : xy2ll

  implicit none

  include 'netcdf.inc'

  integer, parameter :: nlon = 129
  integer, parameter :: nlat = 66
  integer, parameter :: ndepth = 101
  integer, parameter :: ntimes = 4

  real, parameter :: lon0 = 6.0
  real, parameter :: lat0 = 68.0
  real, parameter :: depth0 = 0.0

  real, parameter :: dlon = 0.5
  real, parameter :: dlat = 0.2
  real, parameter :: ddepth = 5.0

  real, dimension(nlon, nlat, ndepth, ntimes) :: temp
  real, dimension(nlon, nlat, ndepth, ntimes) :: tstd
  

contains

  ! -----------------------------------------------

  subroutine init_atlas
    
    integer :: ncid, varid
    integer :: status

    status = nf_open('amean.nc', NF_NOCLOBBER, ncid)

    status = nf_inq_varid(ncid, 'Temp', varid)
    status = nf_get_var_real(ncid, varid, temp)

    status = nf_inq_varid(ncid, 'Tstd', varid)
    status = nf_get_var_real(ncid, varid, tstd)

    status = nf_close(ncid)

  end subroutine init_atlas

  ! ---------------------------------------------
  
  subroutine sample_atlas(x, y, z, t, atemp, astd)

    real, intent(in) :: x, y   ! lon, lat
    real, intent(in) :: z      ! depth
    integer, intent(in) :: t      ! month = 1..12
    real, intent(out) :: atemp
    real, intent(out) :: astd

    integer :: i, j, k, l
    real :: lon, lat

    call xy2ll(x, y, lon, lat)

    i = int((lon-lon0)/dlon) + 1
    j = int((lat-lat0)/dlat) + 1
    k = int((z-depth0)/ddepth) + 1
    l = 1 + mod(t, 12)/3

!    print *, lon, lat, z, t
!    print *, i, j, k, l

    if ((i < 1) .or. (i > nlon)) then
      atemp = -999.999
      astd  = -999.999
      return
    end if

    if ((j < 1) .or. (j > nlat)) then
      atemp = -999.999
      astd  = -999.999
      return
    end if

    atemp = temp(i,j,k,l)
    astd  = tstd(i,j,k,l)

    if ((atemp < -2.0) .or. (astd < 0.0)) then
      atemp = -999.999
      astd  = -999.999
    end if
 
  end subroutine sample_atlas


end module tempatlas
