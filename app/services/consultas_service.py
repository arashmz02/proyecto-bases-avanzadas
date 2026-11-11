
from app.database.mongodb import db


def consultar_cupones_por_departamento():
    """
    Consulta los cupones obtenidos agrupados por departamento.
    Calcula el total de cupones y la cantidad de clientes distintos.
    """

    coleccion = db["cupones"]

    pipeline = [
        {
            "$group": {
                "_id": "$departamento",
                "total_cupones": {"$sum": 1},
                "clientes": {"$addToSet": "$cliente_nombre_normalizado"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "departamento": "$_id",
                "total_cupones": 1,
                "clientes_distintos": {"$size": "$clientes"}
            }
        },
        {
            "$sort": {
                "departamento": 1
            }
        }
    ]

    resultados = list(coleccion.aggregate(pipeline))

    return resultados
