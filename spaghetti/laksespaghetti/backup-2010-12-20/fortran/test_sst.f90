! Test of sst module
! Compile with 
! gfortran sst.o time_module.o test_sst.f90 \ 
!    -L/usr/local/lib -lnetcdff -lnetcdf -lhdf5_hl -lhdf5
! ------------------------------

program test_sst

  use sst_module

  real :: lon, lat
  integer :: m, d
  real :: asst, aerr

!  lon =  5.4
!  lat = 70.2
!  m = 10
!  d = 22
! ---
  lon =  10.2
  lat = 69.7
  m = 7
  d = 30


  call init_sst("../input/oisst_2008.nc")

  call sample_sst(lon, lat, m, d, asst, aerr)

  print *, asst, aerr

! should print 7.89 and 0.022063

end program test_sst
