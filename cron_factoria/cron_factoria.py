#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import datetime
import logging
import cgi
logging.basicConfig(filename='/var/log/factoria.log',level=logging.DEBUG)

html_escape_table = {
# "&": "&amp;",
# '"': "&quot;",
 "'": "&apos;",
# ">": "&gt;",
# "<": "&lt;",
 }

def html_escape(text):
	return "".join(html_escape_table.get(c,c) for c in text)

def ahora():
	return str(datetime.datetime.now())

start = datetime.datetime.now()
logging.debug(ahora() + " BEGIN!!!! ")
#Sacar cadenas de conexión de todas las instancias y meterlas en un diccionario 
# conn = {'pais':['servidor','usuario','pass','database']}
# Alex propone otra BD con una tabla con los datos de conexion. De momento tiro....
# '':['','','',''],
conn_dict = {
'es':['10.228.98.29','SantillanaGOES','pg3Zga9YTb','SantillanaGOES',2],
'richmondmx':['10.33.154.74','SantillanaGOrich','gjXKbpFGcb','SantillanaGOrich',8],
'modernabr':['177.71.137.46','SGO_modernabr','oGhei3sher','SGO_modernabr',9],
'richmondbr':['177.71.137.46','SGO_richmondbr','oGhei3sher','SGO_richmondbr',10],
'mx':['10.33.154.74','SantillanaGOMX','p2b96Mhj7b','SantillanaGOMX',11],
'do':['10.33.154.74','SantillanaGODO','QKG347p2Ji','SantillanaGODO',20],
'co':['10.33.154.74','SantillanaGOCO','EDeFeaF9YW','SantillanaGOCO',21],
'bo':['10.33.154.74','SantillanaGOBO','obY9WeK7ak','SantillanaGOBO',19],
'testglobal':['10.33.154.74','SantillanaGOtest','boEJC9glif','SantillanaGOtest',12],
'pt':['10.33.154.74','SantillanaGOPT','H9ogcpREgD','SantillanaGOPT',18],
've':['10.33.154.74','SantillanaGOVE','ZXMHXeiTQY','SantillanaGOVE',5],
'ar':['10.33.154.74','SantillanaGOar','TNdAGkEdJb','SantillanaGOar',3],
'gtsv':['10.33.154.74','SantillanaGOGTSV','9WN6CEQQFY','SantillanaGOGTSV',7],
'ur':['10.33.154.74','SantillanaGOUR','3Byz5PDVbr','SantillanaGOUR',22],
'py':['10.33.154.74','SantillanaGOpy','nooGahw4zo','SantillanaGOpy',14],
'cr':['10.33.154.74','SantillanaGOCR','eaFeiPu5','SantillanaGOCR',4],
'pr':['10.33.154.74','SantillanaGOPR','jieJahzu9x','SantillanaGOPR',15],
'formacion':['10.33.154.74','SantillanaGOFO','Fie0oung','SantillanaGOFO',13],
'cl':['10.33.154.74','SantillanaGOcl','yaga3Ohghu','SantillanaGOcl',16],
'ec':['10.33.154.74','SantillanaGOEC','ieShah5Y','SantillanaGOEC',17],
# 'pe':['10.33.154.74','SantillanaGOcl','noexiste','SantillanaGOcl',6],
#'test':['10.33.154.74','root','','SantillanaGOtest',21],
#'develop':['78.47.151.244','SantillanaGOdeve','AHK4TK9CTk','SantillanaGOdeve',22],
#'develop':['10.226.74.80','SantillanaGOdeve','AHK4TK9CTk','SantillanaGOdeve',22],
#'develop':['10.226.74.80','root','','SantillanaGOdeve',22],
}

# con_main lleva el conector a la base de datos local, la que recibirá los datos del resto de bases de datos.
try:
	con_main = mdb.connect('localhost', 'administrador', 'xgV7WkqX', 'factoria')
	#con_main = mdb.connect('localhost', 'root', '', 'test')
	#print("Conectado")
	logging.info(ahora()+' INFO:::: Conectado factoria')
except mdb.Error, e:
	logging.error(ahora()+' ERROR:::: Ostion como un campano conexion instancia principal.... '+ repr(e))
	exit(1)

query_cursos = "SELECT `id_curso`,`nombre_curso` FROM `go_cursos`;"
query_asignaturas = "SELECT `id_asignatura`,`nombre_asignatura` FROM `go_asignaturas`;"

#query_tip_act = "SELECT 'actividad' AS `tipo`, `id_tipo_actividad` AS `id_tipo`, `nombre_tipo_actividad` AS `nombre_tipo`, `mascara_id` FROM  `go_tipo_actividad`;"
query_tip_act= "SELECT 'actividad' AS `tipo`, `id_tipo_actividad` AS `id_tipo`, `nombre_tipo_actividad` AS `nombre_tipo`, `mascara_id`, `subfolder_tipoactividad` AS `subfolder_tipo` FROM  `go_tipo_actividad`;"

#query_tip_rec = "SELECT 'recurso' AS `tipo`, `id_tipo_recurso` AS `id_tipo`, `nombre_tipo_recurso` AS `nombre_tipo`, `mascara_id` FROM  `go_tipo_recurso`;"
query_tip_rec = "SELECT 'recurso' AS `tipo`, `id_tipo_recurso` AS `id_tipo`, `nombre_tipo_recurso` AS `nombre_tipo`, `mascara_id`, `subfolder_tiporecurso` AS `subfolder_tipo` FROM  `go_tipo_recurso`;"

#query_act = "SELECT `act`.*, `arch`.`url_archivo` AS `thumbnail` FROM `view_data_actividades_to_factoria` `act` LEFT JOIN `go_actividades_archivos` `act_arch` ON `act_arch`.`id_act`= `act`.`id_elemento` LEFT JOIN `go_archivos` `arch` ON `arch`.`id_archivo`= `act_arch`.`id_archivo` WHERE `act_arch`.`section` = '';"
query_act = "SELECT `act`.*, `arch`.`url_archivo` AS `thumbnail` FROM `view_data_actividades_to_factoria` `act` LEFT JOIN `go_actividades_archivos` `act_arch` ON `act_arch`.`id_act`= `act`.`id_elemento` LEFT JOIN `go_archivos` `arch` ON `act_arch`.`id_archivo` = `arch`.`id_archivo` AND `act_arch`.`section` = '' and `act`.`idioma` in ('Español', 'Inglés', 'Francés');"
#query_rec = "SELECT `rec`.*, `arch`.`url_archivo` AS `thumbnail` FROM `view_data_recursos_to_factoria` `rec` LEFT JOIN `go_recursos_archivos` `rec_arch` ON `rec_arch`.`id_rec` = `rec`.`id_elemento` LEFT JOIN `go_archivos` `arch` ON `arch`.`id_archivo`= `rec_arch`.`id_archivo` WHERE `rec_arch`.`section` = '' and rec.idioma in ('Español', 'Inglés', 'Francés');"
query_rec = "SELECT rec_arch.section, `rec`.*, `arch`.`url_archivo` AS `thumbnail` FROM `view_data_recursos_to_factoria` `rec` LEFT JOIN `go_recursos_archivos` `rec_arch` ON `rec_arch`.`id_rec` = `rec`.`id_elemento`LEFT JOIN `go_archivos` `arch` ON `rec_arch`.`id_archivo` = `arch`.`id_archivo` AND `rec_arch`.`section` = '' and `rec`.`idioma` in ('Español', 'Inglés', 'Francés');"

query_ifaz_act = "SELECT 'actividad' AS `tipo`, `id_interfaz`, `nombre_interfaz`, `id_tipo_actividad` AS `id_tipo`, `url_interfaz` FROM  `go_actividades_interfaces`;"
query_ifaz_rec = "SELECT 'recurso' AS `tipo`, `id_interfaz`, `nombre_interfaz`, `id_tipo_recurso` AS `id_tipo`, `url_interfaz` FROM  `go_recursos_interfaces`;"

#CREATES a 20/05/2014
query_create_cursos = "CREATE TABLE  `sgo_cursos_aux` (`id` int(11) NOT NULL AUTO_INCREMENT,`instancia` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,`id_curso` int(11) NOT NULL,`nombre_curso` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;"
query_create_asig = "CREATE TABLE  `sgo_asignaturas_aux` (`id` int(11) NOT NULL AUTO_INCREMENT,`instancia` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,`id_asignatura` int(11) NOT NULL,`nombre_asignatura` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;"
query_create_act_rec = "CREATE TABLE  `sgo_actividadesYrecursos_aux` (`id` int(11) NOT NULL AUTO_INCREMENT,`instancia` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,`id_elemento` int(11) NOT NULL,`tipo` set('actividad','recurso') COLLATE utf8_spanish2_ci NOT NULL,`id_tipo_elemento` int(11) NOT NULL,`id_interfaz` int(11) NOT NULL,`id_estado` int(11) NOT NULL,`idioma` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,`curso` int(11) NOT NULL,`asignatura` int(11) NOT NULL,`createDateInFactoria` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,`fechaFinalizado` datetime NOT NULL,`titulo` text COLLATE utf8_spanish2_ci NOT NULL,`tags` text COLLATE utf8_spanish2_ci,`thumbnail` varchar(250) COLLATE utf8_spanish2_ci DEFAULT NULL,`favorito` set('0','1') COLLATE utf8_spanish2_ci NOT NULL DEFAULT '0', `newUploadPath` set('0','1') DEFAULT '0',PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;"
query_create_ifas = "CREATE TABLE  `sgo_interfaces_aux` (`id` int(11) NOT NULL AUTO_INCREMENT,`instancia` varchar(50) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL,`id_interfaz` int(11) NOT NULL,`tipo` set('actividad','recurso') NOT NULL,`nombre_interfaz` varchar(30) NOT NULL,`id_tipo` int(11) NOT NULL,`url_interfaz` varchar(200) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB  DEFAULT CHARSET=utf8;"
query_create_tipos = "CREATE TABLE  `sgo_tipo_actividadesYrecursos_aux` (`id` int(11) NOT NULL AUTO_INCREMENT,`tipo` set('actividad','recurso') NOT NULL,`id_tipo` int(11) NOT NULL,`nombre_tipo` varchar(150) NOT NULL ,`mascara_id` varchar(5) NOT NULL, `subfolder_tipo` varchar(250) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" 

query_drop_bck1 = "drop table if exists sgo_actividadesYrecursos_bck;"
query_drop_bck2 = "drop table if exists sgo_asignaturas_bck;"
query_drop_bck3 = "drop table if exists sgo_cursos_bck;"
query_drop_bck4 = "drop table if exists sgo_interfaces_bck;"
query_drop_bck5 = "drop table if exists sgo_tipo_actividadesYrecursos_bck;"
query_drop_bck6 = "drop table if exists sgo_actividadesYrecursos_aux;"
query_drop_bck7 = "drop table if exists sgo_asignaturas_aux;" 
query_drop_bck8 = "drop table if exists sgo_cursos_aux;"
query_drop_bck9 = "drop table if exists sgo_interfaces_aux;"
query_drop_bck0 = "drop table if exists sgo_tipo_actividadesYrecursos_aux;"

with con_main:

	cur_main = con_main.cursor(mdb.cursors.DictCursor)
	try:
		cur_main.execute(query_drop_bck1)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("A")
	try:
		cur_main.execute(query_drop_bck2)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("B")
	try:
		cur_main.execute(query_drop_bck3)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("B")
	try:
		cur_main.execute(query_drop_bck4)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("B")
	try:
		cur_main.execute(query_drop_bck5)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("C")
	try:
		cur_main.execute(query_drop_bck6)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("D")
	try:
		cur_main.execute(query_drop_bck7)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("E")
	try:
		cur_main.execute(query_drop_bck8)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("F")
	try:
		cur_main.execute(query_drop_bck9)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("G")
	try:
		cur_main.execute(query_drop_bck0)
		con_main.commit()
	except mdb.Error, e:
		logging.error( ahora() +' ERROR:::: Drops backups '+ repr(e))
		logging.error("H")

		print "drops"


	#CREATE TABLAS AUX
	try:
		cur_main.execute(query_create_act_rec)
		con_main.commit()
		print "create act rec aux"
	except mdb.Error, e:
		logging.error(ahora()+' ERROR:::: Creando tabla aux act rec '+ repr(e))
	query_extra = "INSERT INTO `sgo_tipo_actividadesYrecursos_aux` (`tipo`, `id_tipo`, `nombre_tipo`, `mascara_id`, `subfolder_tipo`) VALUES ('recurso', 202, 'Objeto Universal 3D', 'OBJ3D', ''), ('recurso', 201, 'Objeto Universal 2D', 'OBJ2D', '');"
	try:
		cur_main.execute(query_extra)
		con_main.commit()
	except mdb.Error, e:
		logging.error (ahora() + " extra")
	try:
		cur_main.execute(query_create_cursos)
		con_main.commit()
		print "create cursos aux"
	except mdb.Error, e:
		logging.error(ahora()+' ERROR:::: Creando tabla aux cursos'+ repr(e))
	try:
		cur_main.execute(query_create_asig)
		con_main.commit()
		print "create asig aux"
	except mdb.Error, e:
		logging.error(ahora()+' ERROR:::: Creando tabla aux asignaturas'+ repr(e))
	try:
		cur_main.execute(query_create_tipos)
		con_main.commit()
		print "create tipos aux"
	except mdb.Error, e:
		logging.error(ahora()+' ERROR:::: Creando tabla aux tipos '+ repr(e))
	try:
		cur_main.execute(query_create_ifas)
		con_main.commit()
		print "create ifaz aux"
	except mdb.Error, e:
		logging.error(ahora()+' ERROR:::: Creando tabla aux interfaces '+ repr(e))


	for pais in conn_dict:
		try:
			con = mdb.connect (conn_dict[pais][0],conn_dict[pais][1],conn_dict[pais][2],conn_dict[pais][3])
			logging.info(ahora()+' INFO:::: Conectado ' + str(pais))
			#print("Conectado " + str(pais))
			with con:

				cur = con.cursor(mdb.cursors.DictCursor)

				cur.execute(query_cursos)
				row_cursos = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: cursos ' + str(pais)+': '+str(len(row_cursos)))
				#print(ahora() +' DEBUG:::: cursos ' + str(pais)+': '+str(len(row_cursos)))
				
				cur.execute(query_asignaturas)
				row_asig = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: asignaturas ' + str(pais)+': '+str(len(row_asig)))
				#print(ahora() +' DEBUG:::: asignaturas ' + str(pais)+': '+str(len(row_asig)))

				cur.execute(query_act)
				row_act = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: actividades ' + str(pais)+': '+str(len(row_act)))
				#print(ahora() +' DEBUG:::: actividades ' + str(pais)+': '+str(len(row_act)))

				cur.execute(query_rec)
				row_rec = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: recursos ' + str(pais)+': '+str(len(row_rec)))
				#print(ahora() +' DEBUG:::: recursos ' + str(pais)+': '+str(len(row_rec)))

				cur.execute(query_ifaz_act)
				row_ifaz_act = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: interfaz actividades ' + str(pais)+': '+str(len(row_ifaz_act)))
				#print(ahora() +' DEBUG:::: interfaz actividades ' + str(pais)+': '+str(len(row_ifaz_act)))

				cur.execute(query_ifaz_rec)
				row_ifaz_rec = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: interfaz recursos ' + str(pais)+': '+str(len(row_ifaz_rec)))
				#print(ahora() +' DEBUG:::: interfaz recursos ' + str(pais)+': '+str(len(row_ifaz_rec)))
				
				cur.execute(query_tip_act)
				row_tipo_act = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: tipo act ' + str(pais)+': '+str(len(row_tipo_act)))
				#print(ahora() +' DEBUG:::: tipo act ' + str(pais)+': '+str(len(row_tipo_act)))

				cur.execute(query_tip_rec)
				row_tipo_rec = cur.fetchall()
				#logging.debug(ahora() +' DEBUG:::: tipo rec ' + str(pais)+': '+str(len(row_tipo_rec)))
				#print(ahora() +' DEBUG:::: tipo rec ' + str(pais)+': '+str(len(row_tipo_rec)))
				
				#recorrer row* e insertar o updatear la bd de factoria
				#fich_sqls.write("\n-- Cursos " + str(pais)+"\n")
				if len(row_cursos)!= 0:
					for row in row_cursos:
						query_insert_curso = "INSERT INTO sgo_cursos_aux (instancia, id_curso, nombre_curso) VALUES ('"+str(pais)+"', '"+str(row["id_curso"])+"', '"+str(row["nombre_curso"])+"');"
						#logging.debug(ahora() +' DEBUG:::: insert curso ' + query_insert_curso)
						try:
							cur_main.execute(query_insert_curso)
							con_main.commit()
							#fich_sqls.write(query_insert_curso+"\n")
							#print("OK CURSOS")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en cursos '"+str(pais)+"' "+ repr(e) + " " + str(query_insert_curso))
						#logging.debug(ahora() +' DEBUG:::: insert curso ' + str(pais)+': '+ str(row["id_curso"]))
				#fich_sqls.write("\n-- asignaturas " + str(pais)+"\n")		
				if len(row_asig)!= 0:
					for row in row_asig:
						query_insert_asig = "INSERT INTO `sgo_asignaturas_aux` (`instancia`, `id_asignatura`, `nombre_asignatura`) VALUES ('"+str(pais)+"', '"+str(row["id_asignatura"])+"', '"+str(row["nombre_asignatura"])+"');"
						try:
							cur_main.execute(query_insert_asig)
							con_main.commit()
							#fich_sqls.write(query_insert_asig+"\n")
							#print("OK ASIGNATURAS")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en asignaturas '"+str(pais)+"' "+ repr(e) + " " + str(query_insert_asig))
						#logging.debug(ahora() +' DEBUG:::: insert asig ' + str(pais)+': '+ str(row["id_asignatura"]))
				#fich_sqls.write("\n-- Actividades " + str(pais)+"\n")			
				if len(row_act)!= 0:	
					for row in row_act:	
						titulo_escapado = html_escape(str(row["titulo"]))
						tags_escapado = html_escape(str(row["tags"]))
						query_insert_act = "INSERT INTO `sgo_actividadesYrecursos_aux` (`instancia`, `id_elemento`, `tipo`, `id_tipo_elemento`, `id_interfaz`, `id_estado`, `fechaFinalizado`, `idioma`,  `titulo`, `tags`, `curso`, `asignatura`, `favorito`, `thumbnail`, newUploadPath) VALUES ('"+str(pais)+"','"+str(row["id_elemento"])+"','actividad', '"+str(row["id_tipo_elemento"])+"', '"+str(row["id_interfaz"])+"', '"+str(row["id_estado"])+"', '"+str(row["fechaFinalizado"])+"', '"+str(row["idioma"])+"', '"+ str(titulo_escapado) +"', '"+str(tags_escapado)+"', '"+str(row["curso"])+"', '"+str(row["asignatura"])+"', 0,'"+str(row["thumbnail"])+"','"+str(row["newUploadPath"])+"');"
						try:
							cur_main.execute(query_insert_act)
							con_main.commit()
							#fich_sqls.write(query_insert_act+"\n")
							#print("OK ACTIVIDADES")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en actividades '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_act))
						#logging.debug(ahora() +' DEBUG:::: insert act ' + str(pais)+': '+ str(row["id_elemento"]))
				#fich_sqls.write("\n-- Recusos " + str(pais)+"\n")
				if len(row_rec)!= 0:	
					for row in row_rec:
						titulo_escapado = html_escape(str(row["titulo"]))
						tags_escapado = html_escape(str(row["tags"]))
						query_insert_rec = "INSERT INTO `sgo_actividadesYrecursos_aux` (`instancia`, `id_elemento`, `tipo`, `id_tipo_elemento`, `id_interfaz`, `id_estado`, `fechaFinalizado`, `idioma`,  `titulo`, `tags`, `curso`, `asignatura`, `favorito`, `thumbnail`, `newUploadPath`) VALUES ('"+str(pais)+"', '"+str(row["id_elemento"])+"', 'recurso', '"+str(row["id_tipo_elemento"])+"', '"+str(row["id_interfaz"])+"', '"+str(row["id_estado"])+"', '"+str(row["fechaFinalizado"])+"', '"+str(row["idioma"])+"', '"+str(titulo_escapado)+"', '"+str(tags_escapado)+"', '"+str(row["curso"])+"', '"+str(row["asignatura"])+"', 0,'"+str(row["thumbnail"])+"','"+str(row["newUploadPath"])+"');"
						try:
							cur_main.execute(query_insert_rec)
							con_main.commit()
							#fich_sqls.write(query_insert_rec+"\n")
							#print("OK RECURSOS")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en recursos '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_rec))
						#logging.debug(ahora() +' DEBUG:::: insert rec ' + str(pais)+': '+ str(row["id_elemento"]))
				#fich_sqls.write("\n-- Ifaz Act " + str(pais)+"\n")
				if len(row_ifaz_act)!= 0:
					for row in row_ifaz_act:
						query_insert_ifaz_act = "INSERT INTO `sgo_interfaces_aux` (`instancia`, `id_interfaz`, `tipo`, `id_tipo`, `nombre_interfaz`, `url_interfaz`) VALUES ('"+str(pais)+"' , '"+str(row["id_interfaz"])+"' ,'actividad', '"+str(row["id_tipo"])+"', '"+str(row["nombre_interfaz"])+"', '"+str(row["url_interfaz"])+"');"
						try:
							cur_main.execute(query_insert_ifaz_act)
							con_main.commit()
							#fich_sqls.write(query_insert_ifaz_act+"\n")
							#print("OK IFAZ ACT")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en ifaz act '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_ifaz_act))
						#logging.debug(ahora() +' DEBUG:::: insert ifaz act ' + str(pais)+': '+ str(row["id_interfaz"]))
				#fich_sqls.write("\n-- Ifaz rec " + str(pais)+"\n")
				if len(row_ifaz_rec)!= 0:
					for row in row_ifaz_rec:
						query_insert_ifaz_rec = "INSERT INTO `sgo_interfaces_aux` (`instancia`, `id_interfaz`, `tipo`, `id_tipo`, `nombre_interfaz`, `url_interfaz`) VALUES ('"+str(pais)+"' , '"+str(row["id_interfaz"])+"' ,'recurso', '"+str(row["id_tipo"])+"', '"+str(row["nombre_interfaz"])+"' ,'"+str(row["url_interfaz"])+"');"
						try:
							cur_main.execute(query_insert_ifaz_rec)
							con_main.commit()
							#fich_sqls.write(query_insert_ifaz_rec+"\n")
							#print("OK IFAZ REC")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en ifaz rec '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_ifaz_rec))
						#logging.debug( ahora() +' DEBUG:::: insert ifaz rec ' + str(pais)+': '+ str(row["id_interfaz"]))
				#fich_sqls.write("\n-- Tipo act " + str(pais)+"\n")
				if len(row_tipo_act)!= 0:
					for row in row_tipo_act:
						query_insert_tipo_act = "INSERT INTO `sgo_tipo_actividadesYrecursos_aux` (`tipo`, `id_tipo`, `nombre_tipo`, `mascara_id`, `subfolder_tipo`) VALUES ('actividad', '"+str(row["id_tipo"])+"', '"+str(row["nombre_tipo"])+"', '"+str(row["mascara_id"])+"', '"+str(row["subfolder_tipo"])+"');"
						try:
							cur_main.execute(query_insert_tipo_act)
							con_main.commit()
							#fich_sqls.write(query_insert_tipo_act+"\n")							
							#print("OK TIPO ACT")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en tipo act '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_tipo_act))
							#logging.debug( ahora() +' DEBUG:::: insert tipo rec ' + str(pais)+': '+ str(row["id_tipo"]))

				#fich_sqls.write("\n-- Tipo rec " + str(pais)+"\n")
				if len(row_tipo_rec)!= 0:
					for row in row_tipo_rec:
						query_insert_tipo_rec = "INSERT INTO `sgo_tipo_actividadesYrecursos_aux` (`tipo`, `id_tipo`, `nombre_tipo`, `mascara_id`, `subfolder_tipo`) VALUES ('recurso', '"+str(row["id_tipo"])+"', '"+str(row["nombre_tipo"])+"', '"+str(row["mascara_id"])+"', '"+str(row["subfolder_tipo"])+"');"
						try:
							cur_main.execute(query_insert_tipo_rec)
							con_main.commit()
							#fich_sqls.write(query_insert_tipo_rec+"\n")
							#print("OK TIPO REC")
						except mdb.Error, e:
							logging.error (ahora() + " Oh shit " +str(ahora())+ "... en tipo rec '"+str(pais)+"' "+ repr(e)+ " " + str(query_insert_tipo_rec))
							#logging.debug( ahora() +' DEBUG:::: insert tipo rec ' + str(pais)+': '+ str(row["id_tipo"]))

			con.close()
			logging.info( ahora() +' INFO:::: Desconectado instancia ' + str(pais) )
		except mdb.Error, e:
			#print "Oh shit " +str(ahora())+ "... en '"+str(pais)+"' "+ repr(e)
			logging.error( ahora() +" ERROR en '"+str(pais)+" "+ repr(e) )

#MOVER ACTUALES -> BCK
query_move_act_bck1 = "rename table sgo_actividadesYrecursos to sgo_actividadesYrecursos_bck;" 
query_move_act_bck2 = "rename table sgo_asignaturas to sgo_asignaturas_bck;"
query_move_act_bck3 = "rename table sgo_cursos to sgo_cursos_bck; "
query_move_act_bck4 = "rename table sgo_interfaces to sgo_interfaces_bck;" 
query_move_act_bck5 = "rename table sgo_tipo_actividadesYrecursos to sgo_tipo_actividadesYrecursos_bck;"
try:
	cur_main.execute(query_move_act_bck1)
	con_main.commit()
except mdb.Error, e:
	logging.error("I")
try:
	cur_main.execute(query_move_act_bck2)
	con_main.commit()
except mdb.Error, e:
	logging.error("J")
try:
	cur_main.execute(query_move_act_bck3)
	con_main.commit()
except mdb.Error, e:
	logging.error("K")
try:
	cur_main.execute(query_move_act_bck4)
	con_main.commit()
except mdb.Error, e:
	logging.error("L")
try:
	cur_main.execute(query_move_act_bck5)
	con_main.commit()
except mdb.Error, e:
	logging.error("M")
print "moves"

#MOVER AUX -> ACTUALES
query_move_aux_act1 = "rename table sgo_actividadesYrecursos_aux to sgo_actividadesYrecursos;" 
query_move_aux_act2 = "rename table sgo_asignaturas_aux to sgo_asignaturas;"
query_move_aux_act3 = "rename table sgo_cursos_aux to sgo_cursos;"
query_move_aux_act4 = "rename table sgo_interfaces_aux to sgo_interfaces;"
query_move_aux_act5 = "rename table sgo_tipo_actividadesYrecursos_aux to sgo_tipo_actividadesYrecursos;"
try:
	cur_main.execute(query_move_aux_act1)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + "move final1")
try:
	cur_main.execute(query_move_aux_act2)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + "move final2")
try:
	cur_main.execute(query_move_aux_act3)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + "move final3")
try:
	cur_main.execute(query_move_aux_act4)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + "move final4")
try:
	cur_main.execute(query_move_aux_act5)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + "move final5")

alter_1="alter table sgo_actividadesYrecursos convert to character set utf8 collate utf8_spanish2_ci;"
alter_2="alter table sgo_asignaturas convert to character set utf8 collate utf8_spanish2_ci;"
alter_3="alter table sgo_cursos convert to character set utf8 collate utf8_spanish2_ci;"
alter_4="alter table sgo_interfaces convert to character set utf8 collate utf8_spanish2_ci;"
alter_5="alter table sgo_tipo_actividadesYrecursos convert to character set utf8 collate utf8_spanish2_ci;"

try:
	cur_main.execute(alter_1)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + " alter_1")

try:
	cur_main.execute(alter_2)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + " alter_2")

try:
	cur_main.execute(alter_3)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + " alter_3")

try:
	cur_main.execute(alter_4)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + " alter_4")

try:
	cur_main.execute(alter_5)
	con_main.commit()
except mdb.Error, e:
	logging.error (ahora() + " alter_5")

con_main.close()
end = datetime.datetime.now()

logging.debug( end - start +' ENDUCHT!')