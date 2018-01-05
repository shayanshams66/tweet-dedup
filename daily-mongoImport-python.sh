#!/bin/bash
##Cron Job Aded by Shayan to import collected tweets every day at 11:59 pm
DATE=`date +%Y-%m-%d`
Root=/twit-data
###check if the date-folder exists:
tmrw_date=$(date --date="${DATE} +1 day" +%Y-%m-%d)
mkdir $Root/$tmrw_date
sleep 2m
date_folder=$Root/$DATE
db_array=()
if [ -d "$date_folder" ]; then
  cd $date_folder
  for server_id in $(ls) ;
  do
      cd $date_folder/$server_id
      for db_id in $(ls) ;
      do        
	db_array+=(`echo $db_id | cut -d '_' -f2`)
      done
  done
  db_set=`tr ' ' '\n' <<< "${db_array[@]}" | sort -u | tr '\n' ' '`
  for db in $db_set;
  do
     python dedup.py $db $DATE
     #echo $db
 done 
   cd $Root
   tar -cvf $DATE.tar.gz $DATE
   echo $Root/$DATE.tar.gz $Root/$DATE
   rm -rf $Root/$DATE
fi


