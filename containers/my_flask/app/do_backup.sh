#!/bin/bash
#@author Julius Zaromskis
#@description Backup script for your website

BACKUP_DIR=/backup
TEMP_DIR=/tmp

# Precautionary cleanup
mkdir -p $BACKUP_DIR/incoming
mkdir -p $BACKUP_DIR/temp
mkdir -p $BACKUP_DIR/backup.daily
mkdir -p $BACKUP_DIR/backup.weekly
mkdir -p $BACKUP_DIR/backup.monthly
rm $BACKUP_DIR/incoming/*
rm -rf $BACKUP_DIR/temp/*

# Dump MySQL tables
mysqldump --all-databases -h mariadb -P 3306 -u root -pgsdfgtwevdfg >/config/log/sqldump

# Backup logs and config
cp -r /config/*  $BACKUP_DIR/temp/.

cd $BACKUP_DIR/temp

# Compress tables and files
tar -cvzf $BACKUP_DIR/incoming/archive.tgz *

# Cleanup
rm -rf $BACKUP_DIR/temp/*

# Run backup rotate
cd $BACKUP_DIR
bash /app/rotate.sh
