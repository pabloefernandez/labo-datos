#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 15:30:40 2023

@author: tsl2004
"""


import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import re


padron = pd.read_csv("./tablas_creadas/tablas_originales_normlizadas_y_limpiadas/Padron_en_3raFN_y_1raFN.csv")
padron_original = pd.read_csv("./tablas_originales/padron-de-operadores-organicos-certificados.csv", encoding= 'windows-1252')
padron_poco_limpiado_bien_codificado = pd.read_csv("./tablas_originales/padron-de-operadores-organicos-certificados_en_UTF.csv")
padron_mod=  pd.read_csv("./tablas_creadas/padron-de-operadores-organicos-certificados_mod.csv")
localidades_censales_original = pd.read_csv("./tablas_originales/localidades-censales.csv")
loc_cens = pd.read_csv("./tablas_creadas/tablas_originales_normlizadas_y_limpiadas/loc_sensales_1raFN.csv")
loc_cens_limpiado = pd.read_csv("./localidades-censales_limpiado.csv")
dict_deptos_original  = pd.read_csv("./tablas_originales/diccionario_cod_depto.csv")
dict_act_original  = pd.read_csv("./tablas_originales/diccionario_clae2.csv")
clae2_original  = pd.read_csv("./tablas_originales/w_median_depto_priv_clae2.zip")


#LIMPIEZA

padron_poco_limpiado = padron_original.copy()
#Limpieza establecimientos mal subidos con NC en establecimiento
padron_poco_limpiado.rename(columns={padron_poco_limpiado.columns[16]: 'establecimiento2'},inplace=True)

filtro = padron_poco_limpiado["establecimiento2"].isna()

padron_poco_limpiado = padron_poco_limpiado[filtro]
padron_poco_limpiado = padron_poco_limpiado.iloc[:, :-3]

#Limpieza de los -99 en los salarios de clae_2
consulta_sacar_99 = """
                    SELECT *
                    FROM clae2_original
                    where w_median > 0

                    """
clae_sin_99 = sql^consulta_sacar_99

consulta_sacar_NC = """
                    SELECT *
                    FROM padron_poco_limpiado
                    WHERE  padron_poco_limpiado.establecimiento != 'NC'

                    """
padron_poco_limpiado = padron_poco_limpiado_bien_codificado
padron_poco_limpiado= sql^consulta_sacar_NC
padron_poco_limpiado = padron_poco_limpiado_bien_codificado

#SECCION ESTANDARIZACION
# Se estandarizan algunas columnas importantes

padron_mod = padron_poco_limpiado.copy()

sin_tildes = """
            SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(padron_mod.departamento,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') as departamento, 
            FROM padron_mod  
            """     
tabla_arreglo= sql^sin_tildes
padron_mod["departamento"]=tabla_arreglo["departamento"]


sin_tildes_loc = """
            SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(loc_cens_limpiado.departamento_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as departamento_loc
            FROM loc_cens_limpiado  
            """     
tabla_arreglo_loc = sql^sin_tildes_loc
loc_cens_limpiado["departamento_nombre"] = tabla_arreglo_loc["departamento_loc"]

sin_tildes_loc_en_muni = """
                    SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(loc_cens_limpiado.municipio_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as municipio_nombre
                    FROM loc_cens_limpiado  
                    """
                    
tabla_arreglo_loc_muni = sql^sin_tildes_loc_en_muni

loc_cens_limpiado["municipio_nombre"] = tabla_arreglo_loc_muni["municipio_nombre"]




#LIMPIEZA ATRIBUTO DEPARTAMENTOS DE PADRON 
#Nos fijamos que que departamentos en el atributo departamentos de apdron son verdaderamente departamentos
consulta_deptos = """
                SELECT DISTINCT padron_mod.departamento, loc_cens_limpiado.provincia_id
                FROM padron_mod
                INNER JOIN loc_cens_limpiado
                ON UPPER(padron_mod.departamento) = UPPER(loc_cens_limpiado.departamento_nombre)
                
                """
tabla_consulta = sql^consulta_deptos

#Nos fijamos que valores de departamentos en padron no son en realidad departamentos                 
consulta_deptos_de_mas = """
                SELECT padron_mod.departamento 
                FROM padron_mod
                EXCEPT (
                   SELECT tabla_consulta.departamento
                   FROM tabla_consulta 
                    )
                
                """
tabla_consulta2 = sql^consulta_deptos_de_mas

# Nos fijamos coincidencias entre departamentos de padron y municipios de loc sensales
consulta_deptos_que_son_muni =  """
                SELECT DISTINCT loc_cens_limpiado.municipio_nombre ,loc_cens_limpiado.departamento_nombre,  loc_cens_limpiado.provincia_id,
                FROM loc_cens_limpiado
                INNER JOIN tabla_consulta2
                ON UPPER(loc_cens_limpiado.municipio_nombre ) = UPPER(tabla_consulta2.departamento) 
                
                """
tabla_consulta3 = sql^consulta_deptos_que_son_muni
#Nos fijamos los valores en el atributo departamentos que no son ni departamentos ni municipios
consulta_cosas_raras = """
                SELECT DISTINCT UPPER(tabla_consulta2.departamento) as departamento
                FROM tabla_consulta2
                EXCEPT (
                   SELECT UPPER(tabla_consulta3.municipio_nombre)
                   FROM tabla_consulta3 
                    )

                """
tabla_consulta4 = sql^consulta_cosas_raras
#Todo lo no son ni deptos ni municpios, se elimina
consulta_eliminacion= """
                        SELECT DISTINCT *
                        FROM padron_mod
                        WHERE padron_mod.departamento NOT IN(
                            SELECT tabla_consulta4.departamento
                            FROM tabla_consulta4
                            )

"""

padron_mod = sql^consulta_eliminacion



p_copia = padron_mod.copy()


def cambiar_valores_a_partir_de_tabla3(p_copia,tabla3):
    for i in range(len(p_copia)):
        for j in range(len(tabla3)):
            if p_copia.iloc[i,4] == tabla3.iloc[j,0] and (p_copia.iloc[i,2] == tabla3.iloc[j,2]): #ME IMPORTAN LAS PROVINCIAS
                p_copia.iloc[i,4] = tabla3.iloc[j,1]
                break
    return p_copia 
padron_mod = cambiar_valores_a_partir_de_tabla3(p_copia,tabla_consulta3) #Padron_mod tiene la columna departamento limpiada!!

padron_mod.to_csv("padron_limpiado.csv",index= False)



































































