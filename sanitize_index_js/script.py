#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

def ahora():
	return str(datetime.datetime.now())

searchline = '["style", "-webkit-transform-origin", '
terceravariable = '-webkit-transform-origin'
legitline = 'transform-origin'

print ahora() + " begin"

origen = 'rutas.txt'

forigen = open(origen)
lorigen = forigen.readlines()
forigen.close()

for line in lorigen:
	change = False;
	fline = open(line)
	lines = fline.readlines()
	fline.close()
	i = 0
	for l in lines:		
		#print str(i) + " " +  str(l.find(searchline)) + ": " + str(l)
		if l.find(searchline)!=-1:
		 	print ahora() + " encuentra!"
		 	lines.insert(i+1, lines[i].replace(terceravariable,legitline) )
		 	change = True
		i = i + 1
	#escribe lines en line
	if change:
		fline = open(line,"w")
		for l in lines:
			fline.write(l)
		fline.close()

print ahora() + " end!"

# for i in `cat /home/ubuntu/rutas_edge_archivos.txt`
# do 
# echo $i
# grep -n "\-webkit\-transform\-origin" $i 
# done > /home/ubuntu/archivitoconwebkits.txt  &