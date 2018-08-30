module output
!
! Module for output of particle distributions to netCDF files
!

!use topography
use setup, only: forward_outfile_name, backward_outfile_name
use position, only: nFish, Lon, Lat, life
use netcdf

  implicit none

  integer, private :: FWid, BWid
  integer, private :: time_id, x_id, y_id, life_id

contains

! --- Wrappers for FW and BW files

subroutine init_FW_output
  call init_output(forward_outfile_name, FWid)
end subroutine init_FW_output

subroutine init_BW_output
  call init_output(backward_outfile_name, BWid)
end subroutine init_BW_output

subroutine save_FW_output(daynr)
  integer, intent(in) :: daynr
  call save_output(FWid, daynr)
end subroutine save_FW_output

subroutine save_BW_output(daynr)
  integer, intent(in) :: daynr
  call save_output(BWid, daynr)
end subroutine save_BW_output

subroutine close_FW_output
  call close_output(FWid)
end subroutine close_FW_output

subroutine close_BW_output
  call close_output(BWid)
end subroutine close_BW_output

! -----------------------------

subroutine init_output(fname, ncid)
  character(len=*), intent(in) :: fname
  integer, intent(out) :: ncid

  integer :: status
  integer :: dim_time, dim_fish

! Open the file

  status = nf90_create(fname, NF90_clobber, ncid)
  call check_err(status)

! Global attributes 

  status = nf90_put_att(ncid, NF90_GLOBAL, 'type',        & 
           'Forward spaghetti output file')
  call check_err(status)

! Dimensions
  status = nf90_def_dim(ncid, 'time', NF90_UNLIMITED, dim_time)
  call check_err(status)
  
  status = nf90_def_dim(ncid, 'fish', nFish, dim_fish)
  call check_err(status)

! Variables

  status = nf90_def_var(ncid, 'time', NF90_FLOAT, (/ dim_time /), time_id)
  call check_err(status)
  status = nf90_def_var(ncid, 'X', NF90_FLOAT, (/ dim_fish, dim_time /), x_id)
  call check_err(status)
  status = nf90_def_var(ncid, 'Y', NF90_FLOAT, (/ dim_fish, dim_time /), y_id)
  call check_err(status)
  status = nf90_def_var(ncid, 'life', NF90_INT,              &
                        (/ dim_fish, dim_time /), life_id)
  call check_err(status)

! Attributes
  status = nf90_put_att(ncid, time_id, "long_name", 'simulation time')
  call check_err(status)
  status = nf90_put_att(ncid, time_id, "units", 'days')
  call check_err(status)

! ---


  status = nf90_put_att(ncid, x_id, "long_name", "Longitude")
  call check_err(status)
  status = nf90_put_att(ncid, x_id, "units", "degrees east")
  call check_err(status)

! ---


  status = nf90_put_att(ncid, y_id, "long_name", "Latitude")
  call check_err(status)
  status = nf90_put_att(ncid, y_id, "units", "degrees north")
  call check_err(status)

! ---

  
  status = nf90_put_att(ncid, life_id, "long_name",    & 
                        "Flag for active trajectory")
  call check_err(status)


  ! ----------------------------------------
  ! Leave NetCDF definition mode
  ! ----------------------------------------
  status = nf90_enddef(ncid)
  call check_err(status)

end subroutine init_output

!
! ================================================
!
  subroutine save_output(ncid, daynr)

    integer, intent(in) :: ncid
    integer, intent(in) :: daynr

    integer :: status
    !integer :: n

    status = nf90_put_var(ncid, time_id, daynr, start = (/ daynr+1 /))
    call check_err(status)
    status = nf90_put_var(ncid, x_id, Lon, start = (/ 1, daynr+1 /))
    call check_err(status)
    status = nf90_put_var(ncid, y_id, Lat, start = (/ 1, daynr+1 /))
    call check_err(status)
    status = nf90_put_var(ncid, life_id, life, start = (/ 1, daynr+1 /))

  end subroutine save_output

!
! ==================================================
!
  subroutine close_output(ncid)
    integer, intent(in) :: ncid
    integer :: status
    status = nf90_close(ncid)
    call check_err(status)
  end subroutine close_output

!
! ==============================================
!
  subroutine check_err(iret)
!
!   NetCDF file operation error handling
!
    implicit none

    integer, intent(in) :: iret
 
    if (iret .ne. NF90_NOERR) then
      print *, nf90_strerror(iret)
      stop
    endif

  end subroutine check_err





end module output
