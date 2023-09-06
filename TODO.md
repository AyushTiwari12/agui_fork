# List of issues and todo's

- python vs. python3 (just a worry if some have no python, but do have python3)

- better detect what's available (tab, vtk, bin)
  - use the -d flag in plot1.py for directory, it should auto-detect *.tab or tab/*.tab  [done]
  - use vtk reader to grab vtk files (1d and 2d)  [no more vtk, we use bin]
  - use bin reader (can do AMR, where vtk cannot) - check between

- for output (run) directory, use basename of the problem set, and then run1, run2, ..... inside of those?
  - the startup tool could look inside the problem run directories
  - this closes the loop in running and reviewing old runs  

- GUI peculiarities
  - when browsing, a cancel does not repopulate with the old entry
  - killing parent will not kill the children (could be an advanced option,
    because it's nice killing a parent keeps the children alive.

- option to integrate with a running athena

- plot1d:  bring up multiple plots.  issue will be what scaling to use

- plot2d:  allow option of contour with color, or just contour or just color. this would
  (like in plot1d) give us option to combine two variables

  

# Older vis software from athenak

Awkward to use, but here it is:

      ./plot_tab.py  -i tab/LinWave.hydro_w.00000.tab  -n 100 -v dens

and for 2D:

      ./plot_slice.py run2/bin/OrszagTang.mhd_w_bcc.00001.bin dens show --notex

but this only brings up one plot, no animation. our plot2d should do that


# Features

Stating perhaps the obvious, the different GUIs all have their own issues. Here is the current GUI list

                           click_+/-  scroll_+/-    step<1      run?     comments
     tkrun   (test1)       ok         not           ok		 -
     qtrun   (test5)       ok         ok  
     gooey   (test7)       ok         ok            ?            ?
     pyqt    (test1        ok         ok            ok           ok
     pysg-tk (test13)      ok         not           weird        not     step < 1 not working?
     pysg-qt (test13)      ok         ok            ok           not
 


# Python versions

A recent nuisance is the label_props= and radio_props= arguments to
matplotlib.widgets.RadioButtons(), introduces in matplotlib 3.7.0, but
also with a missing module pyparsing. They can usually be solved by
updating your modules in your python, viz.

     pip install --upgrade matplotlib

or

     pip install -r requirements.txt
     
Here's a summary of older versions of python that gave us trouble. Again, the solution
could we be to just update matplotlib.

     distro:                python:    mpl:     comments
     -------------------    -------    -----    --------
     ubuntu 22.04           3.10.12    3.7.2      ok
     ubuntu 22.04           3.10.12    3.5.1      unexpected keyword argument 'label_props'
     anaconda3 2023.07-2    3.11.4     3.7.1      ok
     anaconda3 2023.03-1    3.10.12               No module named 'pyparsing' - broken release?
     anaconda3 2022.10      3.9.13     3.5.2      unexpected keyword argument 'label_props'

where versions can be retrieved as follows:

     python --version
     python -c 'import matplotlib as m; print(m.__version__)'

