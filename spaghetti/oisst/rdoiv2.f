      program rdoiv2 
c  read OIv2 SST file and land mask and print selected values.

c  sst   - sea surface temperature array (deg C)
c  err   - normalized error variance
c  ice   - ice concentration array (%)  (0-100,   >100 = land or coast)
c  iyrst - year of start date of analysis
c  imst  - month of start date of analysis
c  idst  - day of start date of analysis
c  iyrnd - year of end date of analysis
c  imnd  - month of end date of analysis
c  idnd  - day of end date of analysis
c  ndays - number of days in analysis (start date thru enddate)
c  index - analysis version for reference
c  xlon  - longitude of center of grid square
c  xlat  - latitude of center of grid square
c  tagls - land/sea tag array (0=land, 1=water)

c  NOTES:  
c   - land values for sst do not necessarily coincide with land values 
c       from ice analysis
c   - recl definition for the direct access open depends on the compiler
c     (number of 4-byte words OR number of bytes).
c     Choose the appropiate parameter statement for krecl
c  

      implicit none
c
      integer krecl
c      parameter(krecl=360*180)        ! number of 4-byte words
      parameter(krecl=360*180*4)      ! number of bytes

      real*4 sst(360,180),err(360,180),xlon,xlat
      integer*4 iyrst,imst,idst,iyrnd,imnd,idnd,ndays,index,i,j
      integer*4 ice(360,180)
      character*1 cice(360,180)
      real*4 tagls(360,180)

      open (24,file='lstags.onedeg.dat',form='unformatted',
     1   access='direct',recl=krecl)

c
c     Read in land sea tags (1 for ocean; 0 for land)
c
      read (24,rec=1) tagls


c   date string used in filename represents the  mid-week date
c            weeks prior 1990 are centered on Sunday 
c            weeks in 1990 and onward are centered on Wednesday

      open(11,file='oisst.19930804',form='unformatted')

      read(11) iyrst,imst,idst,iyrnd,imnd,idnd,ndays,index
      read(11) ((sst(i,j),i=1,360),j=1,180)
      read(11) ((err(i,j),i=1,360),j=1,180)
      read(11) ((cice(i,j),i=1,360),j=1,180)

      print '(a,i4,1x,i2,1x,i2)', 'start date: ',iyrst,imst,idst
      print '(a,i4,1x,i2,1x,i2)', '  end date: ',iyrnd, imnd,idnd
      print             '(a,i2)', '  num days: ',ndays
      print          '(a,i10,/)', '     index: ',index
  
c ...choosing one longitude
      i = 181
c  ... determine longitude of middle of grid boxes with this index
      xlon = float(i) - 0.5  

c  .... loop thru several latitudes (decrementing to run North->South)
      do j = 180,150,-1  
        ice(i,j)=ichar(cice(i,j))
        xlat = float(j) - 90.5
        print 125, 'lon = ',xlon,'lat = ',xlat,'sst = ',sst(i,j),
     1     'nev = ',err(i,j),'ice = ',ice(i,j),'tagls= ',tagls(i,j)
  125   format(a,f5.1,4x,a,f5.1,4x,a,f5.1,4x,a,f5.3,3x,a,i3,3x,a,f2.0)
      enddo

      stop
      end
