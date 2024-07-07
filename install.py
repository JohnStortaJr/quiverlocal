#!/usr/bin/python3

import sys
import json

infile = open(sys.argv[1])

indata = json.loads(infile.read())

print(indata[sys.argv[2]])

infile.close()