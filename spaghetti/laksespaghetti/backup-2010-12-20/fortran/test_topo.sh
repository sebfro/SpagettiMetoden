#export LD_LIBRARY_PATH=/usr/local/lib

gfortran -o test_topo topo.o test_topo.f90 -L/usr/local/lib -lnetcdff -lnetcdf

test_topo


