#!/bin/bash
# Julius Zaromskis
# Backup rotation

# Storage folder where to move backup files
# Must contain backup.monthly backup.weekly backup.daily folders
storage=/backup

# Source folder where files are backed
source=$storage/incoming

# Destination file names
date_daily=`date +"%d-%m-%Y"`
#date_weekly=`date +"%V sav. %m-%Y"`
#date_monthly=`date +"%m-%Y"`

# Get current month and week day number
month_day=`date +"%d"`
week_day=`date +"%u"`

# It is logical to run this script daily. We take files from source folder and move them to
# appropriate destination folder

# Note that this puts each day's files in eactly one place. They never move. On the first day of the month, for example,
# the files will be put into backup.monthly and you will not find them in backup.daily.

# On first month day do
if [ "$month_day" -eq 1 ] ; then
  destination=backup.monthly/$date_daily
else
  # On saturdays do
  if [ "$week_day" -eq 6 ] ; then
    destination=backup.weekly/$date_daily
  else
    # On any regular day do
    destination=backup.daily/$date_daily
  fi
fi

# Move the files
mkdir $destination
mv -v $source/* $destination

/usr/local/bin/python /app/healthchecks.py vdjbase-backups log -m "backup file stored at $destination"

# Cut these times down because VDJbase data is pretty static

# daily - keep for 7 days
find $storage/backup.daily/ -maxdepth 1 -mtime +3 -type d -exec rm -rv {} \;

# weekly - keep for 30 days
find $storage/backup.weekly/ -maxdepth 1 -mtime +3 -type d -exec rm -rv {} \;

# monthly - keep for 180 days
find $storage/backup.monthly/ -maxdepth 1 -mtime +3 -type d -exec rm -rv {} \;
