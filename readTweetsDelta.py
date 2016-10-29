import couchdb #Libreria de CouchDB (requiere ser instalada primero)
import json #Libreria para manejar archivos JSON
import re
import redis

nombre = "Quito";
twitterKeys = "twitterKeys.json"
min_words=5
key_redis_base = "bg:g6:v1:indexme:"


r = redis.StrictRedis(host='localhost', port=6379, db=0)

with open(twitterKeys) as data_file:    
    keys = json.load(data_file)

def initCouchInstance(url):
	server = couchdb.Server(url)
	# server.resource.credentials = (user, password)
	return server

def readRedisIds(key):
	lastRedisList = []
	lenIdsByKey = r.llen(key)
	for i in range(lenIdsByKey):
		lastRedisList.append(r.rpop(key))
	return lastRedisList

def readTweets(dbName):
	# serverInstance = initCouchInstance('http://localhost:8080/', keys["COUCH_USER"], keys["COUCH_PASSWORD"])
	serverInstance = initCouchInstance('http://localhost:8080/')
	db = serverInstance[dbName]

	idTweetsList = readRedisIds(key_redis_base + dbName)
	print idTweetsList
	try:
		dbClean = serverInstance.create('quitoclean')
	except:
		dbClean = serverInstance['quitoclean']

	for idTweet in idTweetsList:
		currentTweet = db[idTweet]
		if('place' in currentTweet):
			if(currentTweet["place"]):
				if(currentTweet["place"]["name"]):
					print idTweet
					if(currentTweet["place"]["name"] == nombre):
						print "from quito"
						text = re.sub(r'(https?://\S+)', '', currentTweet["text"])
						score = currentTweet["favorite_count"] + currentTweet["retweet_count"]
						if len(re.split(r'[^0-9A-Za-z]+', text)) > min_words:
							currentTweet.pop('_rev', None)
							currentTweet["score"] = score
							try:
								dbClean.save(currentTweet)
								print "Guardado " + "=> " + currentTweet["_id"]
							except:
								print "Error conflict rev"

readTweets("quito_sur")
readTweets("quito_norte")
readTweets("quito_centro")



