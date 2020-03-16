#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

## UTILITY TO UPDATE BLENDER-2.81 BETA RELEASES ##

import sys
import os
from bs4 import BeautifulSoup
import urllib2
import re

htmlPage = urllib2.urlopen("https://builder.blender.org/download/")
soup = BeautifulSoup(htmlPage, 'html.parser')
downloadLink = None
fileName = None
untaredFolder = None
destinationDir = "/home/sanath.shetty/Packages/blender-2.81/"
crapDir = "/crap/crap.server/softwares/blender/blender-2.81-linux-glibc217-x86_64/"

for link in soup.findAll('a', attrs={'href': re.compile("(?=.*2.81)(?=.*linux-glibc217-x86_64.tar.bz2)")}):
    fileName = link.get('href').replace("/download/","")
    untaredFolder = fileName.replace(".tar.bz2","")
    downloadLink = ("https://builder.blender.org"+link.get('href'))
    print (downloadLink)
    print(fileName)

if(downloadLink):
    if(os.path.exists(os.path.join(destinationDir,untaredFolder))):
        print("already up to date")
        sys.exit(0)
    os.system("aria2c -c -s 10 -x 10 -d /tmp/ "+ downloadLink)
    os.system("cd /tmp/ ;tar -xvf "+ fileName +" ; cd -")
    os.system("rsync -av /tmp/"+ untaredFolder +" "+ destinationDir)
    os.system("cd "+crapDir+"; rm -frv *")
    os.system("cd "+destinationDir+untaredFolder+"; rsync -av * "+crapDir)

else:
    print("Wrong Syntax.")
