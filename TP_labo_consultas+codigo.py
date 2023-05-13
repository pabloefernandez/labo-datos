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


