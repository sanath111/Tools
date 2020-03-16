#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os
import sys
import argparse

parser = argparse.ArgumentParser(description="Utility to set wacom tablet work display")
parser.add_argument('display', metavar='N', type=str, help='display number: 0 or 1')
parser.add_argument("-r","--rotate",dest='rotate',help='rotae display.values= cw, ccw, half, none')
args = parser.parse_args()

# os.system("xsetwacom --list devices")
a = os.popen("xsetwacom --list devices").read()
# b = a.replace('\t','')
c = a.split(' ')
# d = c.index('\tid:')
d = [i for i, x in enumerate(c) if x == "\tid:"]

# e = " ".join([c[i] for i in range(0,d)])

if not a:
    print ("no wacom device detected")
    sys.exit(0)

else:
    print(a)
    # print(b)
    # print(c)
    # print(d)
    # print(e)
    # print(f)
    for n in d:
        e = c[int(n)+1].split('\t')
        f = e[0]

        cmd = "xsetwacom --set " + "\"" + f + "\"" + " MapToOutput HEAD-"+args.display
        print(cmd)
        os.system(cmd)
        if args.rotate:
            cmd1 = "xsetwacom --set " + "\"" + f + "\"" + " Rotate " + args.rotate
            print(cmd1)
            os.system(cmd1)
