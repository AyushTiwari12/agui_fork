#! /usr/bin/env python
import sys
from re import match
from aparser import parse_generic as parse
import json

ofile ="athena_problems.json"

if len(sys.argv) > 1:
    ifile = sys.argv[1]
else:
    ifile = 'inputs.txt'
    
file = open(ifile, 'r')
print("input: ",ifile)

line = file.readline()

dict = {}
athena = last = None
while line:
    m = match('./([^/]+)/', line)
    if m:
        info = None
        last = athena
        athena = m.group(1)
        clean_line = line.split()[0]
        problem = clean_line.split('/')[-1].split('.')[0 if athena == 'athenak' else 1]
        try:
            _, info, _ = parse(clean_line, True)
        except:
            pass
        if athena != last:
            dict[athena] = {}
        try:
            dict[athena][info['problem']] = clean_line
        except:
            dict[athena][problem] = clean_line
    line = file.readline()

# Serializing json
json_object = json.dumps(dict, indent=3)
 
# Writing to sample.json
with open(ofile, "w") as outfile:
    outfile.write(json_object)

file.close()
print("output:",ofile)
