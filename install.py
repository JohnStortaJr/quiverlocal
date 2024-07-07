#!/usr/bin/python3

import json

infile = open('localtest01.json')

indata = json.loads(infile.read())

for i in indata:
    print(i + " -> " + indata[i])

infile.close()