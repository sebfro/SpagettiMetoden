PROG = spaghetti

SRC  = spaghetti.f90 topo.f90 position.f90 time_module.f90 setup.f90   \
       output.f90 tagdata.f90 sst.f90

# Fortran compiler
FC = gfortran

FFLAGS = -O
#FFLAGS = -fbounds-check -ftrace=frame -Wall

OBJ  = $(SRC:.f90=.o) 

# NetCDF
INC_NC = -I/usr/local/include

LIB_NC = -L/usr/local/lib -lnetcdff -lnetcdf
#LIB_NC = -L/usr/local/lib -lnetcdff -lnetcdf -lhdf5_hl -lhdf5
LIB = $(LIB_NC)

####

all: $(PROG)

.SUFFIXES:
.SUFFIXES: .f90 .o

.f90.o: 
	$(FC) -c $(FFLAGS) $(INC_NC) $<

$(PROG): $(OBJ)
	 $(FC) $(FFLAGS) -o $(PROG) $(OBJ) $(LIB)



#### YMSE ########

# Lager TAGS-fil
tags: TAGS
TAGS: $(SRC) 
	etags  $(SRC)


# Samler koden
tar: $(PROG).tar
$(PROG).tar: $(SRC) Makefile $(MISC)
	tar cf $(PROG).tar $(SRC) Makefile $(MISC)

tgz: $(PROG).tar.gz
$(PROG).tar.gz:	$(PROG).tar
	gzip -f $(PROG).tar

# Opprydding
clean:
	rm -f $(OBJ) $(PROG)

love:
	@echo "not war"

# Dependencies
time_module.o : 
grid.o        :
output.o      : setup.o position.o
setup.o       : time_module.o 
tagdata.o     : setup.o
sst.o         : time_module.o
position.o    : topo.o setup.o sst.o tagdata.o
spaghetti.o   : topo.o position.o setup.o output.o tagdata.o sst.o
