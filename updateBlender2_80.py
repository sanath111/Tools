#!/usr/bin/python2
# *-* coding: utf-8 *-*

## UTILITY TO UPDATE BLENDER-2.80 BETA RELEASES ##

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
destinationDir = "/proj/standard/share/"

for link in soup.findAll('a', attrs={'href': re.compile("(?=.*2.8)(?=.*linux-glibc224-x86_64.tar.bz2)")}):
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

blenderrc="/proj/standard/share/blender-2.80-rc"
blenderfinal=os.path.join(destinationDir,untaredFolder)

os.system ("rm " + blenderrc)
os.system ("ln -sf " + blenderfinal + " " + blenderrc)
