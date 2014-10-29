#!/usr/bin/python

#USAGE 

import os

def contenidos(route):
        l = []
        for path,dirs,files in os.walk(route):
                for fn in files:
                        l.append(os.path.join(path,fn))
        return l

origen = "./i18ntranslate.csv"


#cargar csv estructura en memoria: un diccionario
fich_trad = ".csv"
ft = open(fich_trad,"r")
lines = ft.readlines()
ft.close()

dict_trad = {}

for l in lines:
	origen = str(l.split(",")[0])
	final = str(l.split(",")[1])
	dict_trad[str(origen)] = str(final)

#comprobar rutas!
rutas = contenidos(origen)
tot = len(rutas)

# recorrer ficheros de rutas linea a linea. Si la linea tiene la cadena de la key dict_trad[str(origen)], cambiarla por el value dict_trad[str(origen)]
# discriminar extensiones? NO

keys = dict_trad.keys
pos = 1

for r in rutas:
	print str(pos)+"/"+str(tot)
	change = False
	fr = open(r,"r")
	linesr = ft.readlines()
	fr.close()

	for l in linesr:
		for k in keys:
			if str(l).find(k)!=-1:
				#cambia
				change=True
				l.replace(str(k), str(dict_trad(k)))

	if change:
		#sobrescribir fichero con contenido de linesr
		fr = (r, "w")
		for l in linesr:
			ft.write(str(l)+"\n")
		fr.close()
	pos = pos + 1