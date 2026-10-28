
# API REST de clientes y créditos

## 1. Descripción

Esta API está desarrollada con Flask y permite consultar información relacionada con clientes y créditos. Utiliza una base de datos MySQL para realizar consultas y también se conecta a una API externa para obtener tipos de cambio de monedas.

La API devuelve las respuestas en formato JSON.

## 2. Tecnologías utilizadas

- Python.
- Flask, para crear los endpoints.
- SQLAlchemy, para conectarse a la base de datos.
- MySQL, como sistema de gestión de bases de datos.
- Open ER API, para consultar los tipos de cambio de monedas.

## 3. Ejecución de la API

Para ejecutar la API es necesario tener instaladas las dependencias y configurar la variable de entorno `DATABASE_URL` con los datos de conexión a MySQL.

Después, se ejecuta el archivo principal:

```bash
python main.py
```

La API estará disponible en el puerto 8000.

## 4. Endpoints disponibles

Todos los endpoints utilizan el método HTTP `GET`.

### 4.1. Página principal

**Ruta:** `/`

Comprueba que la API está funcionando.

**Respuesta de ejemplo:**

```json
{
  "mensaje": "API Flask funcionando"
}
```

### 4.2. Consulta de préstamos

**Ruta:** `/prestamos`

Consulta los primeros 10 registros de la tabla `clientes_credito`, ordenados por `row_id`.

**Respuesta:** devuelve un objeto JSON con una lista de préstamos.

### 4.3. Comprobación de conexión

**Ruta:** `/estado`

Comprueba que la conexión con MySQL funciona correctamente mediante una consulta sencilla.

**Respuesta de ejemplo:**

```json
{
  "mensaje": "Conexión con MySQL correcta"
}
```

### 4.4. Consulta de clientes

**Ruta:** `/clientes`

Actualmente devuelve un mensaje indicando que se trata de la consulta de todos los clientes. Todavía no realiza una consulta a la base de datos.

### 4.5. Consulta de un cliente

**Ruta:** `/clientes/{id_cliente}`

Recibe el identificador de un cliente como parte de la URL.

**Ejemplo:** `/clientes/123`

Actualmente devuelve el identificador recibido, pero todavía no busca al cliente en la base de datos.

### 4.6. Filtrado por impago

**Ruta:** `/clientes/impago/{impago}`

Permite indicar si se quiere filtrar por clientes con impago o sin él.

- `0`: sin impago.
- `1`: con impago.

**Ejemplo:** `/clientes/impago/1`

Si se introduce un valor distinto de 0 o 1, devuelve un error con código HTTP 400.

Actualmente no realiza el filtrado real en la base de datos.

### 4.7. Estadísticas generales

**Ruta:** `/estadisticas`

Está destinada a ofrecer estadísticas generales relacionadas con los créditos. Actualmente solo devuelve un mensaje informativo.

### 4.8. Análisis de un cliente

**Ruta:** `/clientes/{id_cliente}/analisis`

Recibe el identificador de un cliente y está destinada a realizar un análisis individual. Actualmente devuelve el identificador y un mensaje, sin realizar cálculos.

**Ejemplo:** `/clientes/123/analisis`

### 4.9. Consulta de tipos de cambio

**Ruta:** `/monedas`

Consulta la API externa `https://open.er-api.com/v6/latest/EUR` para obtener los tipos de cambio con el euro como moneda base.

Devuelve la moneda base y los tipos de cambio obtenidos.

Si se produce un error durante la consulta, devuelve un mensaje de error con código HTTP 500.

## 5. Códigos de respuesta

- `200 OK`: la petición se ha procesado correctamente.
- `400 Bad Request`: se ha introducido un valor de impago no válido.
- `500 Internal Server Error`: se ha producido un error al consultar la API externa.

## 6. Consideraciones

La aplicación necesita una variable de entorno `DATABASE_URL` válida para conectarse a MySQL.

Algunos endpoints están implementados como estructura inicial y necesitan incorporar las consultas o los cálculos correspondientes para ofrecer toda la funcionalidad prevista.

