module setup

  use time_module
!  use grid  

  implicit none

  logical, parameter, private :: DEBUG = .TRUE.
  integer, parameter, private :: SUPFIL = 17

  type(time_type) :: start_time
  type(time_type) :: stop_time

  real :: lon0, lat0  ! start location  [deg]
  real :: lon1, lat1  ! end location      [deg]

! Bruker n� lon, lat trenger ikke x-ene
!  real :: x0, x1      ! start location  [grid units]
!  real :: y0, y1      ! ens location    [grid units]


  integer :: nstep

  character(len=80) :: tag_file_name
  
  ! Ha noen output-filer ogs� 
  character(len=80) :: forward_outfile_name
  character(len=80) :: backward_outfile_name
  
  ! Setting for termination

  integer :: nFish     ! Number of trajectories
  real :: randspeed    ! Random speed
  real :: dfac         ! Htag < dfac*Htopo + add_depth
  real :: add_depth
  real :: temp_lim     ! temperature difference <= temp_lim


  real :: dt       ! Input time step
  integer :: outper   ! Number of input time steps per output time
  integer :: simdays  ! Number of days to simulate

  contains

! -----------------
  subroutine readsup(supfile_name)
! -----------------

    character(len=80), intent(in) :: supfile_name

    character(len=80) linje
!    integer, dimension(6) :: timevec
!    integer :: daystep
!    integer :: dtout

!    integer :: i

!
!***FIRST EXECUTABLE STATEMENT LESSUP
!
    if (DEBUG) write(*,*) 'READSUP: Started'

    open(SUPFIL, file=supfile_name, status='old', action='read') 
    if (DEBUG) write(*,*) 'READSUP: Opened set-up file'

    ! --- Start time
    call readln(linje) 
    start_time = linje
    print *, "start time = ", timestr(start_time)

    ! --- Start position
    call readln(linje)
    read(linje,*) lon0
    call readln(linje)
    read(linje,*) lat0
    print *, "start position = ", lon0, lat0
    !call ll2xy(lon_start, lat_start, x0, y0)

    ! --- Stop time
    call readln(linje) 
    stop_time = linje
    print *, "end time   = ", timestr(stop_time)
 
    ! --- Stop position
    call readln(linje)
    read(linje,*) lon1
    call readln(linje)
    read(linje,*) lat1
    print *, "end position   = ", lon1, lat1
    !call ll2xy(lon1, lat1, x1, y1)

   
    ! --- Files
    call readln(linje)
    read(linje,*) tag_file_name
    print *, "Tag file: ", tag_file_name

    call readln(linje)
    read(linje,*) forward_outfile_name
    print *, "Forward trajectory output : ", forward_outfile_name

    call readln(linje)
    read(linje,*) backward_outfile_name
    print *, "Backward trajectory output: ", backward_outfile_name

    ! Skip output file for merging script
    call readln(linje)


    ! --- Termination settings

    call readln(linje)
    read(linje, *) nFish
    print *, "number of trajectories = ", nFish

    call readln(linje)
    read(linje,*) randspeed
    print *, "random speed = ", randspeed

    call readln(linje)
    read(linje,*) dfac
    print *, "depth factor = ", dfac
    call readln(linje)
    read(linje,*) add_depth
    print *, "added depth = ", add_depth
    call readln(linje)
    read(linje,*) temp_lim
    print *, "temperature tolerance = ", temp_lim





    ! --- Time steps
    call readln(linje)
    read(linje,*) dt
    print *, "Input time step  = ", dt, " min"

    call readln(linje)
    read(linje,*) outper
    print *, "Output time step = ", dt*outper/60, " hours"

! --- Clean up and finish.
!
    close(SUPFIL)

! --- Derived values
    simdays = nint(stop_time - start_time)



  end subroutine readsup

! -----------------------------
! ***************************** 
! -----------------------------
  subroutine readln(Line)
! -----------------------------
  !
  ! --------------------------------------
  !  Reads a line from a file, skipping
  !  comments and blank lines.
  !
  !  Comments starts with a character from
  !  COMCHAR and continues to the end of line.
  ! 
  !  Readln reads a line.
  !  If the line contains a comment, the comment is removed.
  !  If thereafter the line is blank, the line is skipped
  !  and the procedure repeated with a new line.
  !
  !  Bj�rn �dlandsvik,
  !  IMR, October 1997
  ! --------------------------------------

  !
  ! --- Arguments ---
  !
    character(len=*), intent(out) :: Line
  !   First non comment line read
  !
  ! --- Local constants
  !
    character(len=*), parameter :: COMCHAR = "*!#"
  !   Comment starting characters
  !
  ! --- Local variables
  !
    integer :: ipos
  !   Start position for comment
  !
  ! --------------------------------
  !
    do
    !
    ! --- Read a line
    !
      read(unit=SUPFIL, fmt="(A)") Line
    !
    ! --- Scan for comments
    !
      ipos = scan(Line, COMCHAR)
    !
    ! --- Remove any comments 
    !
      if (ipos /= 0) then  
        Line = Line(:ipos-1)
      end if
    !
    ! --- Exit loop if result is not blank
    !
      if (len_trim(Line) /= 0) then  
        exit
      end if

    end do

  end subroutine readln
! ------------------------------
! ******************************

end module setup




