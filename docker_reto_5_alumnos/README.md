# RETO 5 — API de préstamos

Este proyecto proporciona un entorno Docker con una API REST desarrollada
con Flask y una base de datos MySQL, cargada a partir del archivo
`datos/datos_powerbi.csv`.

La API permite consultar préstamos, obtener estadísticas e incorporar
tipos de cambio de una API externa. Power BI utiliza `/prestamos`
para cargar los datos.

## Requisitos

- Docker Desktop instalado y en funcionamiento.
- Archivo `datos_powerbi.csv` disponible en la carpeta `datos/`
  del entorno Docker.

Los datasets y los modelos entrenados no se incluyen en el repositorio.

## Arranque

Desde la carpeta `docker_reto_5_alumnos`, donde se encuentra
`docker-compose.yml`, ejecutar:

```bash
docker compose up --build
```

Servicios disponibles:

- API Flask: http://localhost:8000
- MySQL desde el ordenador: `localhost:3307`
- MySQL entre contenedores: `db:3306`
- Base de datos: `creditos`
- Usuario: `clase`
- Contraseña del entorno de prácticas: `clase123`
- Tabla: `clientes_credito`

Para comprobar la conexión con MySQL:

http://localhost:8000/estado

## Estructura del entorno Docker

| Ruta | Contenido |
|---|---|
| `api/main.py` | Rutas y lógica de la API Flask. |
| `api/requirements.txt` | Dependencias de la API. |
| `api/Dockerfile` | Configuración de la imagen de la API. |
| `loader/load_data.py` | Lectura, preparación y carga de los datos en MySQL. |
| `loader/requirements.txt` | Dependencias del cargador. |
| `loader/Dockerfile` | Configuración de la imagen del cargador. |
| `datos/datos_powerbi.csv` | Dataset de entrada, disponible solo localmente. |
| `docker-compose.yml` | Configuración de los servicios, red y volumen. |

## Persistencia de datos

MySQL almacena los datos en un volumen Docker. Estos se mantienen
aunque se detengan o eliminen los contenedores mediante:

```bash
docker compose down
```

Para volver a iniciar los servicios:

```bash
docker compose up
```

El siguiente comando elimina también el volumen y los datos almacenados:

```bash
docker compose down -v
```

En el siguiente arranque, el cargador volverá a crear la tabla a partir
del CSV, que deberá estar disponible en `datos/`.

La variable `FORCE_RELOAD` del servicio `cargar_datos` controla la recarga:

- `"false"`: conserva la tabla si ya está cargada.
- `"true"`: fuerza la sustitución de la tabla con los datos del archivo.

Después de una recarga, se recomienda volver a dejarla en `"false"`.

## API REST

La URL base es:

```text
http://localhost:8000
```

Todos los endpoints utilizan el método GET y devuelven JSON.
En este entorno de prácticas no se requiere autenticación.

### Endpoints

| Método | Ruta | Descripción | Códigos previstos |
|---|---|---|---|
| GET | `/` | Mensaje de funcionamiento de la API. | 200 |
| GET | `/estado` | Comprueba la conexión con MySQL. | 200 |
| GET | `/prestamos` | Devuelve todos los préstamos. | 200 |
| GET | `/prestamos/<id_prestamo>` | Consulta un préstamo por ID. | 200, 404 |
| GET | `/prestamos/impago/<impago>` | Filtra los préstamos por impago. | 200, 400 |
| GET | `/estadisticas` | Devuelve estadísticas generales. | 200 |
| GET | `/monedas` | Consulta tipos de cambio con base EUR. | 200, 502, 503 |

Los fallos inesperados del servidor pueden generar un código 500.

### Parámetros

| Parámetro | Tipo | Descripción |
|---|---|---|
| `id_prestamo` | Texto | Identificador único del préstamo, por ejemplo `KG9CT9`. |
| `impago` | Entero | `0`: sin impago; `1`: con impago. |

En el filtro por impago, otro entero admitido por la ruta, como `2`,
devuelve un error 400. Un valor que no coincide con el tipo de la ruta,
como `abc`, devuelve un 404 de Flask.

Ninguna de estas peticiones GET necesita un body.

### Consulta de todos los préstamos

```http
GET http://localhost:8000/prestamos
```

Devuelve un objeto con la clave `prestamos`, que contiene una lista
con todos los registros de la tabla.

Actualmente, las columnas numéricas del CSV se devuelven como texto.
Sus tipos se convierten en Power Query para realizar las visualizaciones.

### Consulta de un préstamo

```http
GET http://localhost:8000/prestamos/KG9CT9
```

Respuesta: **200 OK**.

Extracto de la respuesta:

```json
{
  "prestamo": {
    "id": "KG9CT9",
    "edad": "34",
    "ingresos": "56572",
    "monto_inicial": "73978",
    "impago": "0"
  }
}
```

La respuesta completa incluye el resto de las columnas del préstamo.

Si el identificador no existe:

```http
GET http://localhost:8000/prestamos/NOEXISTE
```

Respuesta: **404 Not Found**.

```json
{
  "error": "Préstamo no encontrado"
}
```

### Filtro por impago

Para consultar los préstamos con impago:

```http
GET http://localhost:8000/prestamos/impago/1
```

Para consultar los préstamos sin impago:

```http
GET http://localhost:8000/prestamos/impago/0
```

Ambas peticiones devuelven **200 OK** y un objeto con la clave
`clientes`, que contiene la lista de préstamos seleccionados.
Esta clave se mantiene con el nombre utilizado en la implementación.

Un valor no permitido:

```http
GET http://localhost:8000/prestamos/impago/2
```

Devuelve **400 Bad Request**:

```json
{
  "error": "El impago debe ser 0 o 1"
}
```

### Estadísticas generales

```http
GET http://localhost:8000/estadisticas
```

Devuelve **200 OK** y un objeto con la clave `estadisticas`,
que contiene:

| Campo | Significado |
|---|---|
| `total_prestamos` | Número total de préstamos. |
| `edad_media` | Edad media de los prestatarios. |
| `ingresos_medios` | Ingresos anuales medios. |
| `monto_medio` | Importe inicial medio de los préstamos. |
| `total_impagos` | Número de préstamos con impago observado. |

### API externa de tipos de cambio

```http
GET http://localhost:8000/monedas
```

Consulta el servicio externo:

https://open.er-api.com/v6/latest/EUR

Se utiliza `requests` para realizar la petición, con un timeout de
5 segundos, comprobación de errores HTTP y gestión de excepciones.

La respuesta contiene:

- `moneda_base`: moneda de referencia, EUR.
- `tipos_cambio`: equivalencia de un euro en las monedas disponibles.

El endpoint proporciona tipos de cambio para posibles comparaciones
de importes en otras monedas. No convierte automáticamente los
importes de los préstamos.

Errores controlados:

| Código | Situación |
|---|---|
| 502 | La respuesta no contiene los campos necesarios o no es un JSON válido. |
| 503 | Se produce una excepción de `requests`, por ejemplo por conexión, timeout o error HTTP del proveedor. |

## Códigos HTTP

| Código | Significado |
|---|---|
| 200 | Petición realizada correctamente. |
| 400 | Valor de entrada no permitido. |
| 404 | Recurso o ruta no encontrados. |
| 500 | Error inesperado del servidor. |
| 502 | Respuesta externa no válida. |
| 503 | No se pudo completar la consulta al servicio externo. |

## Pruebas funcionales

Se han realizado pruebas manuales con Postman, manteniendo los
servicios Docker en funcionamiento.

| Prueba | Resultado comprobado |
|---|---|
| Consultar un préstamo existente. | 200 y datos del préstamo. |
| Consultar un préstamo inexistente. | 404 y mensaje de error. |
| Filtrar por impago con un valor válido. | 200 y lista de registros. |
| Filtrar por impago con el valor 2. | 400 y mensaje de validación. |
| Consultar las estadísticas. | 200 y estadísticas generales. |
| Consultar los tipos de cambio. | 200 y tipos de cambio con base EUR. |

## Conexión con Power BI

1. Mantener los servicios Docker en funcionamiento.
2. En Power BI Desktop, seleccionar **Obtener datos → Web**.
3. Introducir `http://localhost:8000/prestamos`.
4. Seleccionar autenticación anónima si se solicita.
5. Convertir la lista de préstamos en tabla y expandir los registros.
6. Asignar los tipos de datos correspondientes.

Para convertir las columnas decimales recibidas como texto con punto,
utilizar **Cambiar tipo → Usar configuración regional → Número decimal
→ Inglés (Estados Unidos)**.

## Datos y modelos

No se incluyen en Git los datos originales, los datasets generados
ni los modelos entrenados.

Los archivos necesarios deben colocarse localmente en las rutas
indicadas antes de ejecutar el proyecto.