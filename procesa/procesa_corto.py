import commands
import glob
import os
import smtplib
import sys

lista = glob.glob('/mnt/aux/*.log*')
#sort glob http://stackoverflow.com/questions/6773584/how-is-pythons-glob-glob-ordered

resumen = open("/mnt/resumen_mes.csv","w")

for fichero in lista:
	pais = fichero.split(".")[0].split("/")[-1]
	fecha = fichero.split("-")[-1]
	#print pais
	trafico = 0
	f = open(fichero)
	for linea in f:
		dato = linea.split(" ")[9]
		if (dato.find('-')!=-1) or dato.find('+')!=-1 or dato.find('/')!=-1: dato = 0
		else: dato = int(linea.split(" ")[9])
		trafico = trafico + dato
	f.close()
	resumen.write(pais+";"+fecha+";"+str(trafico)+"\n")
	
resumen.close()