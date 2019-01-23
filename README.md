# msdas
multisource data archiver system
## Install & Using
1. Cloned: git clone https://github.com/Bakirov-Artur/msdas.git
2. Create dir: mkdir -p /opt/tools/backup/
3. Copy file archver.py: cp ./msdas/archver.py /opt/tools/backup/
4. Copy file backup_data: cp ./msdas/backup_data /etc/cron.daily/
5. Edit backup_data(custom vars:BACKUP_DIRS, ARHC_NAME, DST_DIR): vim or your lovly editor /etc/cron.daily/backup_data
