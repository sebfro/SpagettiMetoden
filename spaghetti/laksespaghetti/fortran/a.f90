program test

use time_module

integer :: m, d
type(time_type) :: date, date0
integer, dimension(4) :: a
integer, dimension(1) :: l

  m = 10
  d = 22
  

  date = (/ 2008, m, d, 0, 0, 0 /)
  date0 = (/ 2008, 1, 1, 0, 0, 0 /)
  print *, int(date-date0)

  print *, int(2.7), int(-2.7)

  a = (/ 1, 8, 15, 22 /)
  l = minloc(abs(a-16))
  print *, l

  print *, date
  print *, str(date + 24)


end program test


  

  
