#!/bin/bash
##Aded by Shayan to import collected tweets every day at 11:59 pm
DATE=`date +%Y-%m-%d`
Root=/twit-data
###check if the date-folder exists:
tmrw_date=$(date --date="${DATE} +1 day" +%Y-%m-%d)
mkdir $Root/$tmrw_date
sleep 2m
date_folder=$Root/$DATE
if [ -d "$date_folder" ]; then
  cd $date_folder
  for server_id in $(ls) ;
  do
      cd $date_folder/$server_id
      for db_id in $(ls) ;
      do
        cd $date_folder/$server_id/$db_id
        for collection_id in $(ls) ;
        do
          for raw_file in $date_folder/$server_id/$db_id/$collection_id/*.json ; 
          do
          
              mongoimport --host 130.39.92.103 --db $db_id --collection $collection_id --file $raw_file
          done
        done
      done
  done
   cd $Root
   tar -cvf $DATE.tar.gz $DATE
   echo $Root/$DATE.tar.gz $Root/$DATE
   rm -rf $Root/$DATE
fi


