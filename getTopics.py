#!/usr/bin/python
# -*- coding: utf-8 -*-
import couchdb #Libreria de CouchDB (requiere ser instalada primero)
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
import json #Libreria para manejar archivos JSON

CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRECT = "CONSUMER_SECRECT"
ACCESS_TOKEN = "ACCESS_TOKEN"
ACCESS_SECRECT = "ACCESS_SECRECT"
QUITO_CODE = 375732

twitterKeys = "twitterKeys.json"
with open(twitterKeys) as data_file:    
    keys = json.load(data_file)

if (len(keys) == 4):
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(keys[CONSUMER_KEY], keys[CONSUMER_SECRECT])
    auth.set_access_token(keys[ACCESS_TOKEN], keys[ACCESS_SECRECT])
    api = tweepy.API(auth)
    trends1 = api.trends_place(QUITO_CODE)

    data = trends1[0] 
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends]
    # put all the names together with a ' ' separating them
    trendsName = ','.join(names)

    class listener(StreamListener):
        
        def on_data(self, data):
            dictTweet = json.loads(data)
            try:
                print(dictTweet['text'])
                dictTweet["_id"] = str(dictTweet['id'])
                #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
                #a guardar en documento en la base de datos
                doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
                print "Guardado " + "=> " + dictTweet["_id"]
            except:
                print "Documento ya existe"
                pass
            return True
        
        def on_error(self, status):
            print status


    #Setear la URL del servidor de couchDB
    server = couchdb.Server('http://127.0.0.1:5984/')
    try:
        #Si no existe la Base de datos la crea
        db = server.create('topics')
    except:
        #Caso contrario solo conectarse a la base existente
        db = server['topics']

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=[trendsName])
else:
    print("Unable to read twitterKeys.json")

