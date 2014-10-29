#!/usr/bin/python

#USAGE 

import os, fnmatch

def findReplace(directory, find, replace, filePattern):
#USAGE
#findReplace("some dir", "find this", "replace with this", "*.txt")
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            if s.find(find)!=-1:print "HIT! en " +str(filepath) 
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

origen = "./av/platforms/"
patron = ["*.js","*.hbc"]

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

# recorrer ficheros de rutas linea a linea. Si la linea tiene la cadena de la key dict_trad[str(origen)], cambiarla por el value dict_trad[str(origen)]
# discriminar extensiones? NO

keys = dict_trad.keys()
tot_keys = len(keys)
pos = 1

#for j in keys: print dict_trad[j]

for k in keys:
	print str(pos)+"/"+str(tot_keys)+" ::pasada " + str(k) + " por " +str( dict_trad[str(k)] )
	for p in patron:
		findReplace(origen, str(k), str( dict_trad[str(k)] ), str(p))
	pos = pos +1

print "END!"
