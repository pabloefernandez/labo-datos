#!/usr/bin/env python3

import pandas as pd
from inline_sql import sql, sql_val

#padron= pd.read_csv("/home/tsl2004/Escritorio/labo-datos/tablas_originales/padron-de-operadores-organicos-certificados.csv")
#dict_salario = pd.read_csv("")
localidades_censales =  pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_originales_en_1raFN\\loc_sensales_1raFN.csv")
#dict_deptos =  pd.read_csv("diccionario_cod_depto.csv")
#dict_act = pd.read_csv("diccionario_clae2.csv")
padron= pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_originales_en_1raFN\\Padron_en_3raFN(falta_rubro).csv")
provincias =pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\padron\\tabla_provincia_id_U_provincia.csv")
deptos = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\loc_sensales\\tabla_depto_id_U_depto_nombre.csv")
rubro_clae2 = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\1ra_FN\\padron\\rubro_clae2.csv")
rubros = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\1ra_FN\\padron\\rubros_en1FN.csv")

consulta_1 = """
                SELECT DISTINCT provincias.provincia, count(*) as cant_operadores 
                FROM padron
                INNER JOIN provincias
                ON provincias.provincia_id = padron.provincia_id
                GROUP BY provincias.provincia;


             """

ej1 = sql^consulta_1
#print(ej1)

consultaa = '''
SELECT UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(localidades_sensales.departamento_nombre,'á','a'),'é','e'),'í','i'),'ó','o'),'ú','u')) as departamento_loc'''
consulta2 = """"
            
                SELECT DISTINCT loc.sensales.departamentos
                FROM loc sensales
                EXCEPT(
                    SELECT DISTINCT padron.departamentos
                    FROM padron
                    )

                """
ej2 = sql^consulta2
print(ej2)

consulta3 = """
                SELECT r.rubro, COUNT(*)
                FROM rubros r
                INNER JOIN rubro_clae2 rc ON rc.rubro = r.rubro
                GROUP BY r.rubro 
                """
print(sql^consulta3)

# 4)iv) ¿Cuál fue el salario promedio de esa actividad en 2022? (si hay varios
#       registros de salario, mostrar el más actual de ese año)



#tabla_productos = pd.read_csv('/home/tsl2004/Escritorio/labo-datos/tablas_creadas/1ra_FN/padron/tabla_productos_mod.csv')


#CONSULTAS

padroncito = sql^(" SELECT razon_social,establecimiento, rubro FROM padron")


tabla_productos_modificada  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'productos'])




                                  
                                  

#FUNCIONES  
  
def primera_forma_normal_productos(df,nuevo_df):
   for i in range(len(df)):
        productos = df.iloc[i,2].split(" Y ")
        for producto in productos:
            producto = producto.lstrip()
            nuevo_df.loc[len(nuevo_df)] = [df.iloc[i,0],df.iloc[i,1],producto] 
   return nuevo_df

#print(primera_forma_normal_productos(productos, tabla_productos_modificada))

#tabla_productos_modificada.to_csv("tabla_productos_mod.csv",index= False)

tabla_rubros  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'rubro'])

def primera_forma_normal_rubro(df,nuevo_df):
    for i in range(len(df)):
        rubros = re.split(" Y | y |/",df.iloc[i,2])
        for rubro in rubros:
            rubro = rubro.lstrip()
            nuevo_df.loc[len(nuevo_df)] = [df.iloc[i,0],df.iloc[i,1],rubro] 
    return nuevo_df

print(primera_forma_normal_rubro(padroncito, tabla_rubros))

tabla_rubros.to_csv("rubros_en1FN", index = False)


