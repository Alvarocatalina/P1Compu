import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, render_template, request
import urllib, re 
import time
import json 
import ssl
from pymongo import *
from beebotte import *
bclient = BBT("CZP8S52meXC64tZVn61TdAYq", "au3vFZiUPK6BDGfJyXZ5okgHpVuEjp6a")

while 1:
	time.sleep(120) #suspende la funcion por 120 segundos
	pfecha=time.strftime("%d/%m/%y")#dia mes ano
	phora=time.strftime("%H:%M:%S") #hora minuto y segundo
	url = 'http://www.meneame.net'
	web = urllib.urlopen(url).read()
	pnoticia =re.search('<a\s*href=".*?"\s*class="l:\d*"\s*>(.*?)<\/a>' ,web).group(1)
	pmeneos =int(re.search('(\d+)<\/a>\s*meneos' ,web).group(1))
	pclics =re.search('(\d+)\s*clics',web).group(1)
	
	#Bases de datos Beebotte
	#Meneos y clics son de tipo number, fecha y hora son de tipo any y noticias es de tipo string
	#Escritura de datos persistentes, estos deben estar siempre asociados a un recurso existente
	#Create a resource object bfecha
	bfecha = Resource(bclient,"chnoticias","bfecha")#chnoticias es el canal y bfecha el recurso
	#write to the resource
	bfecha.write(pfecha)
	#Create a resource object bhora
	bhora = Resource(bclient,'chnoticias','bhora')
	#write to the resource
	bhora.write(phora)
	#Create a resource object bnoticia
	bnoticia = Resource(bclient,'chnoticias','bnoticia')
	#write to the resource
	bnoticia.write(pnoticia)
	#Create a resource object bmeneos
	bmeneos = Resource(bclient,'chnoticias','bmeneos')
	#write to the resource
	bmeneos.write(int(pmeneos))
	#Create a resource object bclics
	bclics = Resource(bclient,'chnoticias','bclics')
	#write to the resource
	bclics.write(int(pclics))
	
	#Base de datos local Mongo
	client = MongoClient('localhost',27017)
	db = client.DDBB
	Noticias = db.Noticias

	
	mfecha= pfecha
	mhora = phora
	mnoticia = pnoticia
	mmeneos = int(pmeneos)
	mclics = int(pclics)
	DicMongo = {'fecha': mfecha, 'hora': mhora, 'noticia': mnoticia, 'meneos': mmeneos, 'clics': mclics}
	MongoEntrada = Noticias.insert_one(DicMongo)
	print (2)

