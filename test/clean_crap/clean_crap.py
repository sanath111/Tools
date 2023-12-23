#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import debug
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dryrun",dest='dryrun',action="store_true",help="do a test run without actually removing anything")
parser.add_argument("-a","--all",dest='all',action="store_true",help="remove everything")
args = parser.parse_args()

totalDelete = 0
get_files_cmd = "zpool status -v"
debug.info(get_files_cmd)
process = subprocess.Popen(get_files_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
for line in process.stdout:
    if line:
        file_path = line.strip()
        if os.path.exists(file_path):
            # debug.info (file_path)
            try:
                if (args.dryrun == True):
                    du_cmd = "du -sx \"{0}\" ".format(file_path)
                    debug.info(du_cmd)
                    p = subprocess.Popen(du_cmd,shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    outp = p.communicate()[0].split()[0]
                    totalDelete = totalDelete + float(outp)
                if (args.all == True):
                    remove_file_cmd = "rm -fr \"{0}\" ".format(file_path)
                    debug.info(remove_file_cmd)
                    os.system(remove_file_cmd)
            except:
                debug.info(str(sys.exc_info()))
                
if(totalDelete):
    print("Total to delete in TB - "+ str(((totalDelete/1024)/1024)/1024))

