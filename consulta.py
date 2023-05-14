import pandas as pd
from inline_sql import sql, sql_val







if __name__ == "__main__":
    padron = pd.read_csv(
        "C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_originales_en_1raFN\\Padron_en_3raFN(falta_rubro).csv")
    provincias = pd.read_csv(
        "C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\padron\\tabla_provincia_id_U_provincia.csv")
    deptos = pd.read_csv(
        "C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\loc_sensales\\tabla_depto_id_U_depto_nombre.csv")
    rubro_clae2 = pd.read_csv(
        "C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\1ra_FN\\padron\\rubro_clae2.csv")
    rubros = pd.read_csv(
        "C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\1ra_FN\\padron\\rubros_en1FN.csv")
    provincia = pd.read_csv("C:\\Users\\pablo\\PycharmProjects\\labo-datos\\tablas_creadas\\3ra_FN\loc_sensales\\tabla_prov_id_U_prov_nombre1.csv")
    salario_medio = pd.read_csv("C:\\Users\\pablo\\Downloads\\w_median_depto_priv_clae2.csv")
    consulta3 = """
                    SELECT DISTINCT rc.clae2,rc.clae2_desc, COUNT(*)
                    FROM rubros r
                    INNER JOIN rubro_clae2 rc ON rc.rubro = r.rubro
                    GROUP BY rc.clae2_desc,rc.clae2 
                    """
    tabla3 = sql ^ consulta3

    actividad = tabla3.iloc[0,0]
    actividad = str(actividad)
    consulta4 = '''
                SELECT AVG(w_median) AS promedio FROM salario_medio WHERE clae2 = $actividad AND fecha = '2022-12-01' AND w_median > 0
    '''

    print(sql ^ consulta4)
    con = '''SELECT YEAR(CAST(fecha AS DATE)) as fecha,AVG(w_median) promedio_anual,stddev(w_median) AS desvio_estandar FROM salario_medio GROUP BY YEAR(CAST(fecha AS DATE)) ORDER BY fecha'''
    print(sql^con)
    provincial = '''
                SELECT YEAR(CAST(fecha AS DATE)) as fecha,p.provincia_nombre as provincia,AVG(w_median) AS promedio_anual_provincial,stddev(w_median) AS desvio_estandar FROM salario_medio s INNER JOIN provincia p 
                ON p.provincia_id = s.id_provincia_indec GROUP BY YEAR(CAST(fecha AS DATE)),p.provincia_nombre ORDER BY YEAR(CAST(fecha AS DATE))
    
    '''
    print(sql^provincial)