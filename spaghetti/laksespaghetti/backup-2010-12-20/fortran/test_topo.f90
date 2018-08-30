! Test of topo module
! Compile with 
! gfortran topo.o time test_topo.f90 \ 
!    -L/usr/local/lib -lnetcdff -lnetcdf 
! ------------------------------

program test_topo

  use topography

  real, parameter :: lon = 27.3130
  real, parameter :: lat = 73.8340
  real, parameter :: eps = 0.001
  real :: H2


  call init_topo()

  call sample_topo(lon, lat, H2)
  print *, "H = ", H2

  call sample_topo(lon+eps, lat+eps, H2)
  print *, "H = ", H2

  call sample_topo(lon-eps, lat+eps, H2)
  print *, "H = ", H2

  call sample_topo(lon-eps, lat-eps, H2)
  print *, "H = ", H2

  call sample_topo(lon+eps, lat-eps, H2)
  print *, "H = ", H2


end program test_topo

