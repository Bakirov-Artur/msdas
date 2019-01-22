#!/usr/bin/env python
# -*- coding: utf-8 -*-
#BakirovAR turkin86@mail.ru
import tarfile
import os
from datetime import datetime, timedelta
from subprocess import PIPE, Popen

app = 'mount'
app_argv = '/media/ostore'
#app_handle = Popen([app, app_argv], stdout=PIPE)

FILES_SET = ['/home/dds/', '/etc/fstab']
BACKUP_HOME = 'DDBackup/dd_dds'
STORAGE_HOME = '/media/ostore'
STORAGE_PATH = os.path.sep.join([STORAGE_HOME, BACKUP_HOME])

current_time = datetime.now().strftime("%Y%m%d%H%M%S")

#parametr type (zip, rar, tar, gz)
ARHIVE_NAME = 'dds'
ARHIVE_TYPE = 'tar.gz'
ARHIVE_FILE = '.'.join([ARHIVE_NAME, current_time, ARHIVE_TYPE])
ARHIVE_PATH = os.path.sep.join([STORAGE_PATH, ARHIVE_FILE])

index_weekdays = [3, 4, 6]
current_weekday = datetime.today().weekday()

print("Start Backup")

SPDS=True #save parent paths directory structure

for i in index_weekdays:
    if current_weekday == i:
        tar = tarfile.open(ARHIVE_PATH, "w:gz")
        for fl in FILES_SET:
            print(fl)
            if (os.path.isdir(fl)):
                cwd = os.getcwd()
                os.chdir(fl)
                files = os.listdir('.')
                for name in files:
                    if SPDS :
                        fpath=os.path.join(fl, os.path.sep.join([name]))
                    else:
                        fpath = name
                    tar.add(fpath)
                    print("%-5s add: %s" % ('', fpath))
                os.chdir(cwd)
            else:
                tar.add(fl)
                print("add file: %s" % (fl))
        tar.close()

