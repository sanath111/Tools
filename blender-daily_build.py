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
import argparse

parser = argparse.ArgumentParser(description="blender alpha builds downloader")
parser.add_argument("-t","--type",dest="type",help="Type of the build.(ex: daily, experimental")
parser.add_argument("-v","--version",dest="version",help="Version of the build.(ex: 3.0.0-alpha)")
parser.add_argument("-b","--branch",dest="branch",help="Branch of the build.(ex: master, cycles-x)")
args = parser.parse_args()

build_str = ""
version_str = ""

# build_str = "https://builder.blender.org/download/experimental/"

# version_str = "(?=.*2.82)(?=.*linux-glibc217-x86_64.tar.xz)"
# version_str = "(?=.*2.83)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.90)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.91)(?=.*linux64.tar.xz)"
# version_str = "(?=.*2.92)(?=.*linux64.tar.xz)"
# version_str = "(?=.*3.0.0)(?=.*alpha)(?=.*cycles-x)(?=.*linux.x86_64-release.tar.xz)"

if args.type:
    build_str = "https://builder.blender.org/download/"+args.type+"/"
else:
    build_str = "https://builder.blender.org/download/daily/"

if args.version and args.branch:
    version_str = "(?=.*{0})(?=.*{1})(?=.*linux.x86_64-release.tar.xz)".format(args.version, args.branch)
else:
    # version_str = "(?=.*3.0.0-alpha)(?=.*master)(?=.*linux.x86_64-release.tar.xz)"
    # version_str = "(?=.*3.0.0-beta)(?=.*v30)(?=.*linux.x86_64-release.tar.xz)"
    # version_str = "(?=.*3.2)(?=.*linux.x86_64-release.tar.xz)"
    version_str = "(?=.*3.3.0)(?=.*linux.x86_64-release.tar.xz)"


htmlPage = urllib2.urlopen(build_str)
soup = BeautifulSoup(htmlPage, 'html.parser')
downloadLink = None
fileName = None
untaredFolder = None
optDir = "/opt/blender-daily_build/"

try:
    links = {}
    for link in soup.findAll('a', attrs={'href': re.compile(version_str)}):
        downloadLink = link.get('href')
        downloadLabel = link.get('ga_label')
        if downloadLabel:
            links[str(downloadLabel)] = str(downloadLink)

    downloadLink = str(links['linux 64bit tar.xz file'])
    fileName = str(downloadLink.replace(build_str,""))
    untarredFolder = str(fileName.replace(".tar.xz",""))
    print (downloadLink)
    print (fileName)
    print (untarredFolder)

    if (os.path.exists(os.path.join(optDir, untarredFolder))):
        os.system("sudo ln -sf " + optDir + untarredFolder + "/blender /usr/local/bin/blenderBeta")
        print("already up to date")
        # sys.exit(0)
    else:
        # os.system("sudo aria2c --check-certificate=false -c -s 10 -x 10 -d " + optDir + " " + downloadLink)
        os.system("sudo aria2c -c -s 10 -x 10 -d " + optDir + " " + downloadLink)
        os.system("cd " + optDir + " ;sudo tar -xvf " + fileName + " ; cd -")
        # os.system("sudo rm -frv /usr/local/bin/blender")
        os.system("sudo ln -sf " + optDir + untarredFolder + "/blender /usr/local/bin/blenderBeta")

except:
    print(str(sys.exc_info()))
