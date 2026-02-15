# Sección 1: Procesamiento y transferencia de datos

## Requisitos:
-Docker
-Docker compose
-Python 3.11
-PostgreSQL 15

## Docker
Se decidió usar Docker como una herramienta para la creación de contenedores, esto nos traerá beneficios como la reproducibilidad del proyecto en diferentes dispositivos.

### Pasos para su instalación:
* Verificar el sistema operativo y sus características, y descargar Docker Desktop en https://www.docker.com/products/docker-desktop/
* Ejecutar el instalador y continuar la instalación hasta terminar. Posteriormente reiniciar la computadora.
* Se puede verificar si la instalación fue correcta abriendo un CMD y escribiendo ``docker --version``

## postgreSQL
Se eligió postgreSQL debido a que ya tenía un poco de experiencia previa usándolo y además porque ofrece robustez, es un sistema ampliamente usado (mucha documentación) con un gran soporte de variables (timestamp, decimal, etc.) y funciona muy bien con Docker y Python.

## Python 3.11
Después de una investigación, la mejor combinación para evitar problemas de compatibilidad y estabilidad, es el uso de python 3.11 (siendo una versión relativamente moderna) y postgreSQL 15. Además se eligió este lenguaje debido a que tiene un gran enfoque en análisis de datos que junto a sus librerías como Pandas, NumPy, SQLAlchemy facilitan la manipulación y transformación de datos de manera eficiente. Por otro lado, python puede conectarse fácilmente a postgreSQL.

## Pasos para la instalación y ejecución del proyecto
```bash
git clone https://github.com/Emi-Mac/PruebaTecnica_DesarrolladorPython.git
cd Seccion1
docker compose up --build
```
Cuando se levantan los contenedores con ``docker compose up --build`` en automático comienza el pipeline etl, así como también la creación de la base de datos. Si se decea volver a correr el pipeline y subir datos a la base de datos se usa:

```bash
docker exec -it etl python etl/main.py
```

Para desactivar los contenedores se usa:

```bash
docker compose down
```

Y si se desea eliminar la base de datos y volume:

```bash
docker compose down -v
```

## Estructura principal
```
Seccion1/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── dataset/
│   └── data_prueba_tecnica.csv
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── sql/
│   └── init.sql
├── pruebasUnitarias
└── README.md
```

Primero se crearon los directorios principales. Se pensó en hacer dos contenedores, uno con la base de datos y otro con los scripts de Python que harán la extracción, transformación y la carga de datos (ETL). Es por eso que se crearon 3 scripts de python que harán dichas funciones y un cuarto script que se llama main.py que es el script que coordina los demás, organiza el flujo y la forma en la se ejecutan.

Posteriormente se creó un archivo docker-compose.yml, aquí se definen los contenedores que se van a crear, sus nombres, usuarios, el nombre de la base de datos, la imagen en la que se basarán para su creación, etc. El servicio *db* que contendrá la base de datos se crea a partir de una imagen oficial de postgres:15, mientras que el servicio *etl* se crea a partir de una imagen construida por un archivo Dockerfile en el directorio, este se basa de la imagen oficial de Python 3.11 y además instala las librerías que se usarán como pandas para la manipulación de los datos, sqlalchemy para la conexión a postgres, psycopg2 que al igual que sqlalchemy trabajan en conjunto para la conexión con postgres como un driver, y pyarrow para exportar los datos a tipo parquet.

Los datos se exportan en formato Parquet porque tiene muchas ventajas en comparación a CSV por ejemplo. Parquet es columnar, es decir, guarda los datos por columna, si se requiere leer una variable, solo lee la columna que le corresponde, haciendo más rápido el proceso y usa menos memoria. Además guarda los datos con todo y su formato (int, float, string, timestamp, etc.)

## Problemas y retos en la extracción y transformación de los datos:
* Agunos campos de la columna *paid_at* están vacíos, la solución fue que se agregó el argumento ``errors = 'coerce'`` en la línea de código que convierte el formato de fecha a timestamp ``pd.to_datetime()`` en el script transform.py, esto hace que cuando hay error al convertir (como cuando no hay un valor o es un valor inconsistente) escribe NaT.
* Agunos formatos vienen mixtos en la columna *created_at*, vienen en formato simple: aaaa-mm-dd o en formato ISO con tiempo: aaaa-mm-ddT00:00:00
Se agregaron los argumentos ``format='mixed'`` y ``errors = 'coerce'`` en ``pd.to_datetime()``.
* El esquema propuesto tenía algunos errores, como definir company_id VARCHAR(24) o el id VARCHAR(24) ya que el id para ambos casos supera los 24 caracteres. La solución fue modificar el tipo de variable en ambas tablas, la de companies y la de charges, se usó VARCHAR(40).
* Surgió un problema con el envio de datos a la base de datos, cuando se envia el timestamp y hay un NaT, SQL no lo detecta como NULL. Para solucionarlo debemos sustituit NaT a None. En el script de transform.py se agregó ``df['paid_at'] = df['paid_at'].where(pd.notnull(df['paid_at']), None)``.
* Ahora surgió un problema porque sigue existiendo algún NaT por ahí, por lo que se prosigió a convertir ahora a todos los valores (en todas las columnas) por None. Esto hizo que existiera otro error, aquí fue cuando pude darme cuenta que había algunos renglones con ID vacíos, por lo que se decidió eliminarlos. Para eliminar los renglones con ID como None, se usó ``df = df.dropna(subset = ['id'])``.
* Había un valor con más de 16 dígitos en la columna *amount*, esto arrojó un error ya que definimos a amount como tipo DECIMAL(16,2). Debido a que es un valor demasiado grande, no tiene sentido, por lo que debe ser un error de dato. Se debe limpiar el dato. Podemos solucionarlo en el script de transform.py usando ``df['amount'] = pd.to_numeric(df['amount']), errors = 'coerce')`` convirtiendo el valor a numérico y luego aplicando un filtro para que eliminemos los datos con números muy grandes o absurdos usando ``df = df[df['amount'].abs() < 1e9]``

## Diagrama de base de datos

![This is an alt text.](/Images/DiagramaBD.jpeg)

## Vista en base de datos

![This is an alt text.](/Images/SS_VIEW.png)

