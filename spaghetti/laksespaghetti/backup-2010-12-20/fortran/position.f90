module position

  use topography, only : sample_topo, rad
  use setup
  use tagdata, only : tag_depth, tag_temp
  use sst_module, only : sample_sst
  use time_module

  implicit none

!  integer, parameter :: nFish = 1000000   ! Number of particles
!   integer, parameter :: nFish = 500000   ! Number of particles
!  integer, parameter :: nFish = 2000   ! Number of particles
!  integer :: nFish   ! Number of trajectories (particles)
   
  real, dimension(:), allocatable :: Lon, Lat    ! lon, lat of particles
  integer, dimension(:), allocatable :: life     

contains

  !
  ! ==========================================
  ! 
  subroutine init_FW_position

    integer :: n

    allocate(Lon(nFish), Lat(nFish), life(nFish))

    do n = 1, nFish
      Lon(n) = lon0
      Lat(n) = lat0
      life(n) = 1
    end do

    ! --- Initiate the random number generator
    call random_seed()

  end subroutine init_FW_position
  
  ! ----------------------------------------

  subroutine init_BW_position

    integer :: n

    do n = 1, nFish
      Lon(n) = lon1
      Lat(n) = lat1
      life(n) = 1
    end do

    ! --- Initiate the random number generator
    call random_seed()

  end subroutine init_BW_position

  !
  ! =========================================
  ! 

  ! Wrappers for forward/backward simulation
  subroutine movefishFW(timestep)
    integer, intent(in) :: timestep
    call movefish(timestep, lon1, lat1, 1)
  end subroutine movefishFW
  
  subroutine movefishBW(timestep)
    integer, intent(in) :: timestep
    call movefish(timestep, lon0, lat0, -1)
  end subroutine movefishBW

  !
  ! ------------------------------------------
  !  

  subroutine movefish(timestep, xtarget, ytarget, direction)

    integer, intent(in) :: timestep
    real, intent(in) :: xtarget
    real, intent(in) :: ytarget
    integer, intent(in) :: direction  ! +1 forw, -1 back

    real :: time

    real, parameter :: pi = 3.1415926
    real, parameter :: detlimit = 0.9
    real, parameter :: detlim2 = detlimit*detlimit
!    real, parameter :: randspeed = 2.0
!    real, parameter :: temp_lim = 1.5



!    logical, parameter :: use_temp = .FALSE.
    logical, parameter :: use_temp = .TRUE.

!    real, parameter :: dfac = 1000.0
!    real, parameter :: dfac = 1.3
!    real, parameter :: dfac = 1.4
!    real, parameter :: add_depth = 30.0
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
    logical :: tempOK, depthOK, atSea, terminate
    integer :: tstep 
    integer :: termfile

    real :: H, sst, err
    type(time_type) :: date
    integer, dimension(6) :: dvec
    integer :: itempOK, idepthOK

! -----------


    ! running time [days]
    time = real(timestep) / outper

    !print *, timestep, time, tag_depth(timestep)
    if (direction < 0)  then
      tstep = simdays*outper + 1 - timestep
      date = stop_time - time
    else
      tstep = timestep
      date = start_time + time
    end if
    call time2vec(dvec, date)
    !month = dvec(2)
    !day   = dvec(3)


    !print *, "time = ", time, tstep


    do n = 1, nFish

      terminate = .FALSE.   

      if (life(n) == 1) then  ! Only consider active fish


       lonfac = cos(Lat(n)*rad)

       ! 
       ! Compute deterministic velocity
       ! the velocity that would take the particle to the
       ! catch position in the remaining time
       !   
       Udet = (xtarget-Lon(n))*lonfac*1852*60/ ((simdays-time)*86400)
       Vdet = (ytarget-Lat(n))*1852*60 / ((simdays-time)*86400)
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


       ! Update positions (OBS, dt er i minutter, forkortes)
       Xnew = Lon(n) + (Udet + Urand)*dt/(1852*lonfac)
       Ynew = Lat(n) + (Vdet + Vrand)*dt/1852

       ! New depth
       call sample_topo(Xnew, Ynew, H)
      
       ! Depth check
       depthOK = .true.
       if ((tag_depth(tstep) > dfac*H + add_depth) .and. (tag_depth(tstep) < 5000)) then
         depthOK = .false.
       end if
       ! Check land
       if (H < 0) then
          atSea = .False.
       else
          atSea = .True.
       end if
       !depthOK = .True.

       if (atSea) then 
         call sample_sst(Xnew, Ynew, dvec(2), dvec(3), sst, err)
         if (tag_temp(tstep) > 500.0) then   ! No SST
           tempOK = .True.
         else if (abs(tag_temp(tstep) - sst) < temp_lim) then  ! SST OK
           tempOK = .True.
         else
            tempOK = .False.
         end if
         !tempOK = .True.

      
         if ( depthOK .and. tempOK) then
           ! New position OK, update
           Lon(n) = Xnew
           Lat(n) = Ynew

         else if (tempOK .and. .not. depthOK) then! New position does not work
           
           ! check old position
           call sample_topo(Lon(n), Lat(n), H)
           if ( tag_depth(tstep) > dfac*H + add_depth ) then 
              terminate = .TRUE.
           end if

         ! Kunne hatt test om temp i gammel posisjon er OK
         ! men temp. varierer langsommerer i rom
         else if (.not. tempOK) then
!New test code
           call sample_sst(Lon(n), Lat(n), dvec(2), dvec(3), sst, err)

           if (abs(tag_temp(tstep) - sst) < temp_lim) then  ! OLD SST OK
             tempOK = .True.
           else
             terminate = .TRUE.
           end if
  

         end if ! (depth OK .and. tempOK

        end if ! (atSea)


        if (terminate) then
          life(n) = 0
          if (direction > 0) then
            termfile = 51
          else
            termfile = 52
          end if
          itempOK = 0
          idepthOK = 0
          if (tempOK) itempOK = 1
          if (depthOK) idepthOK = 1

          !print *,= "H = ", H
           write(termfile,'(I5, I8, 1X, F8.4, F8.4, 1X, F6.2, F6.2, 1X, F7.1, F7.1, 1X, F6.2, I3, I2)')       &
              timestep, n, Lon(n), Lat(n), tag_temp(tstep), sst,                                     &
              tag_depth(tstep), H, sqrt(Udet**2+Vdet**2), idepthOK, itempOK
       end if ! (terminate

 
      end if ! life(n)
        

    end do ! n
    !print *, sum(life)


    ! Count the number of living fish
    !print *, "movefish: finished, number of living fish = ", sum(life)      

  end subroutine movefish




end module position
