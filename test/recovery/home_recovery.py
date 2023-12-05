#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import debug

users = ['bnag']

try:
    for user in users:
        copy_cmd = "rsync -avzHXWhPs --zc=lz4 --exclude='backup*' --exclude='*cache*' kryptos@stor2:/dell1-pool/stor3/home/"+user+" /dell2-pool/stor7/home/"
        debug.info(copy_cmd)
        process = subprocess.Popen(copy_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            if line:
                debug.info (line)
except:
    print(str(sys.exc_info()))
