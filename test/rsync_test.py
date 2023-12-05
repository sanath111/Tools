#!/usr/bin/python2
# *-* coding: utf-8 *-*


import os
import sys


base_path = "/backup-pool1/backup/"
try:
    for path, subdirs, files in os.walk("/backup-pool1/backup/chotiChethna_ep055"):
        for name in files:
            file = os.path.join(path, name)
            relative_file_path = os.path.relpath(file, base_path)
            print (relative_file_path)
            rsyncCmd = "rsync -avzHXWhPs --zc=zstd --relative {0} bluepixels@stor6:/dell2-pool/stor6/test_backup_recovery/".format(relative_file_path)
            os.system(rsyncCmd)
except:
    print(str(sys.exc_info()))


base_path = "/dell1-pool/stor2/"
try:
    for path, subdirs, files in os.walk("/dell1-pool/stor2/TOM_N_JERRY_s01_ep003_botanicalGarden"):
        for name in files:
            file = os.path.join(path, name)
            relative_file_path = os.path.relpath(file, base_path)
            print(relative_file_path)
            rsyncCmd = "rsync -avzHXWhPs --zc=lz4 --relative {0} kryptos@stor6:/dell2-pool/stor6/".format(relative_file_path)
            print(rsyncCmd)
except:
    print(str(sys.exc_info()))
