import sys,os,json
from PyPDF2 import PdfFileWriter, PdfFileReader

def grabar64(par, cadena):
    archi=open(par,'a')
    archi.write(cadena)
    archi.close()

#python p2jinc origen destino pagina
# Si destino no existe, crear con contenido de pagina de origen
# Si destino existe, agregar contenido de pagina de origen { leer json , desbasear, agregar, basear, escribir json }

if not(len(sys.argv)==4 ) : exit(2);

origen =  sys.argv[1]
destino = sys.argv[2]
pagina = sys.argv[3]

input1 = PdfFileReader(file(origen, "rb"))

total = input1.getNumPages()

if os.path.exists(destino):
	json_data=open(destino)
	data = json.load(json_data)
	json_data.close()
	base64origen = data["content"]
	dataorigen = base64origen.decode("base64")
	base = "/tmp/base.pdf"
	grabar64(base, dataorigen)
	input2 = PdfFileReader(file(base, "rb"))
	
	nombre = "/tmp/out.pdf"
	outputStream = file(nombre, "wb")
	output = PdfFileWriter()

	for i in range(input2.getNumPages()):
		output.addPage(input2.getPage(int(i)-1))
	output.addPage(input1.getPage(int(pagina)-1))
	output.write(outputStream)
	outputStream.close()

	a = "{\"content\": \""+open(nombre, "rb").read().encode("base64").replace("\n","")+"\"}"
	os.remove(destino)
	grabar64(destino, a)
	os.remove(nombre)
	os.remove(base)

	
	
else:
	nombre = "/tmp/out.pdf"
	outputStream = file(nombre, "wb")
	output = PdfFileWriter()

	output.addPage(input1.getPage(int(pagina)-1))
	output.write(outputStream)
	outputStream.close()
	a = "{\"content\": \""+open(nombre, "rb").read().encode("base64").replace("\n","")+"\"}"
	grabar64(destino, a)
	os.remove(nombre)
	
exit(0)