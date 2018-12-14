import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, render_template, request
import urllib, re 
import ssl
import time
import json 
from beebotte import *
from pymongo import *
import numpy as np

app = Flask(__name__)
bclient = BBT("CZP8S52meXC64tZVn61TdAYq", "au3vFZiUPK6BDGfJyXZ5okgHpVuEjp6a")# BBT(API Key, Secret Key)
flag = 0

@app.route('/')
def inicio():
	client = MongoClient('localhost',27017)
	db = client.DDBB
	Noticias = db.Noticias
	resumbral=Noticias.find().sort([('fecha',DESCENDING),('hora',DESCENDING)])
	for entry in resumbral:
		pfecha=str(entry['fecha'])
		phora=str(entry['hora'])
		pnoticia=str(entry['noticia'])
		pmeneos=str(entry['meneos'])
		pclics=str(entry['clics'])
		break
	return render_template('paginaweb.html',wfecha=str(pfecha),whora=str(phora),wtitulo=str(pnoticia),wmeneos=str(pmeneos),wclics=str(pclics))

@app.route('/media',methods=['GET'])
def media():
	client = MongoClient('localhost',27017)
	db = client.DDBB
	Noticias = db.Noticias
	resumbral=Noticias.find().sort([('fecha',DESCENDING),('hora',DESCENDING)])
	for entry in resumbral:
		pfecha=str(entry['fecha'])
		phora=str(entry['hora'])
		pnoticia=str(entry['noticia'])
		pmeneos=str(entry['meneos'])
		pclics=str(entry['clics'])
		break
	meanclics = []
	global flag
	if flag == 0 :
		client = MongoClient('localhost',27017)
		db = client.DDBB
		Noticias = db.Noticias
		MSumClics = Noticias.find()
		for entry in MSumClics:
			meanclics.append(entry['clics'])
		flag = 1
		MMClics = "{0:.2f}".format(np.mean(meanclics))
		return render_template('paginaweb.html',wfecha=str(pfecha),whora=str(phora),wtitulo=str(pnoticia),wmeneos=str(pmeneos),wclics=str(pclics),wmmongo=str(MMClics))
	else :		
		BSumClics = bclient.read('chnoticias', 'bclics')
		for entry in BSumClics:
			meanclics.append(entry['data'])
		flag = 0
		BMClics = "{0:.2f}".format(np.mean(meanclics))
		return render_template('paginaweb.html',wfecha=str(pfecha),whora=str(phora),wtitulo=str(pnoticia),wmeneos=str(pmeneos),wclics=str(pclics),wmbeebotte=str(BMClics))

@app.route('/umbral',methods=['POST'])
def umbral():
	if request.method == "POST":
		umbral=request.form.get("wumbral")
		a=umbral.isdigit()
		if a==True:
			rnoticiaanterior="alvarocatalina"
			i=10
			entrada = ""
			client = MongoClient('localhost',27017)
			db = client.DDBB
			Noticias = db.Noticias
			resumbral=Noticias.find().sort([('fecha',DESCENDING),('hora',DESCENDING)])
			numnoticias=1
			for entry in resumbral:
				if entry['clics'] > int(umbral) and entry['noticia']!= rnoticiaanterior:
					pfecha=str(entry['fecha'])
					phora=str(entry['hora'])
					ptitulo=str(entry['noticia'])
					pmeneos=str(entry['meneos'])
					pclics=str(entry['clics'])
					rnoticiaanterior=ptitulo
					entrada = entrada + '<tr><td align="center">'+pfecha+'</td> <td align="center">'+phora+'</td><td align="center">'+ptitulo+'</td><td align="center">'+pmeneos+'</td><td align="center">'+pclics+'</td></tr>'
					numnoticias += 1
					if numnoticias > 10 :
						break
			if rnoticiaanterior=="alvarocatalina":
				error='<font color="#FF0000" face="arial, verdana, helvetica"  > <b>No hay noticias que superen este umbral</b> </font>'
				return render_template('pagina2.html',w2umbral=str(umbral),wm2error=str(error))
			else:
				return render_template('pagina2.html',w2umbral=str(umbral),wresultado=str(entrada))
		else:
			client = MongoClient('localhost',27017)
			db = client.DDBB
			Noticias = db.Noticias
			resumbral=Noticias.find().sort([('fecha',DESCENDING),('hora',DESCENDING)])
			for entry in resumbral:
				pfecha=str(entry['fecha'])
				phora=str(entry['hora'])
				pnoticia=str(entry['noticia'])
				pmeneos=str(entry['meneos'])
				pclics=str(entry['clics'])
				break
			error='<font color="#FF0000" face="arial, verdana, helvetica"  > <b>El valor del umbral debe ser entero y positivo</b> </font>'
			return render_template('paginaweb.html',wfecha=str(pfecha),whora=str(phora),wtitulo=str(pnoticia),wmeneos=str(pmeneos),wclics=str(pclics),wmerror=error)
	
if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=80)
