import sys,os
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader

def grabar64(par, cadena):
    archi=open(par,'a')
    archi.write(cadena)
    archi.close()

#python pdf2json origen destino [pagina]

if not(len(sys.argv)==4 or len(sys.argv)==3) : exit(2);

origen = sys.argv[1]
destino = sys.argv[2]

input1 = PdfFileReader(file(origen, "rb"))
if os.path.exists(destino): os.remove(destino)

if len(sys.argv)==4 :
pagina = sys.argv[3]
if int(pagina)<=input1.getNumPages():
output = PdfFileWriter()
output.addPage(input1.getPage(int(pagina)-1))
nombre = "/tmp/"+ pagina +".pdf"
outputStream = file(nombre, "wb")
output.write(outputStream)
outputStream.close()
a = "{\"content\": \""+open(nombre, "rb").read().encode("base64").replace("\n","")+"\"}"
grabar64(destino, a)
os.remove(nombre)
else: exit(3)
else:
nombre = "/tmp/"+datetime.now().strftime("%Y%m%d%H%M%S%f")+".pdf"
outputStream = file(nombre, "wb")
output = PdfFileWriter()
total = input1.getNumPages()

for i in range (input1.getNumPages()):
print str(i) +" de " + str(total)
output.addPage(input1.getPage(i))

output.write(outputStream)
outputStream.close()

a = "{\"content\": \""+open(nombre, "rb").read().encode("base64").replace("\n","")+"\"}"
grabar64(destino, a)
os.remove(nombre)