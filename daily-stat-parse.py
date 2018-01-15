import glob
import sys
import json
#a version of this exists in the email script to add a new line to stats_history.json
#get yesterdays date 
#get list of all statfiles from yesterday
#statFiles = glob.glob("/twit-data/stats_*_*.txt")
#statFiles.sort()
db_dic={}
daily_stat={}
keyword_number=0
BB_number=0
file=sys.argv[1]
print file
#for file in statFiles:
db_name = file.split("_")[-1].split(".")[0]
db_dic["date"]=file.split("_")[1]
db_dic["db_name"]=db_name
db_dic["db_stat"]={}
#daily_stat["date"]=file.split("_")[1]
#file="stats_2018-01-11_Disaster.txt"
with open ("/twit-data/"+db_name+".json","w") as dest:
        for line in open(file, 'r'):
            if 'from file' in line:
                splitline = line.split(":")
                number = int(splitline[1].split(" ")[1])
                type = splitline[-1].split("_")[-1].split(".")[0]
                db_dic["db_stat"]["collection"+type+"tweet_number"]=number
                #db_dic["db_stat"]["collection tweet_number"]=number
                if "BB" in type:
		    BB_number+=number
	        else: 
		    keyword_number+=number
        json.dump(db_dic,dest)
        dest.write('\n')
        #daily_stat["BB_number"]=BB_number
        #daily_stat["keyword_number"]=keyword_number
        #total=(keyword_number+BB_number)
        #daily_stat["total_tweet"]=total
        #json.dump(daily_stat,dest)
        #dest.write('\n')
