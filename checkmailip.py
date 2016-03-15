#!/usr/bin/python

import urllib2
import os
import smtplib
from email.mime.text import MIMEText

def send_mail( ip ):
	fromaddr = 'me@me.org'
	toaddrs  = 'you@you.org'
	subject = 'HOME IP'
	msg = 'Subject: ' +subject+ '\n\nHome New IP ' + ip
	server = smtplib.SMTP('smtp.search_a_server.org:587')
	username = 'jdeacon@openmailbox.org'
	password = '0n3P4ssw0rd'
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()


try:
	my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
except urllib2.URLError ,e:
#	print e
	print 'Error accessing external server: ' + str(e) 
	exit(1)
	
# Only root permissions folder
#ruta = '/etc/public.ip'
# Always working folder
ruta='./public.ip'

if not os.path.exists(ruta):
	f = open(ruta, 'w')
	f.write(my_ip)
	f.close()
	send_mail(my_ip)
else:
	f = open(ruta,'r')
	last_ip = f.readline()
	f.close()
	if last_ip!=my_ip:
		f = open(ruta, 'w')
		f.write(my_ip)
		f.close()
		send_mail(my_ip)
		
