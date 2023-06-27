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
import csv


fileDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
baseDir = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-4])

sys.path.append(baseDir)

import rbhus.utilsPipe
import rbhus.debug
import rbhus.constantsPipe
import rbhus.dbPipe



parser = argparse.ArgumentParser()
parser.add_argument("-a","--all",dest='all',action="store_true")
parser.add_argument("-d","--dryrun",dest='dryrun',action="store_true",help="do a test run without actually backing up anything")
parser.add_argument("-p","--projects",dest='projects',help="comma seperated list of projects to backup")
args = parser.parse_args()



excludeProjects = ['AndePirki_se01_ep024_getTheDarts',
                   'AndePirki_se01_ep023_flyMeNot',
                   'AndePirki_se01_ep016_hatAttack',
                   'AndePirki_se01_ep017_hideAndSeek',
                   'AndePirki_se01_ep018_sleepWalk',
                   'AndePirki_se01_ep019_letMeSleep',
                   'AndePirki_se01_ep020_goofBall',
                   'AndePirki_se01_ep021_hypnocity',
                   'AndePirki_se01_ep022_fishyBUsiness',
                   'andePirki_AnimationExplore',
                   'examWorriors_m001',
                   'examWorriors_m002_laughInlaughOut',
                   'AndyPirki_SocialMedia']

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
  allProjSize = 0
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

  projCsvFd = open("/blueprod/CRAP/crap/shrinidhi/projectSize/project_sizes.csv", "a+")
  projCsv = [["projName"," size in TB"]]
  for proj in allProj:
    # if(proj['projName'] in excludeProjects):
    #   continue

    allAssets = rbhus.utilsPipe.getProjAsses(proj['projName'])
    projSize = 0
    if(allAssets):
      assCsvFd = open("/blueprod/CRAP/crap/shrinidhi/projectSize/assets__"+ proj['projName'] +".csv","w")
      assCsv = [['asset','size in MB']]


      for x in allAssets:
        try:
          assSize = 0
          if(x):
            dirMapDets = rbhus.utilsPipe.getDirMapsDetails(x['backupDir'])
            assAbsPath = rbhus.utilsPipe.getAbsPath(x['path'])

            if(x['assetType'] != "output"):
              # print(x['path'])
              if(os.path.exists(assAbsPath)):
                p = subprocess.Popen("du -sx " + assAbsPath, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                try:
                  outp = p.communicate()[0].split()[0]
                  assSize = float(outp)
                  projSize = projSize + assSize
                  allProjSize = allProjSize + assSize
                except:
                  print("asset error : "+ str(x['path']) +" :::::: "+ str(assAbsPath))

            elif(x['assetType'] == "output" and (x['assName'] == "Movs" or x['assName'] == "MovsFx" or x['assName'] == "Rendered_SF" or x['assName'] == "RenderedSF") and (x['sequenceName'] == 'default' and x['sceneName'] == 'default')):
              # print(x['path'])
              if(os.path.exists(assAbsPath)):
                p = subprocess.Popen("du -sx " + assAbsPath, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                try:
                  outp = p.communicate()[0].split()[0]
                  assSize = float(outp)
                  projSize = projSize + assSize
                  allProjSize = allProjSize + assSize
                except:
                  print("asset error : " + str(x['path']) + " :::::: " + str(assAbsPath))

            assCsv.append([x['path'],assSize/1024])
            print("asset "+ x['path'] +" "+ str((assSize / 1024) ) +" MB")
        except:
          rbhus.debug.error(str(sys.exc_info()[2].tb_lineno) + " " + str(sys.exc_info()))

      projCsv.append([proj['projName'], ((projSize / 1024) / 1024) / 1024, " TB "])
      print("projName "+ proj['projName'] + "  " + str(((projSize / 1024) / 1024) / 1024) +" TB")


      with assCsvFd:
        writer = csv.writer(assCsvFd)
        writer.writerows(assCsv)

  with projCsvFd:
    writer = csv.writer(projCsvFd)
    writer.writerows(projCsv)

  if(allProjSize):
    print("Total size in TB - " + str(((allProjSize / 1024) / 1024) / 1024))
except:
  rbhus.debug.error(str(sys.exc_info()[2].tb_lineno) +" "+ str(sys.exc_info()))
