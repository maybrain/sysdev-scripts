import commands
import glob
import os
import smtplib
import sys

#Hola, Obi!!

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def usage():
	print "Parameter error."
	print 'Usage: '+sys.argv[0]+' [anio] [mes]'

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

ruta_root = '/mnt/logs/'

#de momento, paso de parametros y rutas a fuego. No tengo ganas de mas. Octubre 2013.
#mas de Octubre 2013: he sacado un momento y he enchufado el paso de parametros y la funcion de usage()
anio = sys.argv[1]
mes = sys.argv[2]

if (len(sys.argv)!=3): 
	usage()
	sys.exit(2)

#mes = '09'
#anio = '2013'

ruta = ruta_root+'/'+mes+'/'

os.system('mkdir '+ruta)

print commands.getstatusoutput('s3cmd get s3://assets.es.santillanago.com/logs/'+anio+'/'+mes+'/* '+ruta)

os.system('rm -rf '+ruta+'*error*')

lista = glob.glob(ruta+'/*.log*')
#sort glob http://stackoverflow.com/questions/6773584/how-is-pythons-glob-glob-ordered

resumen = open("/tmp/resumen_mes.csv","w")

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
#send_mail(send_from='ignacio.fernandez@inmediastudio.es', send_to=['ignacio.paradisecity@gmail.com','antoniop.deniz@inmediastudio.com'], subject='Resumen trafico '+mes+' '+anio, text= 'Resumen mes '+mes+' '+anio , files=['/tmp/resumen_mes.csv'], server="localhost")

#send_mail(send_from='ignacio.fernandez@inmediastudio.es', send_to='ignacio.paradisecity@gmail.com', subject='Resumen trafico '+mes+' '+anio, text= 'Resumen mes '+mes+' '+anio , files=['/tmp/resumen_mes.csv'], server="localhost")

os.system('rm -rf '+ruta)
os.system('rm -rf /tmp/resumen_mes.csv')

