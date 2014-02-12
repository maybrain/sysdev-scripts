sysdev-scripts
==============

Various scripts to make life simplier.

pdf2json: 
  Python Script to convert PDF files to JSON base64 file. Using 
  2 versions: simple and incremental
	Simple: USAGE python pdf2json SOURCE TARGET [PAGE] -> Get the pdf SOURCE file on TARGET json file. If PAGE is specified, get only the json of that page.
	Incremental: USAGE python pdf2json SOURCE TARGET PAGE -> Add the pdf SOURCE file PAGE on TARGET json file.
  
procesa:
  Python Script to get the sum of Apache log files traffic stored on s3
  2 Versions: Date on parameters & file folder "Stoned"
		Date on parameters: procesa.py YEAR MONTH -> Mail csv file with the resume of daily traffic of given month
		File Folder "Stoned": procesa_corto.py -> Return csv file on /mnt/resumen_mes.csv with the resume of daily traffic of "stoned" folder (/mnt/aux/)