#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import os
import sys
import debug
import subprocess

# proj_list = ["T_J_Main","T_J_pilot_durian","TOM_N_JERRY_s01_ep001_HDB","TOM_N_JERRY_s01_ep002_marinaBarrage","TOM_N_JERRY_s01_ep003_botanicalGarden","TOM_N_JERRY_s01_ep004_merlion","TOM_N_JERRY_s01_ep005_sentosa","TOM_N_JERRY_s01_ep006_murals","durian_test"]
# proj_list = ["short001_andeCrabBite","short002_pirkiEggChase"]
# proj_list = ['temp_short_cowboy', 'test_ap_2021', 'test_ap_HideAndSeek', 'test_ap_candyThief', 'test_ap_getTheDart', 'test_ap_hatAttack', 'test_ap_hypnocity', 'test_ap_rightBrothers', 'test_ap_shot_TheNextDay']
# proj_list = ['exam', 'examWorriors_m001', 'examWorriors_m001_examsAreFestivals', 'examWorriors_m002_ExamsTestPreparation', 'examWorriors_m002_laughInlaughOut', 'examWorriors_m004_BeAwarriorNotAworrier', 'examWorriors_m005_knowledgeIsPermanent', 'examWorriors_m006_competeWithYourself', 'examWorriors_m007_itIsYourTime', 'examWorriors_m008_thePresentIsGodsGreatestPresent', 'examWorriors_m009_technologyIsAgreatTeacher', 'examWorriors_m010_takeAdequateRest', 'examWorriors_m011_SharpenSleep', 'examWorriors_m012_playToShine', 'examWorriors_m013_beYourOwnAnchor', 'examWorriors_m014_reviseAndBecomeWise', 'examWorriors_m015_littleThingsMatter', 'examWorriors_m016_chooseYourOwnStyle', 'examWorriors_m017_presentationIsKey', 'examWorriors_m018_ToCheatIsToBeCheap', 'examWorriors_m019_theAnswerSheetIsAOneWayTicket', 'examWorriors_m020_discoverYourSelf', 'examWorriors_m021_IndiaIsIncredible', 'examWorriors_m022_AsOneJourneyEndsAnotherBigins', 'examWorriors_m023_AspireNotToBeButToDo', 'examWorriors_m024_BeGreatFul', 'examWorriors_m025_YogaBringsTransformation']
# proj_list = ['grantha', 'kshetra']
# proj_list = ['chotiChethana_ep001', 'chotiChethna_ep002', 'chotiChethna_ep003', 'chotiChethna_ep004', 'chotiChethna_ep005', 'chotiChethna_ep006', 'chotiChethna_ep007', 'chotiChethna_ep008', 'chotiChethna_ep009', 'chotiChethna_ep010', 'chotiChethna_ep011', 'chotiChethna_ep012', 'chotiChethna_ep013', 'chotiChethna_ep014', 'chotiChethna_ep015', 'chotiChethna_ep016', 'chotiChethna_ep017', 'chotiChethna_ep018', 'chotiChethna_ep019', 'chotiChethna_ep020', 'chotiChethna_ep021', 'chotiChethna_ep022', 'chotiChethna_ep023', 'chotiChethna_ep024', 'chotiChethna_ep025', 'chotiChethna_ep026', 'chotiChethna_ep027', 'chotiChethna_ep028', 'chotiChethna_ep029', 'chotiChethna_ep030', 'chotiChethna_ep031', 'chotiChethna_ep032', 'chotiChethna_ep033', 'chotiChethna_ep034', 'chotiChethna_ep035', 'chotiChethna_ep036', 'chotiChethna_ep037', 'chotiChethna_ep038', 'chotiChethna_ep039', 'chotiChethna_ep040', 'chotiChethna_ep041', 'chotiChethna_ep042', 'chotiChethna_ep043', 'chotiChethna_ep044', 'chotiChethna_ep045', 'chotiChethna_ep046', 'chotiChethna_ep047', 'chotiChethna_ep048', 'chotiChethna_ep049', 'chotiChethna_ep050', 'chotiChethna_ep051', 'chotiChethna_ep052', 'chotiChethna_ep053', 'chotiChethna_ep054', 'chotiChethna_ep055', 'chotiChethna_ep056']
# proj_list = ['AndePirki_Se02_short012_Jump', 'AndePirki_Se02_short013_door', 'AndePirki_Se02_short014_cookie', 'AndePirki_Stories', 'AndePirki_bible', 'AndePirki_library', 'AndePirki_library_02', 'AndePirki_se01_ep001_ballThrow', 'AndePirki_se01_ep002_highFly', 'AndePirki_se01_ep003_SavingPrivateRyan', 'AndePirki_se01_ep004_olympics', 'AndePirki_se01_ep005_missingEgg', 'AndePirki_se01_ep006_deliveryBoys', 'AndePirki_se01_ep007_salon_de_beaute01', 'AndePirki_se01_ep008_salon_de_beaute02', 'AndePirki_se01_ep009_salon_de_beaute03', 'AndePirki_se01_ep010_helpMenot', 'AndePirki_se01_ep011_prankathon', 'AndePirki_se01_ep012_rightBrothers', 'AndePirki_se01_ep013_fruitCause', 'AndePirki_se01_ep014_doctorTrouble']
# proj_list = ['AndePirki_se01_ep015_fruitBite', 'AndePirki_se01_ep016_hatAttack', 'AndePirki_se01_ep017_hideAndSeek', 'AndePirki_se01_ep018_sleepWalk', 'AndePirki_se01_ep019_letMeSleep', 'AndePirki_se01_ep020_goofBall', 'AndePirki_se01_ep021_hypnocity', 'AndePirki_se01_ep022_fishyBUsiness', 'AndePirki_se01_ep023_flyMeNot', 'AndePirki_se01_ep024_getTheDarts', 'AndePirki_se01_ep025_wheelPlay', 'AndePirki_se01_ep026_mangoBite', 'AndePirki_se01_ep027_painterSDayOut', 'AndePirki_se01_ep028_eggUntouchable', 'AndePirki_se01_ep029_candyThief', 'AndePirki_se01_ep030_badLuckBracelet']
# proj_list = ['AndePirki_se01_ep031_andysPainInTheTooth', 'AndePirki_se01_ep032_chickenHunt', 'AndePirki_se01_ep033_melonMillionaire', 'AndePirkise01_ep034_flyFlyAway']
# proj_list = ['AndePirki_se01_ep035_sleepyHunter', 'AndePirki_se01_ep036_hiccup', 'AndePirki_se01_ep037_', 'AndePirki_se01_ep037_hiccup', 'AndePirki_se01_ep037_iceSkating', 'AndePirki_se01_ep038_snowDogBear', 'AndePirki_se01_ep039_fishTale']
#proj_list = ['AndePirki_se01_short001_painting', 'AndePirki_se01_short002_ballThrow', 'AndePirki_se01_short003_soda', 'AndePirki_se01_short004_apple', 'AndePirki_se01_short005_door', 'AndePirki_se01_short006_iceSkate', 'AndePirki_se01_short007_cookie', 'AndePirki_se01_short011_woofers_2D', 'AndePirki_se01_short013_rubiksCube', 'AndePirki_se01_short014_highDivingAndy', 'AndePirki_se01_short015_jingleBells', 'AndePirki_se01_short016_newYear', 'AndePirki_se01_short017_armWrestling', 'AndePirki_se01_short018_woofers', 'AndePirki_se02_Library', 'AndePirki_se02_ep001_logIn', 'AndePirki_se02_ep002_HungerTimes', 'AndePirki_se02_ep003_eggHunt', 'AndePirki_se02_ep004_beautyAndTheFeast', 'AndePirki_se02_ep004_eggHuntCGI', 'AndePirki_se02_short001_diving', 'AndePirki_se02_short002_lightning', 'AndePirki_se02_short003_rocket', 'AndePirki_se02_short003_umbrella', 'AndePirki_se02_short004_shock', 'AndePirki_se02_short005_umbrella', 'AndePirki_se02_short006_newYear2020', 'AndePirki_se02_short007_MakaraSankranthi2020', 'AndePirki_se02_short008_Festivals_2020', 'AndePirki_se02_short009_HappyDance', 'AndePirki_se02_short010_Trap', 'AndePirki_se02_short011_woofers_2D']
#proj_list = ['Andepirki_se01_short008_bulb', 'Andepirki_se01_short009_boat', 'Andepirki_se01_short010_happySankranthi', 'Andepirki_se01_short011_frisbee', 'Andepirki_se01_short012_hiring', 'AndyPirki_SocialMedia']
# proj_list = ['CC_shorts001_HargharTiranga', 'Chandana', 'Jingles', 'Saha_Elegance', 'Saha_library','WEB', 'andePirki_AnimationExplore', 'andePirki_ep0001', 'blenderBrushes', 'chotiChethana', 'crapTests', 'drWings', 'drWings_ep002', 'drWings_ep003', 'drWings_ep004', 'ep001_beautyAndTheFeast', 'ep002_eggUntouchable', 'ep003_haveAbite', 'ep004_logIn', 'ep005_chickenHunt', 'pipeTest1', 'pipeTest5', 'short001_andeCrabBite', 'short002_pirkiEggChase', 'short004_andepirkiCowboy', 'study_ap_chickenHunt', 'study_ap_lightLayout']
proj_list = ['AndePirki_se01_ep034_flyFlyAway']


def copy_file(source_file, dest_path):
    # source_file = os.path.join(path, name)
    debug.info(source_file)
    # dest_path = (path.replace("/dell1-pool/stor2", "/dell2-pool/stor6"))
    debug.info(dest_path)

    rsync_command = "rsync -avzHXWhPs --zc=lz4 " + "\"" + source_file + "\"" + " \"kryptos@stor6:" + dest_path + os.sep + "\""
    debug.info(rsync_command)

    process = subprocess.Popen(rsync_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        if line:
            debug.info (line)



try:
    for proj in proj_list:
        debug.info(proj)
        # rsync_command = "rsync -avzHXWhPs --zc=lz4 kryptos@stor2:/dell1-pool/stor2"+os.sep+"{0}".format(proj)+" /dell2-pool/stor6/"
        # debug.info(rsync_command)
        
        createProjDirCmd = "rsync -av -f\"+ */\" -f\"- *\" \"/dell1-pool/stor2/{0}\" \"kryptos@stor6:/dell2-pool/stor6/\"".format(proj)
        debug.info(createProjDirCmd)
        process = subprocess.Popen(createProjDirCmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            if line:
                debug.info (line)

        
        source_path = "/dell1-pool/stor2"+os.sep+"{0}".format(proj)

        for path, subdirs, files in os.walk(source_path):
            for name in files:
                source_file = os.path.join(path, name)
                dest_path = (path.replace("/dell1-pool/stor2", "/dell2-pool/stor6"))
                if '.hg' in path:
                    pass
                elif 'log' in path:
                    pass
                elif 'output' in path:
                    if 'png' in name:
                        pass
                    elif 'exr' in name:
                        pass
                    else:
                        copy_file(source_file,dest_path)
                else:
                    copy_file(source_file,dest_path)
                
                # source_file = os.path.join(path, name)
                # debug.info(source_file)
                # dest_path = (path.replace("/dell1-pool/stor2", "/dell2-pool/stor6"))
                # debug.info(dest_path)

                # rsync_command = "rsync -avzHXWhPs --zc=lz4 " + "\"" + source_file + "\"" + " \"kryptos@stor6:" + dest_path + os.sep + "\""
                # debug.info(rsync_command)

                # process = subprocess.Popen(rsync_command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                # for line in process.stdout:
                #     if line:
                #         debug.info (line)

        # debug.info(files)

        # source_path = "kryptos@stor2:/dell1-pool/stor2"+os.sep+"{0}".format(proj)

        # rsync_command = ["rsync", "-avzHXWhPs", "--zc=lz4", source_path , "/dell2-pool/stor6/"]
        
        # process = subprocess.Popen(rsync_command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=1, universal_newlines=True)
        
        # for line in process.stdout:
        #     if line:
        #         debug.info (line)
except:
    debug.info(str(sys.exc_info()))
