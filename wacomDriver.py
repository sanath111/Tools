#!/usr/bin/python2
# *-* coding: utf-8 *-*

## UTILITY TO DOWNLOAD WACOM DRIVERS ##

import os

wacomFolder = "/opt/inputWacom/"
url = "https://github.com/linuxwacom/input-wacom/releases/download/input-wacom-0.43.0/input-wacom-0.43.0.tar.bz2"

if os.path.exists(wacomFolder) == True:
    os.system('rm -frv '+ wacomFolder + '*')
else:
    os.system('cd /opt/ ; mkdir inputWacom')

os.system('cd ' + wacomFolder + ' ; wget ' + url + ' ; tar -xvf input-wacom* ; rm -frv *.tar.bz2 ')
os.system('cd ' + wacomFolder +'input-wacom* ; if test -x ./autogen.sh; then ./autogen.sh; else ./configure; fi && make && sudo make install || echo "Build Failed"')
