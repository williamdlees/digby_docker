#!/bin/bash
#@author Julius Zaromskis
#@description Backup script for your website

BACKUP_DIR=/backup
TEMP_DIR=/tmp

/usr/local/bin/python /app/healthchecks.py vdjbase-backups start

# Precautionary cleanup
mkdir -p $BACKUP_DIR/incoming
mkdir -p $BACKUP_DIR/temp
mkdir -p $BACKUP_DIR/backup.daily
mkdir -p $BACKUP_DIR/backup.weekly
mkdir -p $BACKUP_DIR/backup.monthly
rm $BACKUP_DIR/incoming/*
rm -rf $BACKUP_DIR/temp/*

# Dump MySQL tables
mysqldump --all-databases -h mariadb -P 3306 -u root -p'7Th3y45!N&i%@RW' >/config/log/sqldump

if ! [ $(find "/config/log/sqldump") ]
then
    /usr/local/bin/python /app/healthchecks.py vdjbase-backups fail -m "/config/log/sqldump not created"
	exit
else
	echo "/config/log/sqldump created"
fi	

if [ $(find "/config/log/sqldump" -mmin +60) ]
then
	/usr/local/bin/python /app/healthchecks.py vdjbase-backups fail -m "/config/log/sqldump not updated"
	exit
else
	echo "/config/log/sqldump updated"
fi

if [ $(find "/config/log/sqldump" -printf "%s") -lt 1000 ]
then
	/usr/local/bin/python /app/healthchecks.py vdjbase-backups fail -m "/config/log/sqldump is implausibly small"
	exit
else
	echo "/config/log/sqldump is a reasonable size"
fi

# Backup logs and config
mkdir -p $BACKUP_DIR/temp/config
cp -r /config/*  $BACKUP_DIR/temp/config/.
mkdir -p $BACKUP_DIR/temp/app
cp -r /app/*  $BACKUP_DIR/temp/app/.
mkdir -p $BACKUP_DIR/temp/study_data
cp -r /study_data/*  $BACKUP_DIR/temp/study_data/.

cd $BACKUP_DIR/temp

# Compress tables and files
tar -cvzf $BACKUP_DIR/incoming/archive.tgz *

if ! [ $(find "$BACKUP_DIR/incoming/archive.tgz") ]
then
    /usr/local/bin/python /app/healthchecks.py vdjbase-backups -m "$BACKUP_DIR/incoming/archive.tgz not created"
	exit
else
	echo "$BACKUP_DIR/incoming/archive.tgz created"
fi	

if [ $(find "$BACKUP_DIR/incoming/archive.tgz" -mmin +60) ]
then
	/usr/local/bin/python /app/healthchecks.py vdjbase-backups -m "$BACKUP_DIR/incoming/archive.tgz not updated"
	exit
else
	echo "$BACKUP_DIR/incoming/archive.tgz updated"
fi

backupsize=$(find "$BACKUP_DIR/incoming/archive.tgz" -printf "%s")

if [ $backupsize -lt 1000 ]
then
	/usr/local/bin/python /app/healthchecks.py vdjbase-backups fail -m "$BACKUP_DIR/incoming/archive.tgz is implausibly small"
	exit
else
	echo "$BACKUP_DIR/incoming/archive.tgz is a reasonable size"
fi

# Cleanup
rm -rf $BACKUP_DIR/temp/*

# Run backup rotate
cd $BACKUP_DIR
bash /app/rotate.sh

/usr/local/bin/python /app/healthchecks.py vdjbase-backups success -m "size $backupsize bytes" 
