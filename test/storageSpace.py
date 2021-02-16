#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os
import sys
import subprocess


projname = ["AndePirki_se02_short010_Trap",
            "AndePirki_se02_ep003_eggHunt",
            "AndePirki_se01_ep039_fishTale",
            "AndePirki_se01_ep038_snowDogBear",
            "AndePirki_se01_ep037_iceSkating"]

folders = ["storyreel","animatic","storyboard","colorScript","conceptArt","colorKeys"]


outFile = file("/tmp/storageSpace.txt", "a")


for proj in projname:
    print (proj)
    outFile.write("\n"+proj+"\n")
    for folder in folders:
    # p = subprocess.Popen("du --max-depth=1 -h /blueprod/STOR2/stor2/"+ proj +"/preproduction",shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p = subprocess.Popen("du -sh /blueprod/STOR2/stor2/"+ proj +"/preproduction/"+folder,shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        outP = p.communicate()[0]
        print (outP)
        outFile.write(outP)

# for proj in projname:
#
#     p = subprocess.Popen("du -sh /blueprod/STOR2/stor2/"+ proj +"/preproduction",shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#     outP = p.communicate()[0]
#     print (outP)




outFile.close()
