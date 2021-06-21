#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

## UTILITY TO UPDATE BLENDER-DAILY BUILDS ##

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
optDir = "/opt/blender-daily_build/"

# version_str = "(?=.*2.82)(?=.*linux-glibc217-x86_64.tar.xz)"
# version_str = "(?=.*2.83)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.90)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.91)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.92)(?=.*linux64.tar.xz)"
version_str = "(?=.*3.0.0)(?=.*alpha)(?=.*linux.x86_64-release.tar.xz)"

try:
    links = {}
    for link in soup.findAll('a', attrs={'href': re.compile(version_str)}):
        downloadLink = link.get('href')
        downloadLabel = link.get('ga_label')
        if downloadLabel:
            links[str(downloadLabel)] = str(downloadLink)

    downloadLink = str(links['linux 64bit tar.xz file'])
    fileName = str(downloadLink.replace("https://builder.blender.org/download/daily/",""))
    untarredFolder = str(fileName.replace(".tar.xz",""))
    print (downloadLink)
    print (fileName)
    print (untarredFolder)

    if (os.path.exists(os.path.join(optDir, untarredFolder))):
        os.system("sudo ln -sf " + optDir + untarredFolder + "/blender /usr/local/bin/blenderBeta")
        print("already up to date")
        sys.exit(0)
    else:
        os.system("sudo aria2c -c -s 10 -x 10 -d " + optDir + " " + downloadLink)
        os.system("cd " + optDir + " ;sudo tar -xvf " + fileName + " ; cd -")
        # os.system("sudo rm -frv /usr/local/bin/blender")
        os.system("sudo ln -sf " + optDir + untarredFolder + "/blender /usr/local/bin/blenderBeta")

except:
    print(str(sys.exc_info()))
