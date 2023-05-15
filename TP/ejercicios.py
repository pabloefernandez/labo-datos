#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:32:32 2023

@author: tsl2004
"""

import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import re

padron = pd.read_csv("./tablas_creadas/tablas_originales_normlizadas_y_limpiadas/Padron_en_3raFN_y_1raFN.csv")
padron_original = pd.read_csv("./tablas_originales/padron-de-operadores-organicos-certificados.csv", encoding= 'windows-1252')
padron_mod=  pd.read_csv("./tablas_creadas/padron-de-operadores-organicos-certificados_mod.csv")
localidades_censales_original = pd.read_csv("./tablas_originales/localidades-censales.csv")
loc_cens = pd.read_csv("./tablas_creadas/tablas_originales_normlizadas_y_limpiadas/loc_sensales_1raFN.csv")
dict_deptos_original  = pd.read_csv("./tablas_originales/diccionario_cod_depto.csv")
dict_act_original  = pd.read_csv("./tablas_originales/diccionario_clae2.csv")
clae2_original  = pd.read_csv("./tablas_originales/w_median_depto_priv_clae2.zip")
#Ex provincias
provincias_padron = pd.read_csv("./tablas_creadas/3ra_FN/padron/tabla_provincia_id_U_provincia.csv") 
#ex deptos
deptos_loc_cens = pd.read_csv("./tablas_creadas/3ra_FN/loc_sensales/tabla_depto_id_U_depto_nombre.csv") 
#ex rubro_clae2
rubro_unitario_clae2 = pd.read_csv("./tablas_creadas/rubro_unitario_clae2.csv")
rubros_padron = pd.read_csv("./tablas_creadas/1ra_FN/padron/rubros_en1FN.csv")

# codigo para las consultas del ejercicio hi) 
        #Ejercicio i)

consulta_1 = """
                SELECT DISTINCT provincias_padron.provincia, count(*) as cant_operadores 
                FROM padron
                INNER JOIN provincias_padron
                ON provincias_padron.provincia_id = padron.provincia_id
                GROUP BY provincias_padron.provincia;


             """

ej1 = sql^consulta_1
print(ej1)


        #Ejercicio ii)

consulta2 = """
            
                SELECT DISTINCT loc_cens.departamento_nombre
                FROM loc_cens
                EXCEPT(
                    SELECT DISTINCT padron.departamento
                    FROM padron
                    )

                """
ej2 = sql^consulta2
print(ej2)
        #Ejercicio iii)

consulta3 = """
                    SELECT DISTINCT rc2.clae2,rc2.clae2_desc, COUNT(*)
                    FROM rubros_padron rp
                    INNER JOIN rubro_unitario_clae2 rc2 ON rc2.rubro = rp.rubro
                    GROUP BY rc2.clae2_desc,rc2.clae2 
                    """
ej3 = sql ^ consulta3
print(ej3)    
    
    
    #Ejercicio iv)
actividad = ej3.iloc[0,0]
actividad = str(actividad)
consulta4 = '''
                SELECT AVG(w_median) AS promedio FROM clae2_original 
                WHERE clae2 = $actividad AND fecha = '2022-12-01' AND w_median > 0
    '''

print(sql ^ consulta4)
nacional = '''SELECT YEAR(CAST(fecha AS DATE)) as fecha,AVG(w_median) promedio_anual,stddev(w_median) AS desvio_estandar FROM clae2_original GROUP BY YEAR(CAST(fecha AS DATE)) ORDER BY fecha'''
print(sql^nacional)
provincial = '''
                SELECT YEAR(CAST(fecha AS DATE)) as fecha,p.provincia as provincia,AVG(w_median) AS promedio_anual_provincial,stddev(w_median) AS desvio_estandar FROM clae2_original c2 INNER JOIN provincias_padron p 
                ON p.provincia_id = c2.id_provincia_indec GROUP BY YEAR(CAST(fecha AS DATE)),p.provincia ORDER BY YEAR(CAST(fecha AS DATE))
    
    '''
ej4 = sql^(provincial)
print(ej4)
