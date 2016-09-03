# Curso BigData & Data Analytics by Handytec
# Fecha: Marzo-2016
# Descripcion: Programa que cosecha tweets desde la API de twitter usando tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
CONSUMER_KEY = "ppB0z1Og0fLuY7BgyhA4CZF6D"
CONSUMER_SECRECT = "zVsworsXDEJruStwrLFzL0vwLMAYa1lv71hYGPveNWrgCQuoKu"
ACCESS_TOKEN = "414709805-W003Fimha42AQCEUK8I3m76ECYPjpbrgwQKi7GhW"
ACCESS_SECRECT = "4CMyBr4hFVTOntq2w7yBoGWCKxNiGJQzLpSpB2mkzGYIz"
#####################################

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
        
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRECT)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRECT)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('quito_sur')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['quito_sur']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(track=['pokemon'])
QUITO_SUR = [-78.585205,-0.393391,-78.430023,-0.213546]
ENTIDADES_PUBLICAS = ["ECU911Quito", "PoliciaEcuador", "BomberosQuito"]

twitterStream.filter(locations=QUITO_SUR)  