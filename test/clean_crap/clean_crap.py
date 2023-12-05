#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import debug

get_files_cmd = "zpool status -v"
debug.info(get_files_cmd)
process = subprocess.Popen(get_files_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
for line in process.stdout:
    if line:
        file_path = line.strip()
        if os.path.exists(file_path):
            debug.info (file_path)
            try:
                remove_file_cmd = "rm -fr \"{0}\" ".format(file_path)
                debug.info(remove_file_cmd)
                os.system(remove_file_cmd)
            except:
                debug.info(str(sys.exc_info()))
