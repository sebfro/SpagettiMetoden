module position

  use grid
  use setup
  use tagdata
  use tempatlas, only : sample_atlas

  implicit none

  integer, parameter :: nFish = 10000   ! Number of particles
  real, dimension(nFish) :: X, Y        ! Grid coordinates of particles
  integer, dimension(nFish) :: life     

contains

  !
  ! ==========================================
  ! 
  subroutine init_FW_position

    integer :: n

    do n = 1, nFish
      X(n) = x0
      Y(n) = y0
      life(n) = 1
    end do

    ! --- Initiate the random number generator
    call random_seed()

  end subroutine init_FW_position
  
  ! ----------------------------------------

  subroutine init_BW_position

    integer :: n

    do n = 1, nFish
      X(n) = x1
      Y(n) = y1
      life(n) = 1
    end do

    ! --- Initiate the random number generator
    !call random_seed()

  end subroutine init_BW_position

  !
  ! =========================================
  ! 

  ! Wrappers for forward/backward simulation
  subroutine movefishFW(timestep)
    integer, intent(in) :: timestep
    call movefish(timestep, x1, y1, 1)
  end subroutine movefishFW
  
  subroutine movefishBW(timestep)
    integer, intent(in) :: timestep
    call movefish(timestep, x0, y0, -1)
  end subroutine movefishBW
  

  subroutine movefish(timestep, xtarget, ytarget, direction)

    integer, intent(in) :: timestep
    real, intent(in) :: xtarget
    real, intent(in) :: ytarget
    integer, intent(in) :: direction  ! +1 forw, -1 back

    real :: time

    real, parameter :: pi = 3.1415926
    real, parameter :: detlimit = 0.9
    real, parameter :: detlim2 = detlimit*detlimit
    real, parameter :: randspeed = 0.7
!    real, parameter :: randspeed = 1.4
!    real, parameter :: randspeed = 2.5 
!    real, parameter :: randspeed = 3.0 
!    real, parameter :: randspeed = 0.75 ! dt = 2 h => K = 2025)
     


!    logical, parameter :: use_temp = .FALSE.
    logical, parameter :: use_temp = .TRUE.

!    real, parameter :: stdfac  = 2.5   ! temperatur tolerance
!    real, parameter :: stdfac2 = 3.0   ! temperatur tolerance
    real, parameter :: stdfac  = 0.8  ! temperatur tolerance
    real, parameter :: stdfac2 = 1.0  ! temperatur tolerance
!    real, parameter :: stdfac  = 3.0  ! temperatur tolerance
!    real, parameter :: stdfac2 = 3.5  ! temperatur tolerance

!    real, parameter :: dfac = 1000.0
    real, parameter :: dfac = 1.3
!    real, parameter :: dfac = 1.4
    real, parameter :: add_depth = 0.0
!    real, parameter :: add_depth = 25.0
      ! Detph adjustment factor

!    real :: Xdet, Ydet
!    real :: Norm
    real :: Udet, Vdet      ! Deterministic velocity   [m/s]
    real :: Urand, Vrand    ! Random velocity          [m/s]
    real :: Xnew, Ynew
    integer :: n            ! Particle counter
!    real :: deltaX, deltaY
    real :: lonfac          ! Adjustment for map distortion
    real :: a, angle        ! Uniform random number and angle
    integer :: i,j
    integer :: month
    real :: atemp, astd
    logical :: tempOK
    integer :: tstep 

    ! running time [days]
    time = real(timestep) / outper

    !print *, timestep, time, tag_depth(timestep)
    if (direction < 0)  then
      tstep = simdays*outper + 1 - timestep
    else
      tstep = timestep
    end if

    do n = 1, nFish
      if (life(n) == 1) then  ! Only consider active fish


       lonfac = cos((lat0 + dlat*Y(n))*rad)

       ! 
       ! Compute deterministic velocity
       ! the velocity that would take the particle to the
       ! catch position in the remaining time
       !   
       Udet = (xtarget-X(n))*lonfac*dy/ ((simdays-time)*86400)
       Vdet = (ytarget-Y(n))*dy / ((simdays-time)*86400)
       if ((Udet*Udet + Vdet*Vdet) > detlim2) then
         ! Fish cannot reach target in time, terminate !!!
         life(n) = 0
         cycle         ! Continue with next fish
       end if

         
       ! Random component
       ! (bør restrisere hastighet etter hvor stor del den deterministiske er
       call random_number(a)
       angle = 2*pi*a
       Urand = randspeed * cos(angle)
       Vrand = randspeed * sin(angle)

      !if (n == 100) then
      !  print *, "detVel = ",   sqrt(Udet*Udet + Vdet*Vdet)
      !  print *, "Urand, Vrand = ", Urand, Vrand
      !end if

       ! Update positions (OBS, dt er i minutter)
       Xnew = X(n) + (Udet + Urand)*60*dt/(dy*lonfac)
       Ynew = Y(n) + (Vdet + Vrand)*60*dt/dy

       ! Sjekk om depth-terminate
       ! Tar dyp til nærmeste grid-punkt
       !   Vurder interpolasjon
       i = int(Xnew)
       j = int(Ynew)

       i = max(i, 1)
       i = min(i, imax)
       j = max(j, 1)
       j = min(j, jmax)


       !if (n == 100) then
       !  print *, i, j, H(i,j), tag_depth(tstep)
       !end if
        

       ! Sample temperatur og stdavvik
       ! trenger måned
       read(tag_date(tstep), '(5X,I2,3X)') month
       if (use_temp) then
         call sample_atlas(Xnew, Ynew, tag_depth(tstep), month, atemp, astd)

         tempOK = ((astd < 0.1) .or.                              &
                      ((tag_temp(tstep) > atemp-stdfac*astd)     &
                 .and. (tag_temp(tstep) < atemp+stdfac*astd) ))
       else
         tempOK = .true.
       end if

! Bunnkontakt
! OK dersom baklengs, eller (tid utenfor tidsvindu) eller (riktig dyp)
!        tempOK = ((ytarget > 70) .or. (time < 20) .or. (time > 70) &
!                  .or. (H(i,j) < dfac*tag_depth(tstep)))
!         tempOK = .True.

!       print *, "XXX", i, j, tstep

       if ( (tag_depth(tstep) <= dfac*H(i,j) + add_depth)     &
             .and. (H(i,j) <= 1000)                              &
             .and. tempOK ) then

         ! New position OK
         X(n) = Xnew
         Y(n) = Ynew

       else ! tag_depth > dfac*H or H > 1000 or not tempOK
          ! check old position
          i = int(X(n))
          j = int(Y(n))
          i = max(i, 1)
          i = min(i, imax)
          j = max(j, 1)
          j = min(j, jmax)
          if (use_temp) then
            call sample_atlas(X(n), Y(n), tag_depth(tstep),      &
                              month, atemp, astd)
            tempOK = (astd < 0.1) .or.                              &
                       ((tag_temp(tstep) > atemp-stdfac2*astd)       &
                  .and. (tag_temp(tstep) < atemp+stdfac2*astd) )
         else
          tempOK = .True.
         endif 
          if ((tag_depth(tstep) > dfac*H(i,j) + add_depth)       &
              .or. (.not. tempOK) ) then
            ! old position not OK, terminate
            life(n) = 0
          end if
       end if



!       if (life(n) == 1) then ! update position
!         X(n) = Xnew
!         Y(n) = Ynew
!         X(n) = Xnew
!       end if ! life(n)

      end if ! life(n)
    end do ! n

    ! Count the number of living fish
    !print *, "movefish: finished, number of living fish = ", sum(life)      

  end subroutine movefish




end module position
