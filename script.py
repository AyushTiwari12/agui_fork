#! /usr/bin/env python
from re import match
from aparser import parse_generic as parse
import json

file = open('inputs.txt', 'r')

line = file.readline()

dict = {}

while line:
    m = match('./athena/inputs/[^/]+/athinput+', line)
    if m:
        #print(line)
        clean_line = line.split()[0]
        _, info, _ = parse(clean_line)
        try:
            dict[info['problem']] = clean_line
            #print(info['problem'])
        except:
            dict[match('.+athinput\.(.+)', clean_line).group(1)] = clean_line
            #print(match('.+athinput\.(.+)', clean_line).group(1))
        #print()

    line = file.readline()

# Serializing json
json_object = json.dumps(dict, indent=3)
 
# Writing to sample.json
with open("athena_problems.json", "w") as outfile:
    outfile.write(json_object)

file.close()