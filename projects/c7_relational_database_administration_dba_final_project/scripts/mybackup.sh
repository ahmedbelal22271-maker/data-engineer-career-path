#!/bin/bash

mysqldump --all-databases --user=root --password=ِAh22059038!# > all-databases-backup.sql

CURRENT_DATE=$(date +%Y%m%d)

mkdir -p /tmp/mysqldumps/${CURRENT_DATE}

mv all-databases-backup.sql /tmp/mysqldumps/${CURRENT_DATE}/


