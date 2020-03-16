#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"


import os

blender_source_dir = "/home/sanath.shetty/blender-git/blender/"
blender_build_dir = "/home/sanath.shetty/blender-git/build_linux/"

os.system("cd "+blender_source_dir+" ; git submodule update --init --recursive ; git submodule foreach git checkout master ; git submodule foreach git pull --rebase origin master")
os.system("cd "+blender_source_dir+" ; git stash ; make update ; git stash pop ; make")
os.system("cd "+blender_build_dir+" ; make ; make install")
os.system("cd "+blender_build_dir+"bin/ ; ./blender")
