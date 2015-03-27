#!/usr/bin/python

import string
import random
import datetime
import os
import sys

def usage():
	print sys.argv[0] + ' ([--verbose]||[-v]) | ([--help]||-h)\n'
	print 'Options: \n\t verbose: (OPTIONAL) really *REALLY* nerd information about used charset, generation times and random seed. Not very useful for normal use.\n\t help: this help'

if '--help' in sys.argv or '-h' in sys.argv: 
	usage()
	exit(0)

if '--verbose' in sys.argv or '-v' in sys.argv: verbose = True
else: verbose = False

def id_generator(size=6, chars=string.ascii_uppercase):
	a = datetime.datetime.now()
	random.seed = os.urandom(2048)
	b = datetime.datetime.now()
	if verbose:		
		print '\nVERBOSE::::Charset:\n ' + chars
		print '\nVERBOSE::::2048 bytes generation time: ' + str(b-a)
		print '\nVERBOSE::::2048 seed: ' + str(random.seed)
	return ''.join(random.choice(chars) for _ in range(size))

num = raw_input('Byte number to generate : ')
int_tipo = raw_input('Key Charset:\n\t[1]: ASCII UPPERCASE\n\t[2]: ASCII UPPERCASE + lowercase\n\t[3]: ASCII UPPERCASE + lowercase + digits (0..9)\n\t[4]: ASCII UPPERCASE + lowercase + digits (0..9) + Special Characters\n\tDEFAULT (OR FAIL) [1]: ')

enabled = ['1','2','3','4']
if ( int_tipo not in enabled ): int_tipo = '1'

inicio = datetime.datetime.now()
if int_tipo=='1': 
	key = id_generator( size=int(num), chars=string.ascii_uppercase)
	fin = datetime.datetime.now()
elif int_tipo=='2': 
	key = id_generator( size=int(num), chars=string.ascii_uppercase + string.ascii_lowercase)
	fin = datetime.datetime.now()
elif int_tipo=='3': 
	key = id_generator( size=int(num), chars=string.ascii_uppercase + string.ascii_lowercase + string.digits)
	fin = datetime.datetime.now()
elif int_tipo=='4': 
	key = id_generator( size=int(num), chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '!@#$%^&*()')
	fin = datetime.datetime.now()

if verbose: print 'VERBOSE::::Key Generation Time = ' + str(fin - inicio) + '\n'
output = raw_input('Output exit:\n\t[1]: Terminal\n\t[2]: FILE \n\tDEFAULT (OR FAIL) [1]: ')
if output =='2':
	ruta = raw_input ('Key generated. Path to save it : ')
	f = open(ruta,'w')
	f.write(key)
	f.close()
else: print '$$$$$$$$ BEGIN KEY $$$$$$$$\n' +key+'\n$$$$$$$$ END KEY $$$$$$$$'

