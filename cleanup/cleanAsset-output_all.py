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
parser.add_argument("-a","--all",dest='all',action="store_true")
parser.add_argument("-n","--no-preserve",dest='nopreserve',action="store_true")
parser.add_argument("-d","--dryrun",dest='dryrun',action="store_true",help="do a test run without actually backing up anything")
parser.add_argument("-p","--projects",dest='projects',help="comma seperated list of projects to backup")
args = parser.parse_args()



# excludeProjects = ['AndePirki_se01_ep039_fishTale','AndePirki_se01_ep038_snowDogBear','AndePirki_se01_short018_woofers']
# excludeProjects = ['AndePirki_se02_ep001_logIn', 'AndePirki_se02_short001_diving','AndePirki_se02_short002_lightning','AndePirki_se02_short003_rocket','AndePirki_se02_short004_shock']
# excludeProjects = ['AndePirki_se02_ep002_HungerTimes', 'AndePirki_se02_short001_diving','AndePirki_se02_short002_lightning','AndePirki_se02_short003_rocket','AndePirki_se02_short004_shock','AndePirki_se02_short006_newYear2020','study_ap_lightLayout']
# excludeProjects = ['AndePirki_se02_ep003_eggHunt','AndePirki_se02_ep004_eggHuntCGI','AndePirki_se02_short009_HappyDance']
# excludeProjects = ['AndePirki_se02_short010_Trap']
excludeProjects = ['chotiChethna_ep050','chotiChethna_ep051','chotiChethna_ep052','chotiChethna_ep053','chotiChethna_ep054','chotiChethna_ep055']

def getProjForBackup(days=7):
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


def setAssetDone(assPath):
  project = assPath.split(":")[0]
  asspathfd = open("/tmp/"+ project,"a+")
  asspathfd.write(assPath +"\n")
  asspathfd.flush()
  asspathfd.close()


def isAssetDone(assPath):
  project = assPath.split(":")[0]
  if(os.path.exists("/tmp/" + project)):
    asspathfd = open("/tmp/" + project, "r")
    for x in asspathfd.readlines():
      # print(x.strip())
      if(x.strip() == assPath):
        return(True)
    asspathfd.close()
  return(False)

def sortKey(value):
  try:
    # print(value.split(os.sep)[-1])
    return(float(value.split(os.sep)[-1]))
  except:
    return(0.0)


def getTimeSortedDirs(dirPath):
  all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)))]

  if(all_subdirs):
    # latest_subdir = sorted(all_subdirs, key=os.path.getmtime,reverse=True)
    latest_subdir = sorted(all_subdirs, key=sortKey, reverse=True)
    # latest_subdir = all_subdirs.sort()

    # rbhus.debug.info(latest_subdir)
    return(latest_subdir)
  else:
    return(False)



def getLatestDir(dirPath):
  all_subdirs = [os.path.join(dirPath,x) for x in os.listdir(dirPath) if(os.path.isdir(os.path.join(dirPath,x)))]
  if(all_subdirs):
    latest_subdir = max(all_subdirs, key=os.path.getmtime)
    return(latest_subdir)
  else:
    return(False)


def cleanBackUp(assDets):
  dirMapDets = rbhus.utilsPipe.getDirMapsDetails(assDets['backupDir'])
  pathDestBackupBase = os.path.join(dirMapDets['linuxMapping'],assDets['projName'],assDets['assetId'])
  sortedPaths = getTimeSortedDirs(pathDestBackupBase)
  if(sortedPaths):
    totalBacked = len(sortedPaths)
    toPreserve = sortedPaths[:int(assDets['backupCountToRetain'])]
    toDelLen = totalBacked - int(assDets['backupCountToRetain'])
    if(toDelLen <= 0):
      toDelete = []
    else:
      toDelete = sortedPaths[-toDelLen:]
    print("DELETING : "+ str(len(toDelete)))
    for x in toDelete:
      # print(x)
      os.system("rm -fr "+ x)

    print("PRESERVING : "+ str(len(toPreserve)))
    # for x in toPreserve:
      # print(x)



def isVersioning(absPath):
  if (os.path.exists(absPath + "/.hg")):
    rbhus.debug.info("versioning main : true")
    return (True)
  else:
    rbhus.debug.info("versioning main : false")
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
    allProj = getProjForBackup()

  for proj in allProj:
    if(proj['projName'] in excludeProjects):
      continue

    allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])
    if(allAssets):
      for x in allAssets:
        if(x['assetType'] == "output" and (x['assName'] != "Movs" and x['assName'] != "MovsFx" and x['assName'] != "Rendered_SF" and x['assName'] != "RenderedSF") and (x['sequenceName'] != 'default' and x['sceneName'] != 'default')):
          # print(x['path'])
          dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
          assAbsPath = rbhus.utilsPipe.getAbsPath(x['path'])

          if(os.path.exists(assAbsPath)):
            # p = subprocess.Popen("du -sx " + assAbsPath, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            # outp = p.communicate()[0].split()[0]
            #
            # totalDelete = totalDelete + float(outp)

            outputDir1_2  = getTimeSortedDirs(assAbsPath)
            # rbhus.debug.info(outputDir1_2)
            if(outputDir1_2):
              for outputDir1 in outputDir1_2:
                # print("\_"+ outputDir1)
                if(os.path.exists(outputDir1)):
                  # print(outputDir1)
                  # rmcmd = "rm -frv " + str(outputDir1)
                  # print(rmcmd)
                  # if (args.dryrun == False):
                  #   q = subprocess.Popen(rmcmd, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                  #   outq = q.communicate()[0].split()[0]
                  #   print(outq)
                  outputDir2 = getTimeSortedDirs(outputDir1)
                  if(outputDir2):
                    for od2 in outputDir2:
                      # print("  \_"+ od2)
                      latestDir = getTimeSortedDirs(od2)

                      # if(latestDir):
                      #   latestDir.reverse()
                      #   # print("    \_")
                      #   latestDirImproved = []
                      #   for ldi in latestDir:
                      #
                      #     if(ldi.split(os.sep)[-1].isdigit()):
                      #       latestDirImproved.append(ldi)
                      #   toDeleteDir = latestDirImproved[:-1]
                      # print(latestDir)
                      if(latestDir):
                        for ld in latestDir:
                          print("todel : " + str(ld))

                          p = subprocess.Popen("du -sx "+ ld,shell=True,stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                          outp = p.communicate()[0].split()[0]

                          totalDelete = totalDelete + float(outp)
                          rmcmd = "rm -frv "+ str(ld)
                          print(rmcmd)
                          if (args.dryrun == False):
                            q = subprocess.Popen(rmcmd, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                            outq = q.communicate()[0].split()[0]

                            print(outq)

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
