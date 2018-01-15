#!/bin/bash
##Aded by Shayan to import collected tweets every day at 11:59 pm
DATE=`date +%Y-%m-%d`
ex_date=$(date --date="${DATE} -1 day" +%Y-%m-%d)
Root=/twit-data
stat=$Root/stats_
###check if the stats file exists:
echo $DATE
echo $ex_date
stat+=$ex_date
temp=`echo $stat"_Disaster.txt"`
if [ -f $temp ]; then
    for file in $stat*;
        do
        python daily-stat-parse.py $file
        done
    source /opt/software/twitter/bin/activate
    cd /opt/software/twitter_website
    python manage.py shell < stats/importcsv-disaster.py
    python manage.py shell < stats/importcsv-lsu.py
else
    sleep 10m
fi

