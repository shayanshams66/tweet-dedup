#!/bin/bash
ps -ef | grep GetTweets | grep -v grep | awk '{print $2}' | xargs -r kill -9


tmrw_date=$(date --date="${DATE} +1 day" +%Y-%m-%d)
dir="/twit-data/$tmrw_date"

while true; do
  if [ -d $dir ]; then
    sleep 2m
    java -jar /home/hadoopcd/GetTweets/gettweets1.0.1.jar /home/hadoopcd/GetTweets/config.yaml &
    break
  else
    sleep 1
  fi
done

