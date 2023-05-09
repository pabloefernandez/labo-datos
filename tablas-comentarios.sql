DROP DATABASE IF EXISTS padron;
CREATE DATABASE padron;
USE padron;


CREATE TABLE Departamento(
departamento_id INT,
departamento VARCHAR(50),
CONSTRAINT PK_departamento PRIMARY KEY (departamento_id)
)engine=innodb;

CREATE TABLE Pais(
 pais_id INT,
 pais VARCHAR(20),
 CONSTRAINT PK_paispk PRIMARY KEY (pais_id)
 )engine=innodb;

CREATE TABLE Provincia(
provincia_id INT,
provincia VARCHAR(50),
CONSTRAINT PK_provincia_id PRIMARY KEY (provincia_id)
)engine=innodb;

CREATE TABLE Letra(
letra CHAR,
letra_desc VARCHAR(60),
CONSTRAINT PK_letra PRIMARY KEY (letra)
)engine=innodb;

CREATE TABLE Categoria ( /* SOLO TIENE PRODUCTORES */
categoria_id INT,
categoria_desc VARCHAR(20),
CONSTRAINT PK_categoria_id PRIMARY KEY (categoria_id)
)engine=innodb;

CREATE TABLE Certificadora(
certificadora_id INT,
certificadora_deno VARCHAR(20),
CONSTRAINT PK_certificadora_id PRIMARY KEY (certificadora_id)
)engine=innodb;

CREATE TABLE Municipio(
municipio_id INT,
municipio_nombre VARCHAR(50),
CONSTRAINT PK_municipio_id PRIMARY KEY (municipio_id)
)engine=innodb;


CREATE TABLE Municipio_Departamento_Provincia(
municipio_id INT,
departamento_id INT,
provincia_id INT,
CONSTRAINT PK_municipio_dpto PRIMARY KEY (municipio_id,departamento_id),
CONSTRAINT FK_provincia_id FOREIGN KEY (provincia_id) REFERENCES Provincia (provincia_id),
CONSTRAINT FK_municipio_id FOREIGN KEY (municipio_id) REFERENCES Municipio (municipio_id),
CONSTRAINT FK_departamento_id FOREIGN KEY (departamento_id) REFERENCES Departamento (departamento_id)
)engine=innodb;


CREATE TABLE Localidades_Censales(
id INT,
nombre VARCHAR(50),
categoria VARCHAR(50),
centroide_lat VARCHAR(50),
centroide_lon VARCHAR(50),
departamento_id INT,
fuente VARCHAR(10),
municipio_id INT,
CONSTRAINT PK_id PRIMARY KEY (id),
CONSTRAINT FK_depto FOREIGN KEY (municipio_id,departamento_id) REFERENCES Municipio_Departamento_Provincia (municipio_id,departamento_id)
)engine=innodb;


CREATE TABLE Padron(
razon_social VARCHAR(20),
establecimiento VARCHAR(20),
pais_id INT,
provincia_id INT,
categoria_id INT,
departamento VARCHAR(50), /* SI DEPARTAMENTO Y LOCALIDAD DETERMINAN LA PROVINCIA Y EL PAIS ENTONCES TENDRIA QUE ARMAR OTRA TABLA*/
localidad VARCHAR(50),
certificadora_id INT,
CONSTRAINT PK_primarykey PRIMARY KEY (establecimiento,razon_social),
CONSTRAINT FK_pais FOREIGN KEY (pais_id) REFERENCES Pais (pais_id),
CONSTRAINT FK_provincia FOREIGN KEY (provincia_id) REFERENCES Provincia (provincia_id),
CONSTRAINT FK_categoria_id FOREIGN KEY (categoria_id) REFERENCES Categoria (categoria_id),
CONSTRAINT FK_certificadora_id FOREIGN KEY (certificadora_id) REFERENCES Certificadora (certificadora_id)
)engine=innodb;

CREATE TABLE Diccionario_clae2(
clae2 INT,
clae2_desc VARCHAR(50),
letra CHAR,
CONSTRAINT PK_clae2 PRIMARY KEY (clae2),
CONSTRAINT FK_letra FOREIGN KEY (letra) REFERENCES Letra(letra)
)engine=innodb;

CREATE TABLE Rubro_Clae2(
rubro VARCHAR(50),
clae2 INT,
CONSTRAINT PK_rubro PRIMARY KEY (rubro),
CONSTRAINT FK_fk FOREIGN KEY (clae2) REFERENCES Diccionario_clae2(clae2)
)engine=innodb;

CREATE TABLE Rubro_Razon_Social_Establecimiento (
razon_social VARCHAR(20),
establecimiento VARCHAR(20),
rubro VARCHAR(20),
CONSTRAINT PK_pk PRIMARY KEY (establecimiento,razon_social),
CONSTRAINT FK_primarykey FOREIGN KEY (establecimiento,razon_social) REFERENCES Padron (establecimiento,razon_social),
CONSTRAINT FK_rubro FOREIGN KEY (rubro) REFERENCES Rubro_Clae2 (rubro)
)engine=innodb;

CREATE TABLE Producto(
razon_social VARCHAR(20),
establecimiento VARCHAR(20),
producto VARCHAR(30),
CONSTRAINT PK_pkk PRIMARY KEY (establecimiento,razon_social),
CONSTRAINT FK_razon FOREIGN KEY (establecimiento,razon_social) REFERENCES Padron (establecimiento,razon_social)
)engine=innodb;

CREATE TABLE Salario_Medio(
codigo_departamento_indec INT,
id_provincia_indec INT,
clae2 INT,
fecha DATE,
w_median INT,
CONSTRAINT PK_pk PRIMARY KEY (codigo_departamento_indec,id_provincia_indec),
CONSTRAINT FK_fk22 FOREIGN KEY (codigo_departamento_indec) REFERENCES Departamento (departamento_id),
CONSTRAINT FK_fk23 FOREIGN KEY (id_provincia_indec) REFERENCES Provincia (provincia_id),
CONSTRAINT FK_fk33 FOREIGN KEY (clae2) REFERENCES Diccionario_clae2 (clae2)
)engine=innodb;
