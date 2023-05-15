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


# Se estandarizan algunas columnas importantes

sin_tildes = """
            SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(padron_mod.departamento,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u') as departamento, 
            FROM padron_mod  
            """     
tabla_arreglo= sql^sin_tildes
padron_mod["departamento"]=tabla_arreglo["departamento"]


sin_tildes_loc = """
            SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(loc_cens.departamento_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as departamento_loc
            FROM loc_cens  
            """     
tabla_arreglo_loc = sql^sin_tildes_loc
loc_cens["departamento_nombre"] = tabla_arreglo_loc["departamento_loc"]

sin_tildes_loc_en_muni = """
                    SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(loc_cens.nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as municipio_nombre
                    FROM loc_cens  
                    """
                    
tabla_arreglo_loc_muni = sql^sin_tildes_loc_en_muni

loc_cens["municipio_nombre"] = tabla_arreglo_loc_muni["municipio_nombre"]




#LIMPIEZA ATRIBUTO DEPARTAMENTOS DE PADRON 
consulta_deptos = """
                SELECT DISTINCT padron_mod.departamento, loc_cens.provincia_id
                FROM padron_mod
                INNER JOIN loc_cens
                ON UPPER(padron_mod.departamento) = UPPER(loc_cens.departamento_nombre)
                
                """
tabla_consulta = sql^consulta_deptos

                
consulta_deptos_de_mas = """
                SELECT padron_mod.departamento 
                FROM padron_mod
                EXCEPT (
                   SELECT tabla_consulta.departamento
                   FROM tabla_consulta 
                    )
                
                """
tabla_consulta2 = sql^consulta_deptos_de_mas

# me fijo coincidencias entre depatos de padron(t_cons.2) y munucipios de loc sensales
consulta_deptos_que_son_muni =  """
                SELECT DISTINCT loc_cens.municipio_nombre ,loc_cens.departamento_nombre,  loc_cens.provincia_id, 
                FROM loc_cens
                INNER JOIN tabla_consulta2
                ON UPPER(loc_cens.municipio_nombre ) = UPPER(tabla_consulta2.departamento) 
                
                """
tabla_consulta3 = sql^consulta_deptos_que_son_muni

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
#loc_copia= localidades_sensales.copy()
print(tabla_consulta3.iloc[4,1] == p_copia.iloc[5,2])

def cambiar_valores_a_partir_de_tabla3(p_copia,tabla3):
    for i in range(len(padron)):
        for j in range(len(tabla3)):
            if p_copia.iloc[i,4] == tabla3.iloc[j,0] and (p_copia.iloc[i,2] == tabla3.iloc[j,2]): #ME IMPORTAN LAS PROVINCIAS
                p_copia.iloc[i,4] = tabla3.iloc[j,1]
                break
    return p_copia 
padron_mod = cambiar_valores_a_partir_de_tabla3(p_copia,tabla_consulta3) #Padron_mod tiene la columna departamento limpiada!!

#p_final.to_csv("padron_con_deptos_correctos.csv",index= False)


















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
#print(ej1)

consultaa = '''
SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(localidades_sensales.departamento_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as departamento_loc'''

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
    
    
    
    #Ejercicio iv)
actividad = ej3.iloc[0,0]
actividad = str(actividad)
consulta4 = '''
                SELECT AVG(w_median) AS promedio FROM clae2_original 
                WHERE clae2 = $actividad AND fecha = '2022-12-01' AND w_median > 0
    '''

print(sql ^ consulta4)
con = '''SELECT YEAR(CAST(fecha AS DATE)) as fecha,AVG(w_median) promedio_anual,stddev(w_median) AS desvio_estandar FROM clae2_original GROUP BY YEAR(CAST(fecha AS DATE)) ORDER BY fecha'''
print(sql^con)
provincial = '''
                SELECT YEAR(CAST(fecha AS DATE)) as fecha,p.provincia as provincia,AVG(w_median) AS promedio_anual_provincial,stddev(w_median) AS desvio_estandar FROM clae2_original c2 INNER JOIN provincias_padron p 
                ON p.provincia_id = c2.id_provincia_indec GROUP BY YEAR(CAST(fecha AS DATE)),p.provincia ORDER BY YEAR(CAST(fecha AS DATE))
    
    '''
ej4 = sql^(provincial)












































#FUNCIONES UTILZADAS PARA SEPARAR LA TABLA PADRON EN 1FN
#Se separa el atributo "productos" en una nueva tabla
PK_padron_y_productos = sql^(" SELECT razon_social,establecimiento, productos FROM padron_mod")
tabla_productos_en_1FN  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'productos'])

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

PK_padron_y_rubro = sql^(" SELECT razon_social,establecimiento, rubro FROM padron_mod")
tabla_rubros_en_1FN  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'rubro'])

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
copia_padron = padron_correcto.copy()
copia_padron = sql^("SELECT DISTINCT pais_id, provincia_id, departamento,localidad, rubro, categoria_id, Certificadora_id,razon_social, establecimiento FROM padron_mod")
tabla_paisid_U_pais = sql^ (" SELECT DISTINCT pais_id, pais FROM padron_mod "  )
tabla_provincia_id_U_provincia = sql^("SELECT DISTINCT provincia_id, provincia FROM padron_mod")
tabla_categoria_id_U_categoria_desc = sql^("SELECT DISTINCT categoria_id categoria_desc FROM padron_mod")
tabla_certificadora_id_U_certificadora_deno = sql^("SELECT DISTINCT Certificadora_id, certificadora_deno  FROM padron_mod")

#LOC_SENSALES
copia_loc_censales = loc_cens.copy()
copia_loc_censales= sql ^("SELECT categoria, centroide_Lat, centroide_Lon, departamento_nombre, fuente, id, municipio_id, nombre, provincia_id  FROM localidades_censales_original")
tabla_depto_id_U_depto_nombre = sql^("SELECT DISTINCT departamento_id, departamento_nombre FROM localidades_censales_original")
tabla_muni_id_U_muni_nombre = sql^("SELECT DISTINCT municipio_id, municipio_nombre FROM localidades_censales_original")
tabla_prov_id_U_prov_nombre1 = sql^("SELECT DISTINCT provincia_id, provincia_nombre FROM localidades_censales_original")
tabla_prov_id_U_depto_id_U_muni_id = sql^("SELECT DISTINCT provincia_id, departamento_id, municipio_id FROM localidades_censales_original")


#DICT_DEPTOS
copia_dict_deptos = dict_deptos.copy()
copia_dict_deptos = sql^("SELECT codigo_departamento_indec, id_provincia_indec FROM dict_deptos_original ")
tabla_prov_id_U_prov_nombre2 = sql^("SELECT DISTINCT id_provincia_indec, nombre_provincia_indec FROM dict_deptos_original")
tabla_codigo_depto_U_nombre_depto = sql^("SELECT DISTINCT codigo_departamento_indec, nombre_departamento_indec FROM dict_deptos_original")

#DICT_ACT
copia_dict_act = dict_act.copy()
copia_dict_act =  sql^("SELECT clae2, letra FROM dict_act_original ")
tabla_letra_U_letra_desc = sql^("SELECT DISTINCT letra, letra_desc FROM dict_act_original")
tabla_clae2_U_clae2 = sql^("SELECT DISTINCT clae2, clae2_desc FROM dict_act_original")







#PADRON 3RA FORMA A CSV 
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




