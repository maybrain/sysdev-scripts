#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import ftplib
import subprocess
import os
import socket
import zipfile
import shutil


""" COLORINES! """
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_INTENSITY = 0x08 # text color is intensified.

FOREGROUND_BLACK    = 0x0000
FOREGROUND_BLUE    = 0x0001
FOREGROUND_GREEN    = 0x0002
FOREGROUND_RED    = 0x0004
FOREGROUND_PURPLE    = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_WHITE    = 0x0007
FOREGROUND_GRAY    = 0x0008
FOREGROUND_GREY    = 0x0008
FOREGROUND_AQUA    = 0x0009 #Very Blue

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED  = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.

import ctypes

std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_color(color, handle=std_out_handle):
    """(color) -> BOOL
    
    Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    """
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
# set_color

""" END COLORINES """

def zipdir(source_dir, output_filename):
	shutil.make_archive(output_filename, 'zip', source_dir)

path = 'C:\\windows\\temp\\'
ruta_bat = "C:\\Users\\UsuarioDell07\\Desktop\\Empaquetador.bat"
url = "http://inmediadevelop.com/entregas/pkgwin.txt"

# 1) acceder url, recoger lineas, descargar (wget?) un zip

contents_url = urllib2.urlopen(url).read()
#FORMATO contents_url
#	ORIGEN = http://inmediadevelop.com/entregas/aula_virtual_v1.7.19_win.zip
#	DESTINO = entregas/aula_virtual_v1.7.19_win.zip
origen = contents_url.split('\n')[0].split('=')[1].lstrip()
destino = contents_url.split('\n')[1].split('=')[1].lstrip()
print 'Origen: '+origen
print 'Destino: '+destino
#1b) descargar zip en lineas de content_url

urllib.urlretrieve (origen, path+"origen.zip")

print '\nDescargado en: '+str(path)+'origen.zip'

# 2) descomprimir zip OS WINDOWS??? Libreria

z = zipfile.ZipFile(str(path)+'origen.zip')
z.extractall(path=path+'origen')
z.close()

print '\nExtraido en: '+str(path)+'origen'

# 3) meter origen nw.exe nw.pak EN carpeta
dest = "C:\\Users\\UsuarioDell07\\Desktop\\COPIA AQUI NW\\"
shutil.copy(path+'origen\\aulavirtual\\nw.exe',dest)
shutil.copy(path+'origen\\aulavirtual\\nw.pak',dest)

print '\nArchivos metidos! '

# 4) llamar bat

subprocess.Popen([ruta_bat]).wait()
result_folder = "C:\\Projects\\WrapperNodeWebkit\\Aula Virtual\\BuildResults"

print '\nFin del batch! '
# 5) zip de 4) más carpeta  OS WINDOWS??? Librería
destinob = path + str(destino.split("/")[1])
print "Destino B: "+ destinob
#zipf = zipfile.ZipFile(destinob, 'w')
#zipf = str(destinob.split('.')[0:-1])
zipf = str(destinob[0:destinob.rfind('.')])
zipdir(result_folder, zipf)
#zipf.close()

print "Zip creado en " +str(destinob)

# 6) poner 5 en servidor FTP
try:
	ftp = ftplib.FTP(host='ftp.inmediadevelop.com', user='inmediadevelop', passwd='dxjjfqly')
	print "Entra CONEXION FTP"
	ftp.cwd('entregas')
	size = os.path.getsize(destinob)
	f = open(destinob,'rb')
	print "Voy a subir " + str(destino.split("/")[1]) + " desde " + str(destinob) + " SIZE: " + str(size)
	ftp.set_pasv(True);
	ftp.storbinary(cmd='STOR '+ str(destino.split("/")[1]), fp=f)
	f.close()
	size_ftp = ftp.size(str(destino.split("/")[1]))
	if size!=size_ftp:
		print bcolors.FAIL +"Tamano disco = " + str(size) +" Tamano FTP = " + str(size_ftp) + bcolors.END
	else: print "Comprobacion tamano correcta"
	print "Subido FTP"	
	ftp.delete('pkgwin.txt')
	print "Borrado fichero origen FTP"
	ftp.quit()
	print "Cerrado FTP"
except socket.gaierror, e:
	set_color(FOREGROUND_RED)
	print ' ERROR:::: CONEXION FTP SERVER CAIDO '
	set_color(FOREGROUND_WHITE)
	print repr(e)
except ftplib.error_perm, e:
	set_color(FOREGROUND_RED)
	print bcolors.FAIL + ' ERROR:::: CONEXION FTP CREDENCIALES ' 
	set_color(FOREGROUND_WHITE)
	print repr(e) 


# 7) borrar mierdas
os.remove(path+"origen.zip")
os.remove(destinob)
shutil.rmtree(path+"origen")

set_color(FOREGROUND_GREEN)
print '\n\nTo guay.'
set_color(FOREGROUND_WHITE)
