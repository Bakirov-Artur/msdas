#!/usr/bin/env python
# -*- coding: utf-8 -*-
#BakirovAR turkin86@mail.ru
import tarfile
import os
import sys
import shutil
import logging
from datetime import datetime, timedelta

current_time = datetime.now().strftime("%Y%m%d%H%M%S")

app_name = os.path.basename(__file__)
app_path = os.path.dirname(os.path.abspath( __file__ ))

#logger

flog_name = '.'.join([current_time, "log"])
flog_dirs = 'logs'
flog_path = os.path.sep.join([app_path, flog_dirs, flog_name])

if not os.path.isdir(os.path.dirname(flog_path)):
    os.makedirs(os.path.dirname(flog_path))

logging.basicConfig(filename=flog_path, level=logging.INFO, format = u'%(asctime)-4s %(levelname)-4s %(message)s')

logging.info("App started: %s" %(app_name))
logging.info("App home path: %s" %app_path)

#Нужно добавить обработку ошибок

#notes https://docs.python.org/2.7/library/argparse.html
arguments = sys.argv[1:]
args_count = len(arguments)

if args_count < 3:
    logging.error("No input arguments")
    logging.error("%s {SOURCE_LIST_PATH} {DESTINATION_PATH} {ARCHIVE_NAME}" % (program_name))
    logging.error("example: %s \"/home /etc/fstab /usr\" /media/storage my_archive" % (program_name))
    sys.exit(1)

FILES_SET = []
STORAGE_REMOTE_PATH = ""
ARHIVE_NAME = ""

for x in range(args_count):
    if x == 0:
        fls = arguments[x].split(' ')
        FILES_SET = fls
    elif x == 1:
        STORAGE_REMOTE_PATH = arguments[x]
    elif x == 2:
        ARHIVE_NAME = arguments[x]

STORAGE_PATH = "/opt/backups"

if not os.path.isdir(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)
    logging.info("Create temp dir: %s" %(STORAGE_PATH))

#arhive parametr type: tar.gz
if not ARHIVE_NAME:
    ARHIVE_NAME = 'backup'
    logging.warning("Archive name: %s" %(ARHIVE_NAME))
ARHIVE_TYPE = 'tar.gz'
ARHIVE_FILE = '.'.join([ARHIVE_NAME, current_time, ARHIVE_TYPE])
ARHIVE_PATH = os.path.sep.join([STORAGE_PATH, ARHIVE_FILE])
logging.info("Path archive file: %s" %(ARHIVE_PATH))
index_weekdays = [1, 2, 4, 6]
current_weekday = datetime.today().weekday()

logging.info("Start Backup")

SPDS=True #save parent paths directory structure

for i in index_weekdays:
    if current_weekday == i:
        cwdu = os.getcwd()
        os.chdir(STORAGE_PATH)
        tar = tarfile.open(ARHIVE_FILE, "w:gz")
        for fl in FILES_SET:
            logging.info(fl)
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
                    logging.info("%-5s add: %s" % ('', fpath))
                os.chdir(cwd)
            else:
                tar.add(fl)
                logging.info("add file: %s" % (fl))
        tar.close()
        os.chdir(cwdu)

#Move all files to STORAGE_REMOTE_PATH
if os.path.isdir(STORAGE_REMOTE_PATH):
    logging.info("Start move files")
    archive_files = os.listdir(STORAGE_PATH)
    for f in archive_files:
        sf = os.path.sep.join([STORAGE_PATH, f])
        rf = os.path.sep.join([STORAGE_REMOTE_PATH, f])    
        shutil.move(sf, rf)
        logging.info("move: %s to: %s" %(sf, rf))
else:
    logging.info("No such file or directory: %s" % (STORAGE_REMOTE_PATH))
    sys.exit(1)

logging.info("Archiving successfully completed")    
sys.exit(0)
