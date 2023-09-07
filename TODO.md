# List of issues and todo's

- python vs. python3 (just a worry if some have no python, but do have python3)

- pythana (as package name) is already in use by PyPi:   https://pypi.org/project/pythena/
  so either we change the name, or live with duplicate.   Plenty of those for NEMO already.

  Also: if we allow 'pip install' we need to build a proper wheel, such that athenak gets
  pulled and compiled.


- for output (run) directory, use basename of the problem set, and then run1, run2, ..... inside of those?
  - the startup tool could look inside the problem run directories
  - this closes the loop in running and reviewing old runs
  - could clean up after running?

- GUI peculiarities
  - when browsing, a cancel does not repopulate with the old entry [fixed]
  - killing parent will not kill the children (could be an advanced option,
    because it's nice killing a parent keeps the children alive.
  - resizing and sizing of sub-areas in the GUI (avoid negative space)
  - the delay(ms) in the animator doesn't seem to work well, it's erratic?
    For example I had it taking 5.8sec to do run2, but that was then
    independent of the delay setting , which is now 1..20 ms.
  - in the animation, the picture at T=0 when nothing is loaded yet looks
  - it's easy to accidentally hut the RUN button twice.... athena will run twice. Do
    we need to make a lock file?

- GUI time slider:  it's hard to find a specific time, it would be good if the scrollbar
  and/or click to the left or right of the slider would advance/decrease the slider by
  one unit. 

- Important need for our GUI tags.   We need a new TAGNAME, that clones a keyword value, e.g.
       nx=1   # help for a    #>   SLIDER 0:10:1
       ny=1   # help for b    #>   LINK nx
  or in athena there are blocks, so there it would need to be something like
       ny=1   # help for b    #>   LINK mesh/nx
  this would cause mesh/ny to get the value of mesh/nx.

- GUI ideas
  - when in animation and changing variables, perhaps stick to the time so one can flip at that time
    between e.g. x1v-dens and x1v-velx
  - when in a zoomed mode, remember the new viewing frame and keep that as the animation continues
    or flipping between line and dots, or flipping between variables?

- option to integrate with a running athena [advanced]

- plot1d:  bring up multiple graphs in one plot.  issue will then how to solve the scaling issue

- plot1d:  allow a fixed scaling [the -f flag does that based on first plot, but not always good enough]

- plot2d:  allow option of contour with color, or just contour or just color. this would
  (like in plot1d) give us option to combine two variables and compare them.

- ensure if with id= we can handle different *.tab files. Probably need a new --id flag in plot1d.py for this
  In the end, extracting them from the bin file might be faster.
  
- save animation as mp4? 
  

# Older vis software from athenak

Awkward to use, but here it is:

      ./plot_tab.py  -i run1/tab/LinWave.hydro_w.00000.tab  -n 100 -v dens

and for 2D:

      ./plot_slice.py run2/bin/OrszagTang.mhd_w_bcc.00001.bin dens show --notex

but this only brings up one plot, no animation. our plot2d should do that.

And for hst files

      ./plot_hst.py ./plot_hst.py  -i run2/OrszagTang.mhd.hst  -v dt


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

