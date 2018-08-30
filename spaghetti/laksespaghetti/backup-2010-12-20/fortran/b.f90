program b

  include '/usr/local/include/netcdf.inc'

  integer :: status, ncid

  status = nf_open('../input/oisst_2008.nc', NF_NOWRITE, ncid)
  print *, status

end program b
