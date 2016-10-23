import couchdb #Libreria de CouchDB (requiere ser instalada primero)
import json #Libreria para manejar archivos JSON
import re

nombre = "Quito";
twitterKeys = "twitterKeys.json"
min_words=5
with open(twitterKeys) as data_file:    
    keys = json.load(data_file)

def initCouchInstance(url, user, password):
	server = couchdb.Server(url)
	server.resource.credentials = (user, password)
	return server


def readTweets(dbName):
	serverInstance = initCouchInstance('http://localhost:8080/', keys["COUCH_USER"], keys["COUCH_PASSWORD"])
	db = serverInstance[dbName]
	idTweetsList = []
	for id in db:
		idTweetsList.append(id)

	tweet = db[idTweetsList[0]]

	try:
		dbClean = serverInstance.create('quitoclean')
	except:
		dbClean = serverInstance['quitoclean']

	for idTweet in idTweetsList:
		currentTweet = db[idTweet]
		if('place' in currentTweet):
			if(currentTweet["place"]):
				if(currentTweet["place"]["name"]):
					print currentTweet["place"]["name"]
					print idTweet
					if(currentTweet["place"]["name"] == nombre):
						print "from quito"
						text = re.sub(r'(https?://\S+)', '', currentTweet["text"])
						score = currentTweet["favorite_count"] + currentTweet["retweet_count"]
						if len(re.split(r'[^0-9A-Za-z]+', text)) > min_words:
							currentTweet.pop('_rev', None)
							currentTweet["score"] = score
							try:
								print currentTweet["place"]["name"]
								dbClean.save(currentTweet)
							except:
								print "Error conflict rev"
	
	

	
	


readTweets("quito_sur")
readTweets("quito_norte")
readTweets("quito_centro")


