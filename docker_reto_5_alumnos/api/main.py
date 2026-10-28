import os
import urllib.request
import json
from flask import Flask
from sqlalchemy import create_engine, text
import requests

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

@app.get("/prestamos/<string:id_prestamo>")
def obtener_prestamo(id_prestamo: str):
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("""
                SELECT *
                FROM clientes_credito
                WHERE id = :id_prestamo
            """),
            {"id_prestamo": id_prestamo}
        )

        prestamo = resultado.mappings().first()

    if prestamo is None:
        return {"error": "Préstamo no encontrado"}, 404

    return {"prestamo": dict(prestamo)}, 200



@app.get("/estado")
def comprobar_conexion():
    with engine.connect() as conexion:
        conexion.execute(text("SELECT 1"))

    return {"mensaje": "Conexión con MySQL correcta"}, 200

@app.get("/clientes/<string:id_cliente>")
def obtener_cliente(id_cliente: str):
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("""
                SELECT *
                FROM clientes_credito
                WHERE id = :id_cliente
            """),
            {"id_cliente": id_cliente}
        )

        cliente = resultado.mappings().first()

    if cliente is None:
        return {"error": "Cliente no encontrado"}, 404

    return {"cliente": dict(cliente)}, 200

@app.get("/prestamos/impago/<int:impago>")
def filtrar_impago(impago: int):
    if impago not in [0, 1]:
        return {"error": "El impago debe ser 0 o 1"}, 400

    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("""
                SELECT *
                FROM clientes_credito
                WHERE impago = :impago
                ORDER BY row_id
            """),
            {"impago": str(impago)}
        )

        clientes = [
            dict(fila)
            for fila in resultado.mappings()
        ]

    return {"clientes": clientes}, 200

@app.get("/estadisticas")
def obtener_estadisticas():
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("""
                SELECT
                    COUNT(*) AS total_prestamos,
                    AVG(CAST(edad AS DECIMAL(10, 2))) AS edad_media,
                    AVG(CAST(ingresos AS DECIMAL(15, 2))) AS ingresos_medios,
                    AVG(CAST(monto_inicial AS DECIMAL(15, 2))) AS monto_medio,
                    SUM(
                        CASE WHEN impago = '1' THEN 1 ELSE 0 END
                    ) AS total_impagos
                FROM clientes_credito
            """)
        )

        fila = resultado.mappings().one()

    estadisticas = {
        "total_prestamos": int(fila["total_prestamos"]),
        "edad_media": (
            float(fila["edad_media"])
            if fila["edad_media"] is not None else None
        ),
        "ingresos_medios": (
            float(fila["ingresos_medios"])
            if fila["ingresos_medios"] is not None else None
        ),
        "monto_medio": (
            float(fila["monto_medio"])
            if fila["monto_medio"] is not None else None
        ),
        "total_impagos": int(fila["total_impagos"] or 0)
    }

    return {"estadisticas": estadisticas}, 200

# Consultar una API externa

@app.get("/monedas")
def consultar_monedas():
    url = "https://open.er-api.com/v6/latest/EUR"

    try:
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()

        datos = respuesta.json()

        if "base_code" not in datos or "rates" not in datos:
            return {"error": "La respuesta no contiene los datos necesarios"}, 502

        return {
            "moneda_base": datos["base_code"],
            "tipos_cambio": datos["rates"]
        }, 200

    except requests.RequestException:
        return {"error": "No se pudo consultar la API externa"}, 503

    except ValueError:
        return {"error": "La respuesta no es un JSON válido"}, 502