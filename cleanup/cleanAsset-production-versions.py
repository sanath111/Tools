#!/usr/bin/env python2
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os
import re
import time
import argparse
import subprocess

fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe
import rbhus.dbPipe



parser = argparse.ArgumentParser()
parser.add_argument("-d","--dryrun",dest='dryrun',action="store_true",help="do a test run without actually backing up anything")
parser.add_argument("-p","--projects",dest='projects',help="comma seperated list of projects to cleanup")
args = parser.parse_args()



# excludeProjects = ['AndePirki_se01_ep039_fishTale','AndePirki_se01_ep038_snowDogBear','AndePirki_se01_short018_woofers']

def getAllProjects(days=7):
  dbproj = rbhus.dbPipe.dbPipe()
  projs = dbproj.execute("select * from proj",dictionary=True)
  uniqproj = {}
  projToRet = []
  if(projs):
    for x in projs:
      if(not uniqproj.has_key(x['projName'])):
        projDetail = rbhus.utilsPipe.getProjDetails(x['projName'].strip())
        uniqproj[x['projName']] = 1
        projToRet.append(projDetail)

  return(projToRet)

# for x in getProjForBackup():
#   print(x['projName'])
# sys.exit(0)

def isValidBackupDir(directory):
  allDirMaps = rbhus.utilsPipe.getDirMaps(dirType="backup")
  if(allDirMaps):
    for x in allDirMaps:
      if(x['directory'] == directory):
        return(True)
  return(False)


def getCompoundPaths(assPath,allAssets,isVersion=False):
  pathSrcBackup = rbhus.utilsPipe.getAbsPath(assPath)
  retpaths = []
  for x in allAssets:
    pathToX = rbhus.utilsPipe.getAbsPath(x['path'])
    if(pathSrcBackup != pathToX):
      if(os.path.exists(pathToX)):
        if(re.search(pathSrcBackup,pathToX)):
          if(isVersion):
            if(isVersioning(pathToX)):
              retpaths.append(pathToX)
          else:
            retpaths.append(pathToX)
  return(retpaths)



def isVersioning(absPath):
  if (os.path.exists(absPath + "/.hg")):
    # rbhus.debug.info("versioning main : true")
    return (True)
  else:
    # rbhus.debug.info("versioning main : false")
    return (False)

try:
  totalDelete = 0
  allProj = []
  if(args.projects):
    # print(args.projects)
    projects = args.projects.split(",")
    for p in projects:
      projDet = rbhus.utilsPipe.getProjDetails(p.strip())
      if(projDet):
        allProj.append(projDet)
      else:
        rbhus.debug.warning("bad project name : "+ str(p))
  else:
    print("Enter a list of projects to clean")
    sys.exit(0)

  for proj in allProj:
    allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])
    if(allAssets):
      for x in allAssets:
        if(x['assetType'] != "output" ):
          if(x['stageType'] != 'preproduction'):
            # print(x['path'])
            assAbsPath = rbhus.utilsPipe.getAbsPath(x['path'])
            versionPaths = []
            if(os.path.exists(assAbsPath)):
              if(isVersioning(assAbsPath)):
                versionPaths.append(os.path.join(assAbsPath,".hg"))
                versionPaths.append(os.path.join(assAbsPath,".hglf"))

                if(versionPaths):
                  for versionPath in versionPaths:
                    if(os.path.exists(versionPath)):

                      p = subprocess.Popen("du -sx "+ versionPath,shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                      outp = p.communicate()[0].split()[0]

                      totalDelete = totalDelete + float(outp)
                      rmcmd = "rm -frv "+ str(versionPath)
                      print(rmcmd)
                      if (args.dryrun == False):
                        q = subprocess.Popen(rmcmd, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        outq = q.communicate()[0].split()[0]
                        print("deleting : "+ versionPath)

                              # print(out)
                          # for lds in latestDir[-2:]:
                          #   print("+ "+ lds)
            # else:
            #   print("no output dir")
  if(totalDelete):
    print("Total to delete in TB - "+ str(((totalDelete/1024)/1024)/1024))
  if(args.dryrun == False):
    print("Total DELETED! in TB - " + str(((totalDelete / 1024) / 1024) / 1024))
except:
  rbhus.debug.error(str(sys.exc_info()))
