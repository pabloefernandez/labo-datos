#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:05:32 2023

@author: tsl2004
"""

#CONSULTA PARA VER SI MUNI+DEPTO APARECIA EN MAS DE UNA PROV                                  
tabla_consulta = sql^ consulta_de_provincia_misma_dep_y_muni
tabla_consulta2  = sql^ consulta_de_provincia_misma_dep_y_muni2

consulta_de_provincia_misma_dep_y_muni = """
    SELECT DISTINCT provincia_nombre, departamento_id, municipio_id , 
    FROM localidades_censales
    GROUP BY provincia_nombre, departamento_id ,municipio_id

 """
 
 
 consulta_de_provincia_misma_dep_y_muni2 = """
     SELECT DISTINCT  departamento_id, municipio_id , 
     FROM localidades_censales
     GROUP BY provincia_nombre, departamento_id ,municipio_id

  """
  