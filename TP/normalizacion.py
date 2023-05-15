#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:55:27 2023

@author: tsl2004
"""
import pandas as pd
from inline_sql import sql, sql_val
import numpy as np
import re

padron = pd.read_csv("./tablas_creadas/tablas_originales_normlizadas_y_limpiadas/Padron_en_3raFN_y_1raFN.csv")
padron_original = pd.read_csv("./tablas_originales/padron-de-operadores-organicos-certificados.csv", encoding= 'windows-1252')
padron_limpiado=  pd.read_csv("./tablas_creadas/padron_limpiado.csv")
localidades_censales_original = pd.read_csv("./tablas_originales/localidades-censales.csv")
loc_cens_limpiado = pd.read_csv("./tablas_creadas/localidades-censales_limpiado.csv")
dict_deptos_original  = pd.read_csv("./tablas_originales/diccionario_cod_depto.csv")
dict_act_original  = pd.read_csv("./tablas_originales/diccionario_clae2.csv")
clae2_original  = pd.read_csv("./tablas_originales/w_median_depto_priv_clae2.zip")




#FUNCIONES UTILZADAS PARA SEPARAR LA TABLA PADRON EN 1FN
#Se separa el atributo "productos" en una nueva tabla
PK_padron_y_productos = sql^(" SELECT razon_social,establecimiento, productos FROM padron_limpiado")
tabla_productos_en_1FN  = pd.DataFrame(columns=['razon_social' , 'establecimiento', 'productos'])

def primera_forma_normal_productos(df,nuevo_df):
   for i in range(len(df)):
        if df.iloc[i,2] == "" or type(df.iloc[i,2] ) == float :
           continue
        productos = re.split(" Y | y |/|,",df.iloc[i,2])
        for producto in productos:
            producto = producto.lstrip()
            nuevo_df.loc[len(nuevo_df)] = [df.iloc[i,0],df.iloc[i,1],producto] 
   return nuevo_df


print(primera_forma_normal_productos(PK_padron_y_productos, tabla_productos_en_1FN))
#tabla_productos_en_1FN.to_csv("tabla_productos_mod.csv",index= False)

#Se separa el atributo "rubro" en una nueva tabla

PK_padron_y_rubro = sql^(" SELECT razon_social,establecimiento, rubro FROM padron_limpiado")
tabla_rubros_en_1FN  = pd.DataFrame(columns=['razon_social' , 'establecimiento', 'rubro'])

def primera_forma_normal_rubro(df,nuevo_df):
    for i in range(len(df)):
        if df.iloc[i,2] == "" or type(df.iloc[i,2] ) == float :
            continue
        rubros = re.split(" Y | y |/",df.iloc[i,2])
        for rubro in rubros:
            if rubro != "" :
                rubro = rubro.lstrip()
                nuevo_df.loc[len(nuevo_df)] = [df.iloc[i,0],df.iloc[i,1],rubro] 
    return nuevo_df

print(primera_forma_normal_rubro(PK_padron_y_rubro, tabla_rubros_en_1FN))
#tabla_rubros_en_1FN.to_csv("rubros_en1FN", index = False)




#CODIGO PARA PASAR CADA TABLA A 3FN. Donde dice "copia" y luego la tabla nos refiermos a la tabla orignal a la que se le separan las columnas que tiene una DF transitiva, estando entonces la tabla en 3FN.


#PADRON 3RA FORMA
copia_padron = sql^("SELECT DISTINCT pais_id, provincia_id, departamento,localidad, categoria_id, Certificadora_id,razon_social, establecimiento FROM padron_limpiado")
tabla_paisid_U_pais = sql^ (" SELECT DISTINCT pais_id, pais FROM padron_limpiado "  )
tabla_provincia_id_U_provincia = sql^("SELECT DISTINCT provincia_id, provincia FROM padron_limpiado")
tabla_categoria_id_U_categoria_desc = sql^("SELECT DISTINCT categoria_id categoria_desc FROM padron_limpiado")
tabla_certificadora_id_U_certificadora_deno = sql^("SELECT DISTINCT Certificadora_id, certificadora_deno  FROM padron_limpiado")

#LOC_SENSALES
copia_loc_censales= sql ^("SELECT categoria, centroide_Lat, centroide_Lon, departamento_nombre, fuente, id, municipio_id, nombre, provincia_id  FROM loc_cens_limpiado")
tabla_depto_id_U_depto_nombre = sql^("SELECT DISTINCT departamento_id, departamento_nombre FROM loc_cens_limpiado")
tabla_muni_id_U_muni_nombre = sql^("SELECT DISTINCT municipio_id, municipio_nombre FROM loc_cens_limpiado")
tabla_prov_id_U_prov_nombre1 = sql^("SELECT DISTINCT provincia_id, provincia_nombre FROM loc_cens_limpiado")
tabla_prov_id_U_depto_id_U_muni_id = sql^("SELECT DISTINCT provincia_id, departamento_id, municipio_id FROM loc_cens_limpiado")


#DICT_DEPTOS
copia_dict_deptos = sql^("SELECT codigo_departamento_indec, id_provincia_indec FROM dict_deptos_original ")
tabla_prov_id_U_prov_nombre2 = sql^("SELECT DISTINCT id_provincia_indec, nombre_provincia_indec FROM dict_deptos_original")
tabla_codigo_depto_U_nombre_depto = sql^("SELECT DISTINCT codigo_departamento_indec, nombre_departamento_indec FROM dict_deptos_original")

#DICT_ACT
copia_dict_act =  sql^("SELECT clae2, letra FROM dict_act_original ")
tabla_letra_U_letra_desc = sql^("SELECT DISTINCT letra, letra_desc FROM dict_act_original")
tabla_clae2_U_clae2 = sql^("SELECT DISTINCT clae2, clae2_desc FROM dict_act_original")






#PADRON 3RA FORMA A CSV 
"""
copia_padron.to_csv("Padron_en_3raFN(falta_rubro).csv", index = False)

tabla_paisid_U_pais.to_csv("tabla_pais_id_U_paiss.csv" ,index= False)
tabla_provincia_id_U_provincia.to_csv("tabla_provincia_id_U_provincianocs.csv",index= False)
tabla_categoria_id_U_categoria_desc.to_csv("tabla_categoria_id_U_categoria_desc.csv",index= False)
tabla_certificadora_id_U_certificadora_deno.to_csv("tabla_certificadora_id_U_certificadora_deno.csv",index= False)


#LOC_SENSALES
copia_loc_censales.to_csv("loc_sensales_1raFN.csv", index = False)

tabla_depto_id_U_depto_nombre.to_csv("tabla_depto_id_U_depto_nombre.csv",index= False)
tabla_muni_id_U_muni_nombre.to_csv("tabla_muni_id_U_muni_nombre.csv",index= False)
tabla_prov_id_U_prov_nombre1.to_csv("tabla_prov_id_U_prov_nombre1.csv",index= False)
tabla_prov_id_U_depto_id_U_muni_id.to_csv("tabla_prov_id_U_depto_id_U_muni_id.csv",index= False)

#DICT_DEPTOS
copia_dict_deptos.to_csv("dict_deptos_1raFN.csv", index = False)

tabla_prov_id_U_prov_nombre2.to_csv("tabla_prov_id_U_prov_nombre2.csv",index = False)
tabla_codigo_depto_U_nombre_depto.to_csv("tabla_codigo_depto_U_nombre_depto.csv", index = False)

#DICT_ACT
copia_dict_act.to_csv("dict_act_1raFN.csv",index= False)

tabla_letra_U_letra_desc.to_csv("tabla_letra_U_letra_desc.csv",index= False)
tabla_clae2_U_clae2.to_csv("tabla_clae2_U_clae2.csv",index= False)
"""