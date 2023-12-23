#!/usr/bin/python2
# *-* coding: utf-8 *-*

import os
import sys

projs = os.listdir("/blueprod/STOR2/stor2/")
projs.sort()

du_cmd = "du -sch "

for p in projs:
    if "chotiChethna" in p:
        print(p)
        path = "/blueprod/STOR2/stor2/{0}/share/publicityAssets".format(p)
        print(path)
        rm_cmd = "rm -fr "+path+os.sep+"*"
        print(rm_cmd)
        # os.system(rm_cmd)

        du_cmd = du_cmd + " " + path
print(du_cmd)
os.system(du_cmd)
