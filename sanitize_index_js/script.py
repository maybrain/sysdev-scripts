#!/usr/bin/python

import datetime

def ahora():
        return str(datetime.datetime.now())

#searchline = '["style", "-webkit-transform-origin", '
searchline = '", "-webkit-transform-origin", '
terceravariable = '-webkit-transform-origin'
legitline = 'transform-origin'

print ahora() + " begin"

origen = 'rutas.txt'

forigen = open(origen)
lorigen = forigen.readlines()
forigen.close()


for line in lorigen:
        change = False;
        mac = False
        fline = open(line.strip("\n"))
        lines = fline.readlines()
        #print line + ' ' + str(len(lines))
        #lines = aux.splitlines()
        fline.close()
        if len(lines)==1:
                #print "MAC " + line
                aux = str(lines[0]).split("\r")
                lines = aux
                mac = True
        i = 0
        for l in lines:
                #print str(i) + " " +  str(l.find(searchline)) + ": " + str(l)
                if l.find(searchline)!=-1:
                        #print ahora() + " " + str(line)+" "+str(l) +" encuentra!"
                        lines.insert(i+1, lines[i].replace(terceravariable,legitline) )
                        change = True
                i = i + 1
        #escribe lines en line
        if change:
                fline = open(line.strip("\n"),"w")
                for l in lines:
                        if mac:
                                fline.write(l+'\n')
                        else:
                                fline.write(l)
                        #print "kk"
                fline.close()

print ahora() + " end!"