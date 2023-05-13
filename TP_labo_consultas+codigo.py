#!/usr/bin/env python3



padron= pd.read_csv("/home/tsl2004/Escritorio/labo-datos/tablas_originales/padron-de-operadores-organicos-certificados.csv")
#dict_salario = pd.read_csv("")
localidades_censales =  pd.read_csv("localidades-censales.csv")
dict_deptos =  pd.read_csv("diccionario_cod_depto.csv")
dict_act = pd.read_csv("diccionario_clae2.csv")
padron= pd.read_csv("Padron_en_3raFN.csv")
provincias =pd.read_csv("tabla_provincia_id_U_provincia.csv")

ej1 = sql^consulta_1
consulta_1 = """
                SELECT DISTINCT provincias.provincia, count(*) as cant_operadores 
                FROM padron
                INNER JOIN provincias
                ON provincias.provincia_id = padron.provincia_id
                GROUP BY provincias.provincia;


             """
print(ej1)


tabla_productos = pd.read_csv('/home/tsl2004/Escritorio/labo-datos/tablas_creadas/1ra_FN/padron/tabla_productos_mod.csv')


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


#TABLAS CREADAS}
#tabla_productos  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'productos'])
#tabla_productos.to_csv("tabla_productos.csv",index= False)

#tabla_productos_modificada  = pd.DataFrame(columns=['establecimiento' , 'razon_social', 'productos'])
#tabla_productos_modificada.to_csv("tabla_productos_mod.csv",index= False)

"""
TODO A 3RA FORMA 
#PADRON 3RA FORMA
copia_padron = padron.copy()
copia_padron = sql^("SELECT DISTINCT pais_id, provincia_id, departamento,localidad, rubro, categoria_id, Certificadora_id,razon_social, establecimiento FROM padron")
tabla_paisid_U_pais = sql^ (" SELECT DISTINCT pais_id, pais FROM padron "  )
tabla_provincia_id_U_provincia = sql^("SELECT DISTINCT provincia_id, provincia FROM padron")
tabla_categoria_id_U_categoria_desc = sql^("SELECT DISTINCT categoria_id categoria_desc FROM padron")
tabla_certificadora_id_U_certificadora_deno = sql^("SELECT DISTINCT Certificadora_id, certificadora_deno  FROM padron")

#LOC_SENSALES
copia_loc_censales = localidades_censales.copy()
copia_loc_censales= sql ^("SELECT categoria, centroide_Lat, centroide_Lon, departamento_id, fuente, id, municipio_id, nombre, provincia_id  FROM localidades_censales")
tabla_depto_id_U_depto_nombre = sql^("SELECT DISTINCT departamento_id, departamento_nombre FROM localidades_censales")
tabla_muni_id_U_muni_nombre = sql^("SELECT DISTINCT municipio_id, municipio_nombre FROM localidades_censales")
tabla_prov_id_U_prov_nombre1 = sql^("SELECT DISTINCT provincia_id, provincia_nombre FROM localidades_censales")
tabla_prov_id_U_depto_id_U_muni_id = sql^("SELECT DISTINCT provincia_id, departamento_id, municipio_id FROM localidades_censales")


#DICT_DEPTOS
copia_dict_deptos = dict_deptos.copy()
copia_dict_deptos = sql^("SELECT codigo_departamento_indec, id_provincia_indec FROM dict_deptos ")
tabla_prov_id_U_prov_nombre2 = sql^("SELECT DISTINCT id_provincia_indec, nombre_provincia_indec FROM dict_deptos")
tabla_codigo_depto_U_nombre_depto = sql^("SELECT DISTINCT codigo_departamento_indec, nombre_departamento_indec FROM dict_deptos")






#DICT_ACT
copia_dict_act = dict_act.copy()
copia_dict_act =  sql^("SELECT clae2, letra FROM dict_act ")
tabla_letra_U_letra_desc = sql^("SELECT DISTINCT letra, letra_desc FROM dict_act")
tabla_clae2_U_clae2 = sql^("SELECT DISTINCT clae2, clae2_desc FROM dict_act")


#PADRON 3RA FORMA A CSV 
copia_padron.to_csv("Padron_en_3raFN(falta_rubro).csv", index = False)

tabla_paisid_U_pais.to_csv("tabla_pais_id_U_pais.csv" ,index= False)
tabla_provincia_id_U_provincia.to_csv("tabla_provincia_id_U_provincia.csv",index= False)
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
