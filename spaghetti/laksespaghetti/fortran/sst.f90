module sst_module

  use time_module

  implicit none

  include 'netcdf.inc'

  integer, parameter :: nlon = 60
  integer, parameter :: nlat = 20
  integer, parameter :: ntimes = 53  ! Bør leses fra fil, kan variere

  real, parameter :: lon0 = -10.0
  real, parameter :: lat0 =  60.0

  real, parameter :: dlon = 1.0
  real, parameter :: dlat = 1.0

  real, dimension(nlon, nlat, ntimes) :: sst
  real, dimension(nlon, nlat, ntimes) :: err
  
!private

  integer, dimension(ntimes) :: days

contains

  ! -----------------------------------------------

  subroutine init_sst(fname)
    
    character(len=*), intent(in) :: fname
    integer :: ncid, varid
    integer :: status

    print *, "init_sst: opening ", fname
    status = nf_open(fname, NF_NOWRITE, ncid)
!    status = nf_open(fname, NF_READ, ncid)
     print *, "ncid = ", ncid, status
    call check_err(status)

    status = nf_inq_varid(ncid, 'time', varid)
    status = nf_get_var_int(ncid, varid, days)

    status = nf_inq_varid(ncid, 'sst', varid)
    status = nf_get_var_real(ncid, varid, sst)

    status = nf_inq_varid(ncid, 'err', varid)
    status = nf_get_var_real(ncid, varid, err)

    status = nf_close(ncid)



  end subroutine init_sst

  ! ---------------------------------------------
  
  subroutine sample_sst(lon, lat, m, d, asst, aerr)

    real, intent(in) :: lon, lat ! Position
    integer, intent(in) :: m, d  ! Time: month, day
    real, intent(out) :: asst    ! SST estimate
    real, intent(out) :: aerr    ! error estimate

    integer :: i, j, l
    integer, dimension(1) :: l1
    integer :: jday

    type(time_type) :: date, date0

    ! Find indices of grid cell containing the point
    i = int((lon-lon0)/dlon) + 1
    j = int((lat-lat0)/dlat) + 1

    !print *, "i, j = ", i, j

    ! Find index of week containing the time
    date  = (/ 2008, m, d, 0, 0, 0 /)
    date0 = (/ 2008, 1, 1, 0, 0, 0 /)
    jday = int(date-date0)          ! Day of year (starting with zero)
    l1 = minloc(abs(days-jday))
    l = l1(1)                       ! Fortran index of week
    !print *, "l = ", l, days(l)

!    print *, lon, lat, z, t
!    print *, i, j, k, l

    asst = sst(i,j,l)
    aerr = err(i,j,l)
 
  end subroutine sample_sst

! ------------------------------------

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

end module sst_module
