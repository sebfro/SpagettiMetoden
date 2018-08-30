module grid

implicit none


! NB domain is larger than temperature atlas domain
! to better include the Lofoten area
! Constants
real, parameter :: pi = 3.1415926
real, parameter :: rad = pi/180.0
real, parameter :: deg = 180.0/pi


real, parameter :: lon0 = 0          ! West border
real, parameter :: lon1 = 70         ! East border
real, parameter :: lat0 = 65         ! South border
real, parameter :: lat1 = 81         ! North border
real, parameter :: dlon = 1/30.0     ! Etopo2 grid size
real, parameter :: dlat = 1/30.0     ! Etopo2 grid size
!real, parameter :: dinv = 30.0       ! Grid cells per degree 

! imax = (lon1-lon0)*30 + 1 = Number of grid nodes - east 
! jmax = (lat1-lat0)*30 + 1 = Number of grid nodes - north
integer, parameter :: imax = 2101, jmax = 481

! Grid spacing NS [m]
real, parameter :: dy = 2*1852  ! 2 nautical miles
! EW: dx = dy*cos(lon)

! Depth matrix, positive values in sea points [m]
real, dimension(imax, jmax) :: H

contains
!
!-------------------------------------
!
subroutine init_grid
  ! Denne versjonen leser ASCII-fil
  ! Dersom det ellers blir brukt NetCDF så bør denne
  ! bruke NetCDF også.
  logical, parameter :: debug = .FALSE.
  integer :: i, j
  real :: h0
  
  open(11, file='etopo2_codyssey.dat')
  
  do i = 1, imax
    do j = 1, jmax
      read(11,*) h0
      H(i,j) = -h0
    end do
  end do
  
  if (debug) then
    write(*,*) "init_grid: finished"
    write(*,*) "  H(1000,200) = ", H(1000,200)
    write(*,*) "  Above value should be 290"
  end if
  
end subroutine init_grid
!
! ------------------------------------
!
subroutine xy2ll(x, y, lon, lat)
  real, intent(in) :: x, y
  real, intent(out) :: lon, lat
  
  lon = lon0 + dlon*x
  lat = lat0 + dlat*y

end subroutine xy2ll
!
! ----------------------------------------
!
subroutine ll2xy(lon, lat, x, y)
  real, intent(in) :: lon, lat
  real, intent(out) :: x, y

  x = (lon-lon0)/dlon
  y = (lat-lat0)/dlat

end subroutine ll2xy




end module grid
