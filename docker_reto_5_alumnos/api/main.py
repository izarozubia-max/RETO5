import os
import urllib.request
import json
from flask import Flask
from sqlalchemy import create_engine, text

app = Flask(__name__)

engine = create_engine(
    os.environ["DATABASE_URL"],
    pool_pre_ping=True
)


@app.get("/")
def root():
    return {
        "mensaje": "API Flask funcionando"
    }

@app.get("/prestamos")
def obtener_prestamos():
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("""
                SELECT *
                FROM clientes_credito
                ORDER BY row_id
                LIMIT 10
            """)
        )

        prestamos = [
            dict(fila)
            for fila in resultado.mappings()
        ]

    return {"prestamos": prestamos}, 200



@app.get("/estado")
def comprobar_conexion():
    with engine.connect() as conexion:
        conexion.execute(text("SELECT 1"))

    return {"mensaje": "Conexión con MySQL correcta"}, 200

@app.get("/clientes")
def obtener_clientes():
    return {
        "mensaje": "Consulta de todos los clientes"
}

@app.get("/clientes/<string:id_cliente>")
def obtener_cliente(id_cliente):
    return {
        "mensaje": "Consulta de un cliente",
        "id": id_cliente
    }

@app.get("/clientes/impago/<int:impago>")
def filtrar_impago(impago):
    if impago not in [0, 1]:
        return {"error": "El impago debe ser 0 o 1"}, 400

    return {
        "mensaje": "Filtrar clientes por impago",
        "impago": impago
    }

@app.get("/estadisticas")
def obtener_estadisticas():
    return {
        "mensaje": "Estadísticas generales de los créditos"
    }

@app.get("/clientes/<string:id_cliente>/analisis")
def analizar_cliente(id_cliente):
    return {
        "mensaje": "Análisis del cliente",
        "id": id_cliente
    }

# Consultar una API externa
@app.get("/monedas")
def consultar_monedas():
    url = "https://open.er-api.com/v6/latest/EUR"

    try:
        respuesta = urllib.request.urlopen(url)
        datos = json.loads(respuesta.read())

        return {
            "mensaje": "Datos obtenidos de una API externa",
            "moneda_base": datos["base_code"],
            "tipos_cambio": datos["rates"]
        }

    except Exception:
        return {"error": "No se pudo consultar la API externa"}, 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )