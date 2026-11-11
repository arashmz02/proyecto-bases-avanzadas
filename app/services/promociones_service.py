
import json
from pathlib import Path

from app.database.mongodb import db


def cargar_promociones(archivo=None):
    """
    Carga las promociones desde un archivo JSON
    hacia la colección promociones de MongoDB.
    """

    ruta_archivo = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "promociones.json"
    )

    # Leer el archivo JSON
    if archivo is not None:
        promociones = json.load(archivo)
    else:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_local:
            promociones = json.load(archivo_local)

    # Validar que el contenido sea una lista
    if not isinstance(promociones, list):
        raise ValueError(
            "El archivo JSON debe contener una lista de promociones."
        )

    if not promociones:
        raise ValueError("El archivo JSON no contiene promociones.")

    # Validar todas las promociones antes de insertarlas
    identificadores = set()

    for promocion in promociones:

        if not isinstance(promocion, dict):
            raise ValueError(
                "Cada elemento del JSON debe ser un objeto de promoción."
            )

        identificador = promocion.get("id")

        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError(
                "Una promoción contiene un identificador inválido."
            )

        if identificador in identificadores:
            raise ValueError(
                f"El identificador {identificador} está duplicado en el JSON."
            )

        identificadores.add(identificador)

    # Obtener la colección de MongoDB
    coleccion = db["promociones"]

    insertadas = 0
    existentes = 0

    # Insertar las promociones que todavía no existen
    for promocion in promociones:

        promocion_mongo = promocion.copy()
        promocion_mongo["_id"] = promocion_mongo.pop("id")

        resultado = coleccion.update_one(
            {"_id": promocion_mongo["_id"]},
            {"$setOnInsert": promocion_mongo},
            upsert=True
        )

        if resultado.upserted_id is not None:
            insertadas += 1
        else:
            existentes += 1

    return {
        "total": len(promociones),
        "insertadas": insertadas,
        "existentes": existentes
    }
