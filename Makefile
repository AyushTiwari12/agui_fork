# See the INSTALL.md notes on how to use this Makefile

#
SHELL = /bin/bash

#
TIME = /usr/bin/time

# use python3 or anaconda3
PYTHON = anaconda3

# git directories we should have here

GIT_DIRS = athena athenak

# URLs that we'll need

URL1  = https://github.com/PrincetonUniversity/athena
URL2  = https://gitlab.com/theias/hpc/jmstone/athena-parthenon/athenak
URL3  = https://github.com/teuben/nemo

# the ATHENA executable

ATHENA = athenak/build/src/athena

.PHONY:  help install build


install:
	@echo "The installation has a few manual steps:"

help:
## help:      This Help
help : Makefile
	@sed -n 's/^##//p' $<


## git:       Get all git repos for this install
git:  $(GIT_DIRS)
	@echo Last git: `date` >> git.log

## pull:      Update all git repos
pull:
	@echo -n "lmtoy: "; git pull
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git pull); done
	@echo Last pull: `date` >> git.log

status:
	@echo -n "lmtoy: "; git status -uno
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git status -uno); done

branch:
	@echo -n "lmtoy: "; git branch --show-current
	-@for dir in $(GIT_DIRS); do\
	(echo -n "$$dir: " ;cd $$dir; git branch --show-current); done


athena:
	git clone $(URL1)

athenak:
	git clone --recursive $(URL2)

nemo:
	git clone $(URL3)

## build:     build athenak
build:	athenak
	(mkdir -p athenak/build; cd athenak/build; cmake ..; make -j)

build_nemo:	nemo
	(cd nemo; ./configure ; make build check bench5)

# a few sample runs

run1:
	$(ATHENA) -i athenak/inputs/tests/linear_wave_hydro.athinput -d run1
	# -> LinWave.hydro_w.00000.tab

run2:
	$(ATHENA) -i athenak/inputs/tests/advect_hyd.athinput        -d run2
	# -> Advect.hydro_u.00000.tab

run3:
	$(ATHENA) -i athenak/inputs/tests/advect_mhd.athinput        -d run3
	#  -> Advect.mhd_u.00000.tab

run4:
	$(ATHENA) -i athenak/inputs/tests/hohlraum_1d.athinput       -d run4
	#  -> hohlraum_1d.rad_coord.00000.tab  

run5:
	$(ATHENA) -i athenak/inputs/tests/rad_linwave.athinput       -d run5
	# -> rad_linwave.hydro_w.*.tab
	# -> rad_linwave.rad_coord.*.tab

run6:
	$(ATHENA) -i athenak/inputs/hydro/sod.athinput               -d run6
	# -> Sod.hydro_w.00000.tab
	#   base=run6/tab/Sod  xcol=3 ycol=4
	#   base=run6/tab/Sod  xcol=3 ycol=5
	#   base=run6/tab/Sod  xcol=3 ycol=6

run7:
	$(ATHENA) -i athenak/inputs/hydro/shu_osher.athinput         -d run7
	#   ERROR

run8:
	$(ATHENA) -i athenak/inputs/hydro/viscosity.athinput         -d run8
	#   ViscTest.hydro_w.00000.tab 
	#   base=run8/tab/ViscTest xcol=3 ycol=6