sysdev-scripts
==============

Various scripts to make life simplier.

<b>pdf2json</b>:<br /> 
  Python Script to convert PDF files to JSON base64 file. Using 
  2 versions: simple and incremental <ul><li>
	Simple: USAGE <i>python pdf2json SOURCE TARGET [PAGE]</i> -> Get the pdf SOURCE file on TARGET json file. If PAGE is specified, get only the json of that page.</li><li>
	Incremental: USAGE <i>python pdf2json SOURCE TARGET PAGE</i> -> Add the pdf SOURCE file PAGE on TARGET json file.</li></ul>
  
<b>procesa</b>:<br />
  Python Script to get the sum of Apache log files traffic stored on s3.<br />
  2 Versions: Date on parameters & "Stoned" file folder <ul><li>
		Date on parameters: <i>procesa.py YEAR MONTH</i> -> Mail csv file with the resume of daily traffic of given month</li><li>
		Stoned file folder: procesa\_corto.py: Return csv file on /mnt/resumen_mes.csv with the resume of daily traffic of "stoned" folder (/mnt/aux/)</li></ul>
		
<b>cron_factoria</b>:<br />
Python Script to connect various DB on various servers in order to select data and insert them on a local DB. No parameters.

<b> reemplazo_csv </b>
* __enfoque1.py__: parsear csv a dict, recorrer rutas, filtrar tipo, si tipo -> recorrer lineas y cruzar linea con find de clave de dict con valor de clave: NO FUNCIONA CORRECTAMENTE

* __enfoque2.py__: parsear csv a dict, por cada clave de dict abrir rutas, filtro tipo 1 + filtro tipo 2, recorrer lineas, reemplazar clave de dict por clave por linea.

* __reemplazo.py__: pruebas de carga del csv -> dict

<b> montaje_win </b>
* __montaje_win.py__: recuperar rutas fichero HTML cada 15 minutos por tarea programada. Si existe, se coge zip de la primera, se descarga por wget, se descomprime, se pasa por el empaquetador y se sube por FTP a la segunda ruta
* __empaquetador.bat__: Magia de Gasca para empaquetar AV para windows

<b>generate_key.py</b>
* Interactive program to generate strong random (random.seed = os.urandom(2048) n bytes using different charset selected by the user. Asks the number of bytes to output, the charset to use and the output format (save to file or show on terminal)
* Parameter -v || --verbose: shows info (<b>REALLY NERD INFO</b>, you're warned) about used charset, generation times and random seed. Not very useful for normal use.

<b>script_chop_tables.sh</b>

Need to recover LAAAAAAAARGE mysql dump file in order to get a tiny table?  This one is for you.

Two modes: 
* ./script_chop_tables.sh DUMP_FILE.SQL
   Dumps all tables onto separate sql files
* ./script_chop_tables.sh DUMP_FILE.SQL table
   Dumps only specified table on one sql file

Holaaaaaa
