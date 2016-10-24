# Curso BigData & Data Analytics by grupo6
# Fecha: Marzo-2016
# Descripcion: Programa que cosecha tweets desde la API de twitter usando tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
import tweepy
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON
import redis


CONSUMER_KEY = "CONSUMER_KEY_V"
CONSUMER_SECRECT = "CONSUMER_SECRECT_V"
ACCESS_TOKEN = "ACCESS_TOKEN_V"
ACCESS_SECRECT = "ACCESS_SECRECT_V"
QUITO_CODE = 375732
QUITO_CENTRO = [-78.565979,-0.238265,-78.410797,-0.101623]

r = redis.StrictRedis(host='localhost', port=6379, db=0)
key_redis = "bg:g6:v1:indexme:quito_centro"
twitterKeys = "twitterKeys.json"
with open(twitterKeys) as data_file:    
    keys = json.load(data_file)

if (len(keys) == 14):
    class listener(StreamListener):
        
        def on_data(self, data):
            dictTweet = json.loads(data)
            try:
                dictTweet["_id"] = str(dictTweet['id'])
                #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
                #a guardar en documento en la base de datos
                doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
                r.lpush(key_redis, dictTweet["_id"])
                print "Guardado " + "=> " + dictTweet["_id"]
            except:
                print "Documento ya existe"
                pass
            return True
        
        def on_error(self, status):
            print status
            
    auth = tweepy.OAuthHandler(keys[CONSUMER_KEY], keys[CONSUMER_SECRECT])
    auth.set_access_token(keys[ACCESS_TOKEN], keys[ACCESS_SECRECT])
    twitterStream = Stream(auth, listener())

    #Setear la URL del servidor de couchDB
    server = couchdb.Server('http://localhost:8080/')
    # server.resource.credentials = (keys["COUCH_USER"], keys["COUCH_PASSWORD"])
    try:
        #Si no existe la Base de datos la crea
        db = server.create('quito_centro')
    except:
        #Caso contrario solo conectarse a la base existente
        db = server['quito_centro']
        
    #Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
    #twitterStream.filter(track=['pokemon'])
    

    twitterStream.filter(locations=QUITO_CENTRO)

else:
    print("Unable to read twitterKeys.json")
