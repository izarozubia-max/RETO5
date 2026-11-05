# Reto 5 — API REST de préstamos

La API REST del Reto 5 permite consultar los préstamos almacenados en MySQL, filtrar por impago y obtener estadísticas generales. También consulta un servicio externo de tipos de cambio. Power BI utiliza el endpoint `/prestamos` como origen de datos.

## Requisitos

- Docker Desktop instalado y en funcionamiento.
- El archivo `datos_powerbi.csv` en la carpeta local `docker_reto_5_alumnos/datos/`.

Los datos originales, los datasets generados y los modelos entrenados se mantienen fuera del repositorio.

## Arranque

Desde la raíz del repositorio, ejecuta:

```powershell
cd docker_reto_5_alumnos
docker compose up --build
```

Docker Compose arranca MySQL, ejecuta el cargador de datos y después inicia la API Flask. La configuración de conexión a MySQL se proporciona en `docker-compose.yml`.

| Servicio | Dirección |
|---|---|
| API Flask | `http://localhost:8000` |
| MySQL desde el ordenador | `localhost:3307` |
| MySQL entre contenedores | `db:3306` |

La base de datos se llama `creditos` y los préstamos se almacenan en la tabla `clientes_credito`. Para comprobar la conexión, abre `http://localhost:8000/estado`.

## Estructura

Las rutas de esta tabla son relativas a `docker_reto_5_alumnos/`.

| Ruta | Contenido |
|---|---|
| `api/main.py` | Endpoints de Flask, consultas SQL mediante SQLAlchemy e integración con la API externa. |
| `api/requirements.txt` | Dependencias de la API. |
| `api/Dockerfile` | Configuración de la imagen de la API. |
| `loader/load_data.py` | Lectura del CSV y carga de los datos en MySQL. |
| `loader/requirements.txt` | Dependencias del cargador. |
| `loader/Dockerfile` | Configuración de la imagen del cargador. |
| `datos/datos_powerbi.csv` | Archivo de entrada que debe colocarse localmente. |
| `docker-compose.yml` | Configuración de MySQL, el cargador, la API y el volumen. |

## Persistencia y recarga de datos

MySQL conserva los datos en un volumen de Docker. `docker compose down` detiene y retira los contenedores, pero conserva el volumen. Para volver a arrancar los servicios, ejecuta `docker compose up`.

La variable `FORCE_RELOAD` del servicio `cargar_datos` controla la carga del CSV:

- `"false"` conserva la tabla si ya contiene datos.
- `"true"` sustituye la tabla con los datos del CSV al ejecutar el cargador. Después de la recarga, vuelve a dejarla en `"false"`.

El comando `docker compose down -v` elimina el volumen y sus datos. En el siguiente arranque, el cargador necesitará el CSV para volver a crear la tabla.

## Endpoints

Todos los endpoints utilizan el método `GET` y devuelven JSON en las respuestas que controla la aplicación. Las peticiones no requieren cuerpo ni autenticación en el entorno local de prácticas.

| Ruta | Descripción | Códigos previstos |
|---|---|---|
| `/` | Comprueba que la API está en marcha. | `200` |
| `/estado` | Comprueba la conexión con MySQL. | `200` |
| `/prestamos` | Devuelve todos los préstamos ordenados por `row_id`, en la clave `prestamos`. | `200` |
| `/prestamos/<id_prestamo>` | Devuelve un préstamo por su identificador, en la clave `prestamo`. | `200`, `404` |
| `/prestamos/impago/<impago>` | Filtra los préstamos por impago y devuelve la lista en la clave `clientes`. | `200`, `400` |
| `/estadisticas` | Devuelve medias y totales calculados en MySQL, en la clave `estadisticas`. | `200` |
| `/monedas` | Consulta los tipos de cambio con el euro como moneda base. | `200`, `502`, `503` |

`id_prestamo` es el identificador de texto del préstamo. `impago` admite `0` para préstamos sin impago y `1` para préstamos con impago. Un entero como `2` devuelve `400 Bad Request`. Una ruta con un valor que no coincide con el tipo esperado, como `/prestamos/impago/abc`, devuelve `404 Not Found`.

### Ejemplos de peticiones

| Petición | Respuesta esperada |
|---|---|
| `GET /prestamos/KG9CT9` | `200 OK` y los datos del préstamo en `prestamo`. |
| `GET /prestamos/NOEXISTE` | `404 Not Found` y `{"error": "Préstamo no encontrado"}`. |
| `GET /prestamos/impago/1` | `200 OK` y la lista de préstamos con impago en `clientes`. |
| `GET /prestamos/impago/2` | `400 Bad Request` y `{"error": "El impago debe ser 0 o 1"}`. |

### Estadísticas generales

`GET /estadisticas` devuelve los siguientes campos dentro del objeto `estadisticas`.

| Campo | Significado |
|---|---|
| `total_prestamos` | Número total de préstamos. |
| `edad_media` | Edad media de los prestatarios. |
| `ingresos_medios` | Ingresos anuales medios. |
| `monto_medio` | Importe inicial medio de los préstamos. |
| `total_impagos` | Número de préstamos con impago observado. |

### Tipos de cambio

`GET /monedas` consulta `https://open.er-api.com/v6/latest/EUR` mediante `requests`, con un tiempo de espera configurado de 5 segundos. Devuelve `moneda_base` y `tipos_cambio`.

La API devuelve `502` si la respuesta externa no contiene los campos esperados o el JSON es inválido. Devuelve `503` si falla la conexión, se supera el tiempo de espera o el proveedor devuelve un error HTTP. Los fallos inesperados del servidor pueden generar un `500`.

## Pruebas funcionales

Para reproducir las pruebas en Postman, mantén Docker en marcha y añade `http://localhost:8000` delante de cada ruta. Comprueba el código HTTP y el contenido de la respuesta. Los ejemplos anteriores cubren una consulta por ID válida, un ID inexistente y un filtro por impago válido e inválido. Comprueba también que `/estadisticas` devuelve los totales y medias y que `/monedas` devuelve los tipos de cambio con base EUR.