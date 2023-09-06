#! /usr/bin/env python
from tempfile import mkstemp
from os import remove, getcwd, environ
from subprocess import Popen
from aparser import parse_generic as parse
from argparse import ArgumentParser

def rm_dot(x):
    # being too precise causes problems, but hopefully this is enough
    s = '%.8g' % float(x)
    dot_pos = s.rfind('.')
    if dot_pos < 0:
        return int(s)
    s = s.replace('.', '')
    return int(s)

cwd = getcwd()

options = {}

# parsing arguments
argparser = ArgumentParser(description='Creates a GUI script, then runs it. The GUI will allow for configuring the provided athinput file')
argparser.add_argument('file', help='the athinput file to configure')
args = argparser.parse_args()

# parsing input file
data, info, type = parse(args.file)
name = info['problem']
reference = info['reference']
if not reference: # empty string is falsy
    reference = 'N/A'

# make temp file
_, path = mkstemp(prefix='gooey', suffix='.py')

file = open(path, 'w')

# write a the script that generates the gui
file.write(f'from gooey import Gooey, GooeyParser\n\
@Gooey(program_name=\'gooey_run2\')\n\
def main():\n\
\tparser = GooeyParser(description=\'Problem: {name}\\nReference: {reference}\')\n\
\tparser.add_argument(\'--output_dir\', help=\'The directory where the output files will be dumped\', metavar=\'output directory\', default=\'{cwd}\', widget=\'DirChooser\')\n')

#>  IFILE   in=
#>  OFILE   out=
#>  IDIR    indir=
#>  ODIR    odir=
#>  ENTRY   eps=0.01
#>  RADIO   mode=gauss              gauss,newton,leibniz
#>  CHECK   options=mean,sigma      sum,mean,sigma,skewness,kurtosis
#>  SCALE   n=3.141592              0:10:0.01
i = 0
for k in data:
    e = data[k]
    t = e['gtype']
    if t == 'ENTRY':
        # entry = text box
        file.write('\tparser.add_argument(\'--%s\', help=\'%s\', metavar=\'%s\', default=\'%s\')\n' % (k, e['help'][1:].strip(), k, e['value']))
    elif t == 'RADIO': # currently dropdown menus and not radio buttons, radio buttons seem to be a massive pain
        # number of options is not predetermined, so can't use regex
        options = e['gparams'].split(',')
        # create string list
        c = '['
        for o in options:
            c += f'\'{o}\',' # not wrapping o in quotes causes an error
        c += ']'
        file.write('\tparser.add_argument(\'--%s\', help=\'%s\', metavar=\'%s\', choices=%s, default=\'%s\')\n' % (k, e['help'][1:].strip(), k, c, e['value']))
        '''file.write('\tgroup = parser.add_argument_group()\n')
        file.write('\trgroup = group.add_mutually_exclusive_group()\n')
        for o in options:
            if o in options:
                
            file.write('\trgroup.add_argument(\'--%s\', action=\'store_true\')\n' % ('option', i))'''
    elif t == 'SCALE':
        [minimum, maximum, increment] = e['gparams'].split(':')
        # scale = slider
        # build sliders differently depending on whether tk or qt is used
        scaled_default = rm_dot(e['value'])
        scale = round(scaled_default / float(e['value']))
        file.write('\tparser.add_argument(\'--%s\', help=\'%s\\nscale: %s\', metavar=\'%s\', default=%s, widget=\'Slider\', gooey_options={\'min\':%s, \'max\':%s, \'increment\':%s})\n' 
                   % (k, e['help'][1:].strip(), 1 / scale, k, scaled_default, rm_dot(minimum), rm_dot(maximum), rm_dot(increment)))
    else:
        print('GUI type %s not implemented' & e['gtype'])
        exit()

p = environ['AGUI'] if 'AGUI' in environ else cwd

file.write(f'\targs = parser.parse_args()\n\
\ts = \'{p}/athena/bin/athena -i {args.file} -d %s \' % args.output_dir\n')

for k in data:
    e = data[k]
    file.write(f'\ts += \'{k}=\' + getattr(args, \'{k}\') + \' \'\n')

file.write('\tprint(s)\nmain()')

file.close()

# run gui file in a subprocess
p = Popen(['python', path])
# wait for subprocess to finish before deleting the temp file
p.wait()

# remove temp file
remove(path)