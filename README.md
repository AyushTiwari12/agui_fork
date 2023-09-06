# Developing an Athena GUI (AGUI)

This is the development verson of **agui**, not to be confused with
the public version **pyThena** that only works with "*Athena-miniK*" that
was extracted from this code base during the Aug 21-25 week at IAS.

Here show some examples of executing **athena** using a dynamic GUI.
nIn theory this could apply to any of the
[Athena](https://www.athena-astro.app/) family (athena [AC], athena++
[AX], or athenak [AK]). It is easiest to work with **athenak**, since
all the problems are compiled into one executable. We cover some
examples of athena++ below as well, since at the moment athenak is not
yet public. For good historic measure, classic athenaC is also
available.


Related and inspired by is NEMO's **tkrun** and **run** frontends,
but we aim to use python based software here. The GUI directive we
are proposing are an updated version of the one that was used in
[tkrun](https://teuben.github.io/nemo/man_html/tkrun.l.html)

## Quick Start Guide

This **agui** is a convenience repo that can contain all dependant
repos (athenac, athena, athenak and nemo). First get **agui**:

      git clone https://github.com/teuben/agui
      cd agui

after which any of the components can be built, or pick the one you want to focus on:

      make build_athenac
      make build_athena
      make build_athenak
      make build_nemo
      make build_python

For some systems you may need to install additional software, which are assembled
in the **requirement** files, e.g.

### for Ubuntu Linux:

      sudo apt install $(grep -v ^# requirements.apt)

### for Redhat style Linux:

      sudo dnf install $(grep -v ^# requirements.dnf)

### for a Mac with brew:

      brew install $(grep -v ^# requirements.brew)

### for python (which should apply to any)

      pip install -r requirements.txt

How the user sets up python could be covered in a separate document. We do mention
the **build_python** target listed before, which sets up a personal anaconda3 tree
in this directory, but needs an additional

      source anaconda3/python_start.sh

to be activated in your shell.


### Method-1:  using pyqt (the preferred method)

Using native Qt is probably our preferred method of using the GUI, viz.

      ./pyqt_menu.py

should show a  GUI where to select an athinput file. Everything should guide itself.

### Method-2:  using pysg

pySimpleGui (pysg) is an alternative method where you can pick the GUI from "qt" or "tkinter",
and actually two more we didn't play with. Here you would start with

      ./pysq_menu.py

and again, since it's a GUI, things should guide itself.

## Detailed Example (athenak) 

Using **athenak** is preferred, as it has *all* problems compiled
into one executable. Examples  using **athena++** can be found below.

First, an example how to compile and run the code

```bash
     git clone --recursive https://gitlab.com/theias/hpc/jmstone/athena-parthenon/athenak
     mkdir athenak/build
     cd athenak/build
     cmake ..
     make -j
```

or if you're lazy, use the Makefile in this agui directory:

```bash
     make build
```     

this compilation takes a bit longer than athena++,
mostly because the kokkos library has to be compiled first.   The binary is
now in **athenak/build/src/athena**.

```text
build/src/athena -i inputs/tests/linear_wave_hydro.athinput -d run1
 -> LinWave.hydro_w.00000.tab

build/src/athena -i inputs/tests/advect_hyd.athinput        -d run2
 -> Advect.hydro_u.00000.tab
 
build/src/athena -i inputs/tests/advect_mhd.athinput        -d run3
  -> Advect.mhd_u.00000.tab

build/src/athena -i inputs/tests/hohlraum_1d.athinput       -d run4
  -> hohlraum_1d.rad_coord.00000.tab  

build/src/athena -i inputs/tests/rad_linwave.athinput       -d run5
 -> rad_linwave.hydro_w.*.tab
 -> rad_linwave.rad_coord.*.tab

build/src/athena -i inputs/hydro/sod.athinput               -d run6
 -> Sod.hydro_w.00000.tab
   base=run6/tab/Sod  xcol=3 ycol=4
   base=run6/tab/Sod  xcol=3 ycol=5
   base=run6/tab/Sod  xcol=3 ycol=6

build/src/athena -i inputs/hydro/shu_osher.athinput         -d run7
   ERROR

build/src/athena -i inputs/hydro/viscosity.athinput         -d run8
   ViscTest.hydro_w.00000.tab 
   base=run8/tab/ViscTest xcol=3 ycol=6
```


## Detailed Example (athena++) using Linear Wave

First we grab and compile the code for the linear wave problem

```bash
     git clone https://github.com/PrincetonUniversity/athena
     cd athena
     ./configure.py --prob linear_wave
     make clean
     make -j
```     

Compiling the code takes the most time, but on a typical laptop well under 30 seconds.

After this we can run it

```bash
     bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d run1
```          

but the default output from that **athinput** file is the **vtk** data format, which for this GUI demo would
be too complex to parse. TBD. For now we switch to the ascii table format, viz.

```bash
     bin/athena  -i inputs/hydro/athinput.linear_wave1d  -d run2 output2/file_type=tab
```

which also shows how the GUI will have to deal with command line parameters beyond the -i and -d options.

### Animations

First example is NEMO biased, effectively quickly plotting all **tab** files using tabplot. Noting that the second row
in each table shows the columns names:


```text
# Athena++ data at time=0.000000e+00  cycle=0  variables=prim 
# i       x1v         rho          press          vel1         vel2         vel3     
```

this would be an animation of *x1v* vs. *vel1*

```bash
     for f in LinWave*.tab; do
        tabplot $f xcol=2 ycol=5
     done
```

or using our sample script

```bash
     ../../animate1 xcol=x1v ycol=vel1
```

if **tkrun** is enabled, use

```bash
     tkrun ../../animate1
```

but this may be broken by now, at least the names of the columns differ  between athena++ and athenak


### Statistics

The history (hst) keeps track of a number of variables of which we can obtain the statistics (agui/show_stats)

```text
#col    [1]          [2]         [3]    [4]          [5]     [6]     [7]         [8]     [9]    [10]      [11]
#name   time         dt          mass   1-mom        2-mom   3-mom   1-KE        2-KE    3-KE    tot-E     max-v2

npt:    501          501         501    501          501     501     501         501     501     501       501
min:    0            1.31217e-05 1      -3.14329e-22 0       0       2.49497e-13 0       0       0.9       0
max:    5            0.003125    1      3.19912e-22  0       0       2.5e-13     0       0       0.9       0
sum:    1253.43      1.56251     501    -1.56725e-20 0       0       1.25127e-10 0       0       450.9     0
mean:   2.50186      0.00311879  1      -3.12825e-23 0       0       2.49754e-13 0       0       0.9       0
disp:   1.44625      0.00013889  0      8.61373e-23  0       0       1.46346e-16 0       0       0         0
skew:   -4.15046e-05 -22.316     0      0.0211432    0       0       -0.0439997  0       0       0         0
kurt:   -1.20002     496.002     0      0.579502     0       0       -1.23003    0       0       0         0
min:    -1.72989     -22.3607    -nan   -3.28599     -nan    -nan    -1.75681    -nan    -nan    inf       -nan
max:    1.72732      0.0447214   -nan   4.07715      -nan    -nan    1.68025     -nan    -nan    inf       -nan
median: 2.50312      0.003125    1      -3.21566e-23 0       0       2.49757e-13 0       0       0.9       0
```

# TKRUN format

The old style V1 tkrun format separated the parameter setting from the GUI specification:

       #>  RADIO   mode=gauss              gauss,newton,leibniz

but in the new style V2 will allow us to mix the GUI specifications with
the (language dependent) key=val construct that gives it
a default value, e.g.

bash:
 
       mode=gauss         # specify the integration method      #> RADIO   gauss,newton,leibniz

csh:

       set mode = gauss   # specify the integration method      #> RADIO   gauss,newton,leibniz
       
python:

       mode="gauss"       # specify the integration method      #> RADIO   gauss,newton,leibniz

athinput:

       <integration>
       mode = gauss       # specify the integration method      #> RADIO   gauss,newton,leibniz


but will still leave open the option to build an executionar.


# How to run AGUI

This is how we envision running **agui**:

```text
     agui [-i athinput] [-x athena] [-s scriptfile]

     -i     optional athinput file. If not provided, a filebrowser will let you search for and select one
            Default:  athinput
     -x     name (and or location) of the athena executable to use.
            Default: athena
     -s     name of a script file where run commands will be appended to. This can act like a logfile
            Default: agui.log
```

This will bring up a succession of 3 GUI's:

1.  The (optional) athinput file selector. Here the defaults of all parameters are given

2.  Setting parameters for the run
    1. The "-d" run directory
    2. parameters parsed from the athinput file (with or without the "#> GUI" specifications

    The user can then run the simulation. This should probably detach from this GUI, maybe
    bring up a progress bar in a new window, which will then morph into the results browser(s)
    as described in the next two steps:

3. History (.hst) file browser.  This is a file that as function of simulation time has stored a number
   of variables. This GUI will allow you to plot any column vs. any other column using a standard
   matplotlib windows embedded in the GUI. This will otherwise be a static plot, as time is one of
   the columns in the history table.

3. Results (1D: .tab) browser. This browser is similar to the history file browser, except results
   are available for each selected dump time. An animation button will allow you to move through
   time, as well as select two variables from the results table.

This will of course fine for 1D problems, for 2D problems the last GUI ("plot1D") will be a "plot2D"
widget that shows an image with a color-bar instead of a 1D plot. This has not been implemented yet.
Also to be determined is the allowed format?  FITS and HDF ?

# References

1. athena++ GRMHD code and adaptive mesh refinement (AMR) framework - https://www.athena-astro.app/

1. pyro: a python hydro code - https://github.com/python-hydro/pyro2 


# History

* summer 2023:  UMD students Anh Hoang Cao and Kylie Gong coding pyqt, gooey and pysimplegui examples (test1..9)
