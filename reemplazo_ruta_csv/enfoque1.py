#!/usr/bin/python

#USAGE 

import os

def contenidos(route):
	print "entra funcion"
        l = []
        for path,dirs,files in os.walk(route):
                for fn in files:
                        l.append(os.path.join(path,fn))
        return l

origen = "./av/platforms/"

print "START!"

#cargar csv estructura en memoria: un diccionario
fich_trad = "./i18ntranslate.csv"
ft = open(fich_trad)
lines = ft.readlines()
ft.close()

dict_trad = {}

for l in lines:
	start = str(l.split(",")[0])
	final = str(l.split(",")[1])
	dict_trad[str(start)] = str(final)

#comprobar rutas!
rutas = contenidos(origen)
tot = len(rutas)

print tot

# recorrer ficheros de rutas linea a linea. Si la linea tiene la cadena de la key dict_trad[str(origen)], cambiarla por el value dict_trad[str(origen)]
# discriminar extensiones? NO

keys = dict_trad.keys()
pos = 1

#for j in keys: print dict_trad[j]

for r in rutas:
	print str(pos)+"/"+str(tot)+": "+str(r)
	change = False
	if r.find(".hbc")!=-1 or r.find(".js")!=-1:
		print "CANDIDATO"
		fr = open(r)
		linesr = fr.readlines()
		fr.close()

		for l in linesr:
			for k in keys:
#				print str(pos)+"/"+str(tot) + " :" +str(l) + "//" +str(k)
				if str(l).find(k)!=-1:
					print "Cambia " + str(k) + " // " + str( [dict_trad[str(k)]] )
					change=True
					l.replace(str(k), str( [dict_trad[str(k)]] ) )

		if change:
			print str(pos)+"/"+str(tot)  +": cambio en " + str(r)
			#sobrescribir fichero con contenido de linesr
			fr = open(r, "w")
			for l in linesr:
				fr.write(str(l)+"\n")
			fr.close()
	pos = pos + 1

print "END!"
