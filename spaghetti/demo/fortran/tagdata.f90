module tagdata

! Module for reading tag data
! Data format: 4 columns
!   Date : yyyy-mm-dd
!   Time : hh:mm:ss
!   Pressure [dbar]
!   External temperature [degC]
!
! Presently, the file should be cropped so that
! First time = start_time and last_time = end_time
! (dette bør lett kunne generaliseres)
! Simulering går for helt antall dager 

use setup

  implicit none

  integer :: nobs 
    ! The number of observations used from the tag data file
  real, dimension(:), allocatable :: tag_depth
    ! The pressure of the tag [dbar]
  real, dimension(:), allocatable :: tag_temp
    ! The external temperature of the tag [degC]
  character(len=10), dimension(:), allocatable :: tag_date
    ! date-string of tag


contains

  subroutine read_tag

    integer, parameter :: unit = 11
    integer :: i
    !character(len=10) :: date
    character(len=8) :: time_of_day

    nobs = simdays*outper
    allocate(tag_depth(nobs), tag_temp(nobs), tag_date(nobs))

    open(unit, file=tag_file_name)

    do i = 1, nobs
!      read(unit,*) tag_date(i), time_of_day, tag_depth(i), tag_temp(i)
      read(unit,*) tag_date(i), time_of_day, tag_temp(i), tag_depth(i)
!      print *, date, " ",  time_of_day
    end do
 
    close(unit)

! --- testen under skal gi 9.1 og 4.07
!    print *, "tag(100): ", tag_depth(100), tag_temp(100)

  end subroutine read_tag


end module tagdata
