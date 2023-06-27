#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

import sys
import os
from bs4 import BeautifulSoup
import urllib.request
import re

# url = "https://ambientcg.com/list?type=Material"
# url = "https://ambientcg.com/list?type=Material&sort=Popular&offset=180&limit=180&include=displayData%2CdimensionsData%2CimageData"
url = "https://ambientcg.com/list?type=Material&sort=Popular&offset=0"

html_page = urllib.request.urlopen(url)
soup = BeautifulSoup(html_page, "html.parser")

asset_dir = "/home/sanath.shetty/Blender/textures/ambient_cg/"

links = {}

for link in soup.findAll('a', attrs={'href': re.compile("id")}):
    asset_url = link.get('href')
    # print(link.get('href'))
    links[str(asset_url).strip("/view?id=")] = "https://ambientcg.com"+str(asset_url)

# print(links)

for ass_url in links.values():
    ass_url_new = ass_url.replace("view?id","get?file") + "_2K-JPG.zip"
    # print(ass_url_new)
    os.system("aria2c --check-certificate=false -c -s 10 -x 10 -d " + asset_dir + " " + ass_url_new)

files = os.listdir(asset_dir)
for file in files:
    new_file = file.replace(".zip",".usdz")
    os.system("mv " + asset_dir + file + " " + asset_dir+new_file)
