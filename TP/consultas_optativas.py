#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:46:10 2023

@author: tsl2004
"""
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np

padron = pd.read_csv("./tablas_originales/padron-de-operadores-organicos-certificados_en_UTF.csv")
localidades_censales = pd.read_csv("./tablas_originales/localidades-censales.csv")


#Consultas para saber pk de padron

consulta_1 = """
                SELECT DISTINCT * 
                FROM padron;
             """

pk_padron1 = sql^consulta_1

consulta_2 = """
                SELECT DISTINCT establecimiento, razon_social 
                FROM padron;
             """

pk_padron2 = sql^consulta_2

#Y sabíamos que, de ser pk razon_social y establecimiento, la cantidad de filas debía coincidir.

#Consultas para saber pk de localidades_censales

consulta_1 = """
                SELECT DISTINCT * 
                FROM localidades_censales;
             """

pk_loc_cens1 = sql^consulta_1

consulta_2 = """
                SELECT DISTINCT id
                FROM localidades_censales;
             """

pk_loc_cens2 = sql^consulta_2

#Mismo concepto que en la  consulta anterior



#Otra consulta para comprobar en la tabla LC depto+municipio--->provincia, es decir que existe una DF desde depto+municipio hacia provincia
consulta_de_provincia_misma_dep_y_muni ="""
    SELECT DISTINCT provincia_nombre, departamento_id, municipio_id , 
    FROM localidades_censales
    GROUP BY provincia_nombre, departamento_id ,municipio_id

 """
tabla_provincia_misma_dep_y_muni1 = sql ^consulta_de_provincia_misma_dep_y_muni
 
consulta_de_provincia_misma_dep_y_muni2 = """
     SELECT DISTINCT  departamento_id, municipio_id , 
     FROM localidades_censales
     GROUP BY provincia_nombre, departamento_id ,municipio_id

  """
tabla_aprovincia_misma_dep_y_muni2 = sql ^consulta_de_provincia_misma_dep_y_muni2
