
import json
from pathlib import Path

from app.database.mongodb import db


def cargar_promociones(archivo=None):
    """
    Carga las promociones desde el archivo JSON
    hacia la colección promociones de MongoDB.
    """

    ruta_archivo = Path(__file__).resolve().parents[2] / "data" / "promociones.json"

    # Leer el archivo JSON
    if archivo is not None:
        promociones = json.load(archivo)
    else:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo_local:
            promociones = json.load(archivo_local)
            
    # Validar que el contenido sea una lista
    if not isinstance(promociones, list):
        raise ValueError("El archivo JSON debe contener una lista de promociones.")

    if not promociones:
        raise ValueError("El archivo JSON no contiene promociones.")

    # Obtener la colección de MongoDB
    coleccion = db["promociones"]

    # Insertar las promociones que todavía no existen
    insertadas = 0
    existentes = 0

    for promocion in promociones:
        if "id" not in promocion:
            raise ValueError("Una promoción no contiene el identificador id.")

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
