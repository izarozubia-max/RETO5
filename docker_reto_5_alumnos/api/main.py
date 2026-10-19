import os

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

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

@app.get("/estado")
def comprobar_conexion():
    with engine.connect() as conexion:
        conexion.execute(text("SELECT 1"))

    return {"mensaje": "Conexión con MySQL correcta"}, 200