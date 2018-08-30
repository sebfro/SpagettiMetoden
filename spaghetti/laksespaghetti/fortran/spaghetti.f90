program spaghetti

use setup
use topography
use position
use tagdata
use output
use sst_module

implicit none


real, parameter :: maxspeed = 2.0    ! Maximum speed [m/s]

!real :: x0, y0     ! Start position 
!real :: x1, y1     ! End position
real :: time    ! Time in decimaldays since start
integer :: timestep

!integer :: nstep                     ! Number of time steps

!real :: Norm, Udir, Vdir



integer :: step
integer :: daynr
!integer :: l
!real :: xdir, ydir

!real :: xnew, ynew
!real :: urand, vrand



! ---------------------------------------------------------------


!
! --- Read the setup file
!
call readsup()

!
! --- Read the topography file
!
print *, "before init_grid"
call init_topo()

!
! --- Read the tracking data file
!
print *, "before read_tag"
call read_tag()

!
! --- Read SST data
!
print *, "before init_atlas"
call init_sst("input/oisst_2008.nc")
print *, "etter init_atlas"


!
! Init the particle tracking 
!
call init_FW_position()

!
! --- Open output files
!
call init_FW_output()

! --- Save initial outpur
call save_FW_output(0)

!
! --- Forward simulation loop
!
print *, "Starting forward simulation"

do daynr = 1, simdays

  do step = 1, outper
    timestep = (daynr-1)*outper + step
    time = daynr-1 + real(step-1)/outper
    call movefishFW(timestep)
  end do

  print *, 'daynr, #fish = ', daynr, sum(life)

  ! Output
  call save_FW_output(daynr)

end do ! daynr

call close_FW_output()


!
! --- Backward simulation loop
!

call init_BW_position()
call init_BW_output()
call save_BW_output(0)

print *, "Starting backward simulation"


do daynr = 1, simdays

  do step = 1, outper
    timestep = (daynr-1)*outper + step
    !time = daynr-1 + real(step-1)/outper
    !timestep = simdays*outper - (daynr-1)*outper - step + 1
    !print *, timestep
    call movefishBW(timestep)
  end do

  print *, 'daynr, #fish = ', daynr, sum(life)

  ! Output
  call save_BW_output(daynr)

end do ! daynr

call close_BW_output()



end program spaghetti
