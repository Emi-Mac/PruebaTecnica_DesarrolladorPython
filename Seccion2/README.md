# Sección 2: Creación de una API

## Requisitos:
-Docker
-Docker compose
-Python 3.11

## Docker
Se decidió usar Docker como una herramienta para la creación de contenedores, esto nos traerá beneficios como la reproducibilidad del proyecto en diferentes dispositivos.

### Pasos para su instalación:
* Verificar el sistema operativo y sus características, y descargar Docker Desktop en https://www.docker.com/products/docker-desktop/
* Ejecutar el instalador y continuar la instalación hasta terminar. Posteriormente reiniciar la computadora.
* Se puede verificar si la instalación fue correcta abriendo un CMD y escribiendo ``docker --version``

## Análisis del problema:
Si tenemos un conjunto con 100 números naturales, entonces según la formula de Gauss para la suma de los primeros n números naturales es:

suma = n(n+1)/2

Para los primeros 100 números sería sumacien = 100(100+1)/2 = 5050.

Así que si quitamos un número entre 1 y 100 entonces podemos calcularlo sumando los naturales del 1 al 100 con el número faltante y comparar el total con el que deberíamos tener (5050).

faltante = 5050-sumafaltante

## Estructura principal
```
Seccion2/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── numfalt/
│   ├── number_set.py
│   └── main.py
├── pruebas
└── README.md
```

## Pasos para la instalación y ejecución del proyecto
```bash
git clone https://github.com/Emi-Mac/PruebaTecnica_DesarrolladorPython.git
cd Seccion2
docker compose up --build
```
Cuando se levantan los contenedores con ``docker compose up --build`` en automático se levanta el servidor y la aplicación funciona como una API.

Para desactivar el contenedor o parar el servidor se puede usar *ctr + c* o en la terminal se escribe:

```bash
docker compose down
```

Ahora bien. Podemos ejecutar el programa en un ambiente virtual con python 3.11 y los requerimientos necesarios en requirements.txt, o usando un contenedor de Docker.

### Usando un ambiente virtual
Para correr en un ambiente virtual, es conveniente cambiar al directorio seccion2\pruebas. En windows para crear un ambiente virtual se usa
```bash
py -3.11 -m venv <nombre del ambiente>
```
Pero en este caso ya tenemos un ambiente virtual, por lo que se activa con

```bash
venv\Scripts\activate
```

Para desactivar el ambiente virtual simplemente se escribe

```bash
deactivate
```

Para levantar el servidor de forma local, se ejecuta en la terminal:

```bash
uvicorn main:app
```

y luego en el navegador del mismo dispositivo escribir http://127.0.0.1:8000/docs para probar el endpoint.

O si se quiere ejecutar en terminal, se debe enviar como tipo POST, por eso se escribe:

```bash
curl -X POST http://127.0.0.1:8000/extract/<numero>
```

Para cumplir con que la aplicación debe poder ejecutarse con un argumento introducido por el usuario, entonces se creó un bloque ``if __name__ = "__main__":`` para que sea ejecutado como script y no como API.

Cuando ejecutamos en terminal ``uvicorn main:app``, entonces levantamos el servidor y nuestro script se convierte en una API.

Por otro lado, si ejecutamos en la terminal ``python main.py`` entonces se ejecuta el bloque y ``main.py`` funciona como script ejecutable.

Ahora, para ejecutar la aplicación con un argumento introducido por el usuario, debe escribirse como:

```bash
python numfalt\main.py <numero>
```

donde ``<numero>`` es el argumento (número a extraer)

### Usando Docker

Ahora, usando Docker, primero debemos estar en la carpeta raíz *Seccion2*. Aquí ya debemos tener construido la imagen del contenedor y el contenedor que tendrá los scripts de python y haber ejecutado ``docker compose down``.

para ejecutar la aplicación con un argumento introducido por el usuario, se escribe en la terminal:

```bash
docker compose run numfalt python -m numfalt.main <numero>
```

Para levantar la aplicación como una API, entonces en la terminal se ejecuta:

```bash
docker compose up
```

y en automático se iniciará el servidor.

Posteriormente en un buscador en el mismo dispositivo se puede conectar al servidor y probar el endpoint escribiendo http://localhost:8000/docs

o bien en la terminal enviendo el request como tipo POST se escribe:

```bash
curl -X POST http://localhost:8000/extract/<numero>
```