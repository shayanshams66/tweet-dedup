import pymongo
import os
import json
import sys
import glob
import time
_decoder = json.JSONDecoder()
Data_base=sys.argv[1]
date = sys.argv[2]
#name of the database
HOST_NAME = "130.39.92.103"
HOST_PORT = 27017
DB_NAME = Data_base
TEMP_COLLECTION_NAME = "temp_deduplication_collection"

deduplicateFileName = "Keywords"

# connect to host
client = pymongo.MongoClient(HOST_NAME, HOST_PORT)
tempCollection = client[DB_NAME][TEMP_COLLECTION_NAME]

# create list of file name for bounding box files
boundingBoxFileNames = glob.glob("/twit-data/"+date+"/tweetdata*/"+date+"_"+Data_base+"/*BB/*.json")
# to extend this list with more bb use extend:
# extend adds elements from list2 to list1
# boundingBoxFileNames.extend(glob.glob(some other path))
nonBoundingBoxFileNames = glob.glob("/twit-data/"+date+"/tweetdata*/"+date+"_"+Data_base+"/Keywords/*.json")
i=0
time1=time.time()
tempCollection.create_index([('id', pymongo.ASCENDING)], unique=True)
for boundingBoxFileName in boundingBoxFileNames:
    # open the file for readin
        h=0
	boundingBoxFile = open(boundingBoxFileName, 'r')
    	for line in boundingBoxFile:
        # convert json string into dictionary object
                try:
        		newDoc = json.loads(line)
        # insert the dictionary as new document
        		tempCollection.insert_one(newDoc)
                	h+=1
                	i+=1
		except pymongo.errors.DuplicateKeyError:
			pass
       #tempCollection.create_index([('id', pymongo.ASCENDING)], unique=True)
	print(("number of imported tweet with BB: %s from file: %s") %(h,boundingBoxFileName)+"\n")
f=open("/twit-data/stats_"+date+"_"+Data_base+".txt","a+")
f.write(("total number of imported tweet with BB: %s") %(i)+"\n")
time2=time.time()
elapsed=time2-time1
f.write(("time for importing tweet with BB: %s") %(elapsed)+"\n")
f.close()
i=0
time1=time1=time.time()
for nonBoundingBoxFileName in nonBoundingBoxFileNames:
    # open file for reading
    nonBoundingBoxFile = open(nonBoundingBoxFileName, 'r')
    h=0
    for line in nonBoundingBoxFile:
                try:
            # try to insert each the new document
 			newDoc = json.loads(line)
			tempCollection.insert_one(newDoc)
                        h+=1
                        i+=1
        # insert failed due to duplicate key error, do nothing.
        	except pymongo.errors.DuplicateKeyError:
            		pass
                #print ("line number: %s" %pos)
    print(("number of imported tweet with keyword: %s from file: %s") %(h,nonBoundingBoxFileName))
f=open("/twit-data/stats_"+date+"_"+Data_base+".txt","a+")
f.write(("total number of imported tweet with Keywords: %s") %(i)+"\n")
time2=time.time()
elapsed=time2-time1
f.write(("time for importing tweet with keywords: %s") %(elapsed)+"\n")
f.close()
collectionNames = tempCollection.distinct("collectionType")
print(collectionNames)
# 1.for each unique collection name
# 2.get all the documents in temp database that matches that collection name
# 3.insert all documents of that name into a output collection
for collectionName in collectionNames:

    outputDocumentsCursor = tempCollection.find( { "collectionType": collectionName })

    # get output collection
    outputCollection = client[DB_NAME][collectionName]
    for doc in outputDocumentsCursor:
        outputCollection.insert_one(doc)

tempCollection.drop()
