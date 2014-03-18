#!/usr/bin/python

import sys
import os
from XmlWrapper import XmlWrapper

if len(sys.argv)!=2:
    print "Usage: parsedump.py <datafile>"
    exit()

x = XmlWrapper(sys.argv[1])
x.search()


