#! /usr/bin/env python
from re import match
from aparser import parse_generic as parse
from argparse import ArgumentParser
from os import getcwd, remove, mkdir, environ, path
from subprocess import Popen, PIPE
from importlib import import_module
from glob import glob

cwd = getcwd()

# fonts used in the GUI
fstd = ('Helvetica', 10)
fstd_bold = ('Helvetica', 10, 'bold')

sliders = {}
checks = {}

# parse arguments
argparser = ArgumentParser(description='Runs the GUI for configuring an athinput file')
argparser.add_argument('--tk', 
                       action='store_true', 
                       help='uses PYSimpleGUI (tkinter) instead of PySimpleGUIQt', 
                       default=False)
argparser.add_argument('-r', '--run',
                       action='store_true',
                       help='executes the athena command and plots the tab files on run',
                       default=False)
argparser.add_argument('file', help='the athinput file to configure')
argparser.add_argument('-x', '--exe', help='the path to the athena executable')
args = argparser.parse_args()

if args.exe:
    athena = args.exe
else:
    athena = (environ['AGUI'] if 'AGUI' in environ else cwd) + '/athena/bin/athena'

# import a version of PySimpleGUI
# if the selected one doesn't work, try the other
primary = 'PySimpleGUIQt'
backup = 'PySimpleGUI'

using_tk = args.tk

if using_tk:
    primary = 'PySimpleGUI'
    backup = 'PySimpleGUIQt'

try:
    sg = import_module(primary)
except:
    print(f'Falied to import {primary}. Falling back to {backup}')
    using_tk = not using_tk
    sg = import_module(backup)

# removes the trailing zeroes then the dot from a string float x, then returns an int
# utility function used by build_layout
def rm_dot(x):
    if using_tk:
        return float(x)
    # being too precise causes problems, but hopefully this is enough
    s = '%.8g' % float(x)
    dot_pos = s.rfind('.')
    if dot_pos < 0:
        return float(s)
    s = s.replace('.', '')
    return float(s)

#>  IFILE   in=
#>  OFILE   out=
#>  IDIR    indir=
#>  ODIR    odir=
#>  ENTRY   eps=0.01
#>  RADIO   mode=gauss              gauss,newton,leibniz
#>  CHECK   options=mean,sigma      sum,mean,sigma,skewness,kurtosis
#>  SCALE   n=3.141592              0:10:0.01
def build_layout(data, info):
    global cwd
    layout = [[sg.Text('Problem:', font=fstd_bold), 
               sg.Stretch(), 
               sg.Text(info['problem'])]]
    reference = info['reference']
    if reference: # empty strings are falsy
        # in the future, go to the link and get the abstract if possible
        layout.append([sg.Text('Reference:', font=fstd_bold), 
                       sg.Stretch(), 
                       sg.Text(info['reference'])])
    else:
        layout.append([sg.Text('Reference:', font=fstd_bold), 
                       sg.Stretch(), 
                       sg.Text('N/A')])
    layout.extend([[sg.Text('Output directory:', 
                            font=fstd_bold, 
                            tooltip='The directory where the output files will be dumped'),
                        sg.Stretch(),
                        sg.In(size=(25, 0.75), 
                            enable_events=True, 
                            default_text=cwd, 
                            key='output-dir'),
                        sg.FolderBrowse(initial_folder=cwd, size = (6, 1) if using_tk else (75, 25))],
                  [sg.Text('Parameters:', font=fstd_bold)]])
    for k in data:
        e = data[k]
        t = e['gtype']
        # use this if removing the prefix and underscore is desired
        # row = [sg.Text(match('.*_(.+)', k).group(1))] 
        # otherwise use
        row = [sg.Text(f'     {k}', tooltip=e['help'][1:].strip()), 
               sg.Stretch()]
        if t == 'SCALE': # TODO add textbox for custom values
            # getting scale params
            # min:max:increment
            [minimum, maximum, increment] = e['gparams'].split(':')
            # scale = slider
            # build sliders differently depending on whether tk or qt is used
            scaled_increment = rm_dot(increment)
            # if using qt, we need to prepare our own number display since one is not available by default
            factor = round(scaled_increment / float(increment))
            sliders[k] = {
                'key':k+'_display',
                'factor':factor
            }
            #row.append(sg.Text(float(e['value']), key=sliders[k]['key'], background_color=bgstd))
            row.append(sg.InputText(default_text=float(e['value']), key=sliders[k]['key'], justification='right', size=(7, 0.75)))
            # rm_dot only does anything significant if we are using qt
            slider = sg.Slider(
                range=(int(factor * float(minimum)), int(factor * float(maximum))),
                resolution=scaled_increment,
                default_value=int(factor * float(e['value'])),
                enable_events=True,
                key=k,
                orientation='horizontal',
            )
            if using_tk:
                slider.DisableNumericDisplay = True
            row.append(slider)
        elif t == 'ENTRY':
            # entry = text box
            # size of textboxes seem ok by default when right justified
            # however, if changing the size is desired later, then remember that it is a pair not a single value like in the tkinter version
            row.append(sg.Input(
                e['value'], 
                enable_events=True, 
                key=k,
                size=(20, 0.75)
            ))
        elif t == 'RADIO':
            # number of options is not predetermined, so can't use regex
            for o in e['gparams'].split(','):
                row.append(sg.Radio(o, k, key=k+o, default= o == e['value']))
        elif t == 'CHECK':
            values = e['value'].split(',')
            checks[k] = {}
            for o in e['gparams'].split(','):
                # default value?
                key = k+o
                checks[k][key] = o
                row.append(sg.Checkbox(o, key=key, default= o in values))
        elif t == 'IFILE' or t == 'OFILE':
            row.extend([sg.In(size=(25, 0.75), 
                            enable_events=True, 
                            default_text=e['value'], 
                            key=k),
                        sg.FileBrowse(initial_folder=e['value'], size = (6, 1) if using_tk else (75, 25))])
        elif t == 'IDIR' or t == 'ODIR':
            row.extend([sg.In(size=(25, 0.75), 
                            enable_events=True, 
                            default_text=e['value'], 
                            key=k),
                        sg.FolderBrowse(initial_folder=e['value'], size = (6, 1) if using_tk else (75, 25))])
        else:
            print('GUI type %s not implemented' % e['gtype'])
            exit()
        layout.append(row)
    # add buttons to run/quit/help
    layout.extend([[sg.Text()], 
                   [
                        sg.Button('Run', key='run'), 
                        sg.Button('Quit', key='quit'), 
                        sg.Button('Help', key='help')
                    ]])
    return layout

# collects the values from the GUI and builds the athena command
# returns a string
def run(input_file, output_dir, data, values):
    if not path.exists(output_dir) and not display_conf_dir(output_dir):
        return
    # added output2/file_type=tab
    # necessary?
    cmd = f'{athena} -i {input_file} -d {output_dir} output2/file_type=tab '
    for k in data:
        e = data[k]
        t = e['gtype']
        # radio buttons are a special case
        # we have to loop through each button to see which is selected
        if t == 'RADIO':
            for o in e['gparams'].split(','):
                if values[k+o]:
                    cmd += f'{k}={o} '
                    break
        elif not using_tk and e['gtype'] == 'SCALE':
            cmd += '%s=%s ' % (k, values[sliders[k]['key']])
        elif t == 'CHECK' and checks[k]:
            cmd += f'{k}='
            cs = checks[k]
            for ck in cs:
                if values[ck]:
                    cmd += f'{cs[ck]},'
            cmd = cmd[:-1] + ' '
        else:
            cmd += f'{k}={values[k]} '
    # also print it since its easier to copy the text that way
    print(cmd)
    return cmd

# builds and displays a new window containing only the athena command
def display_cmd(s):
    window = sg.Window('Athena Output', 
                        [[sg.Multiline(s, size=(100, round(len(s) / 100)))]], 
                        font=fstd)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

# builds and displays a new window with a progress bar tracking the process of athena's output
def display_pbar(s, time):
    window = sg.Window('Loading Plot', 
                        [[sg.ProgressBar(100, orientation='h', size=(20, 20), key='pbar')]], 
                        font=fstd)
    p = Popen(s.split(), stdout=PIPE)
    while True:
        event, _ = window.Read(timeout=0)
        line = p.stdout.readline()
        if event == sg.WIN_CLOSED or not line:
            break
        m = match('.*cycle=.* time=(.*) dt=.*', str(line))
        if m:
            window['pbar'].UpdateBar(100 * float(m.group(1)) / time, 100)
    window.close()

# builds and displays a new window containing the help information
def display_help(data):
    layout = [[ sg.Text('Output directory:', 
                        font=fstd_bold), 
                sg.Stretch(),
                sg.Text('The directory where the output files will be dumped')]]
    for k in data:
        layout.append([sg.Text(k + ':', font=fstd_bold), 
                       sg.Stretch(),
                       sg.Text(data[k]['help'][1:].strip())])
    window = sg.Window('Help', layout, font=fstd)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

def display_conf_dir(dir_path):
    layout = [[sg.Text(f'Directory {dir_path} does not exist. Create it?')], 
              [sg.Button('Yes', key='yes'), sg.Button('No', key='no')]]
    window = sg.Window('Directory Not Found', layout, font=fstd)
    while True:
        event, _ = window.read()
        if event == 'no':
            break
        elif event == 'yes':
            mkdir(dir_path)
            break
    window.close()
    return event == 'yes'

# parse the input files
data, info, type = parse(args.file)

sg.theme('Default1')

sg.SetOptions(slider_border_width=0)

# start building gui
inner_layout = build_layout(data, info)
# pysgqt elements seem to be smaller than their tkinter counterparts, so it might be better to reduce the width scaling
scale_factor = 27
if using_tk:
    scale_factor = 33
win_size = (550, len(inner_layout) * scale_factor)
#layout = [[sg.Column(inner_layout, size=win_size, scrollable=False, background_color=bgstd)]]
# only allow verticle scroll for the tk version, otherwise a horizontal scroll bar will show up
#if using_tk:
#    layout[0][0].VerticalScrollOnly = True
# create the main window '#777777'
# already resizable by default?
import PySimpleGUIQt as sg
window = sg.Window('pysg_run', inner_layout, size=win_size, font=fstd, resizable=True, grab_anywhere=True)
# primary event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'quit':
        break
    elif event == 'run':
        cmd = run(args.file, values['output-dir'], data, values)
        if cmd and args.run:
            if not path.exists(athena):
                print('Athena not found\nExiting')
                exit()
            # open the plot in a subprocess
            # remove the forward slash at the end if there is one
            odir = values['output-dir']
            if odir[-1] == '/':
                odir = odir[:-1]
            # remove the hst file since it always gets appended to
            # intentional?
            h = glob(odir + '/*.hst')
            if len(h) > 0:
                remove(h[0])
            # will the tlim variable always be like this?
            display_pbar(cmd, values['time/tlim'])
            print(info)
            Popen(['python', 'plot1d.py', '-d', values['output-dir'], '-n', info['problem']])
            Popen(['python', 'plot1d.py', '-d', values['output-dir'], '--hst', '-n', info['problem'] + ' history'])
        elif cmd:
            display_cmd(cmd)
    elif event == 'help':
        display_help(data)
    # update slider displays if using qt
    elif event in sliders:
        slider_info = sliders[event]
        window[slider_info['key']].update(values[event] / slider_info['factor'])

window.close()
