module topography

implicit none

include 'netcdf.inc'

! Constants
real, parameter :: pi = 3.1415926
real, parameter :: rad = pi/180.0
real, parameter :: deg = 180.0/pi

real, parameter :: lon0 = -10          ! West border
real, parameter :: lon1 = 50         ! East border
real, parameter :: lat0 = 60         ! South border
real, parameter :: lat1 = 80         ! North border
!real, parameter :: dlon = 1/60.0     ! Etopo1 grid size
!real, parameter :: dlat = 1/60.0     ! Etopo1 grid size
!real, parameter :: dinv = 30.0       ! Grid cells per degree 

! imax = (lon1-lon0)*60 + 1 = Number of grid nodes - east 
! jmax = (lat1-lat0)*60 + 1 = Number of grid nodes - north
integer, parameter :: imax = (lon1-lon0)*60 + 1
integer, parameter :: jmax = (lat1-lat0)*60 + 1

! Grid spacing NS [m]
!real, parameter :: dy = 1852  ! 1 minute = 1 nautical mile
! EW: dx = dy*cos(lon)

! Depth matrix, positive values in sea points [m]
!real, dimension(imax, jmax) :: H
real, dimension(imax, jmax) :: H

contains
!
!-------------------------------------
!
subroutine init_topo
  ! Denne versjonen leser ASCII-fil
  ! Dersom det ellers blir brukt NetCDF så bør denne
  ! bruke NetCDF også.
  logical, parameter :: debug = .FALSE.
  character(len=*), parameter ::                               &
       !fname = '/home/bjorn/Data/etopo1/ETOPO1_Bed_g_gmt4.grd'
       fname = '/heim/bjorn/data/etopo1/ETOPO1_Bed_g_gmt4.grd'
  !integer :: i, j
  !real :: h0
  !integer :: ierr
  integer :: ncid, varid
  integer :: status
  integer :: i0, j0
  integer(kind=2), dimension(imax, jmax) :: H0

  print *, "init_topo: opening ", fname
  print *, "topography: lon0, lat0 = ", lon0, lat0
  print *, "topography: imax, jmax = ", imax, jmax
  
  status = nf_open(fname, NF_NOWRITE, ncid)

  print *, "ncid = ", ncid
  call check_err(status)

  ! Read the topography array
  i0 = (lon0 + 180)*60 + 1
  j0 = (lat0 + 90)*60 + 1

  status = nf_inq_varid(ncid, 'z', varid)
  call check_err(status)
  print *, "varid = ", varid
  status = nf_get_vara_int2(ncid, varid, (/ i0, j0 /), (/ imax, jmax /), H0)
  !print *, "H(100,100) = ", H0(100,100)
  call check_err(status)

  ! Close the topography file
  status = nf_close(ncid)
  call check_err(status)

  ! Use real positive depths
  H = -H0
  
end subroutine init_topo

!
! ----------------------------
! 
subroutine sample_topo(lon, lat, depth)

  ! No interpolation, uses nearest neighbour

  real, intent(in) :: lon, lat
  real, intent(out) :: depth
  
  integer :: i, j

  ! sjekke om dette gir riktig koordinater
  i = nint((lon-lon0)*60+1)
  j = nint((lat-lat0)*60+1)
  depth = h(i,j)

end subroutine sample_topo

!
! ---------------------------------------------
!

subroutine check_err(status)
! NetCDF file operation error handling
  integer, intent(in) :: status
  if (status .ne. NF_NOERR) then
    print *, "***NetCDF error, program terminating"
    print *, "NetCDF error message:"
    print *, "  ", nf_strerror(status)
    stop
  endif
end subroutine check_err




end module topography
