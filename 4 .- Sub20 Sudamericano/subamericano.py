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
ckey = "4M3IxhBGcG1xWRaEYSPzdHsR5"
csecret = "OmqgQkuXLjy0HMDYJiX4VsSeEzW8QjDVJVzCSGXiTXmTuHXKfX"
atoken = "801538084529729536-2ZuQKfkv4yQzycbz0MGLEcMV6OPbOxr"
asecret = "H5SsW66bdKZLBDuGg43TYWK6mfl7gr1byM7JaCFrQFeqw"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('subameircacon')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['subameircacon']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
#twitterStream.filter(locations=[31.214956,30.008375,31.301973,30.110602])
twitterStream.filter(track=['sudamericano','futbool','football','soccer','Sub20'])
#twitterStream.filter(track=['ecuador','cynthia viteri'])
