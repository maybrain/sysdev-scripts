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
