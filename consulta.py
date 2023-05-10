import pandas as pd
from inline_sql import sql, sql_val







if __name__ == "__main__":

    padron = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_originales_en_1raFN\\Padron_en_3raFN.csv")
    municipio_dpto_prov = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\loc_sensales\\tabla_prov_id_U_depto_id_U_muni_id.csv")
    localidades = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_originales_en_1raFN\\loc_sensales_1raFN.csv")
    rubros = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\1ra_FN\padron\\rubros_en1FN")
    consulta = sql ^ '''
                        SELECT p1.provincia_id FROM padron p1 WHERE p1.provincia_id IN
                        (SELECT p2.provincia_id FROM padron p2 WHERE p1.provincia_id != p2.provincia_id AND p1.localidad = p2.localidad
                        AND p1.departamento = p2.departamento)
    
    
    '''
    consulta_localidad = sql ^ '''SELECT DISTINCT departamento_id,municipio_id FROM localidades'''#1847
    print(consulta_localidad.head(1847))
    otra = sql ^ '''
                SELECT DISTINCT departamento_id,municipio_id FROM municipio_dpto_prov
    '''
    #print(otra)