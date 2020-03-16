#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import os

driverLink = "https://github.com/DIGImend/digimend-kernel-drivers/releases/download/v9/digimend-kernel-drivers-9.tar.gz"
os.system("cd /opt/; aria2c -c -s 10 -x 10 "+ driverLink + "; tar -xvf digimend-kernel-drivers-9.tar.gz;")
os.system("cd /opt/digimend-kernel-drivers-9; make; sudo make install;")


