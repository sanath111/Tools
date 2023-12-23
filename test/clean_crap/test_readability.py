#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import debug
import argparse


def is_readable(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.read(1)
        return True
    except IOError:
        return False

dir_path = "/backup-pool1/crap/"
# totalDelete = 0

try:
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            file = os.path.join(path, name)
            # print(file)

            if is_readable(file):
                # print("File is readable")
                pass
            else:
                # print("File is not readable")
                print(file)
                # du_cmd = "du -sx \"{0}\" ".format(file)
                # print (du_cmd)
                # p = subprocess.Popen(du_cmd,shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                # outp = p.communicate()[0].split()[0]
                # totalDelete = totalDelete + float(outp)
except:
    print(str(sys.exc_info()))

# if(totalDelete):
#     print("Total to delete in TB - "+ str(((totalDelete/1024)/1024)/1024))
