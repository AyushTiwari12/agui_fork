#! /usr/bin/env python
#
# new 2023 style python

import sys

file1 = "foo"       # help for input file1          #> IFILE
file2 = "bar"       # help for output file2         #> OFILE
dir3  = "fum"       # help for input dir3           #> IDIR
dir4  =  "baz"      # help for output dir4          #> ODIR
hello = "world"     # help for text entry hello     #> ENTRY
a     = "1"         # help for a, between 0 and 2   #> SCALE       0:2:0.1
b     = "2"         # help for b, pick 1, 2 or 3    #> RADIO       0,1,2
c     = "3,c"       # help for c, check any of 6    #> CHECK       0,1,2,a,b,c

# parse the key=val command line
for _arg in sys.argv[1:]:
    ie = _arg.find('=')
    cmd = '%s="%s"' % (_arg[:ie],_arg[ie+1:])
    exec(cmd)

# print keyword vaues
print('file1',file1)
print('file2',file2)
print('dir3', dir3)
print('dir4', dir4)
print('hello',hello)
print('a',    a)
print('b',    b)
print('c',    c)
