#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os
import argparse

parser = argparse.ArgumentParser(description="Utility to batch rename files")
parser.add_argument('directory', type=str, help='Path to files')
parser.add_argument('targetName', type=str, help='Target file name')
parser.add_argument('targetFormat', type=str, help='Target file format')

args = parser.parse_args()

os.chdir(args.directory)
i = 1
files = os.listdir(args.directory)
files.sort()
print (files)
for file in files:
    # print (file)
    src=file
    dst=args.targetName+str(i)+args.targetFormat
    os.rename(src,dst)
    i+=1

