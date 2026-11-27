from app.database.mongodb import db
from app.database.redis import cliente_redis


PREFIJO_CLAVE = "promocion_activa:"

SCRIPT_ACTIVAR = """
if redis.call('EXISTS', KEYS[1]) == 1 then
    return 0
end

redis.call(
    'HSET',
    KEYS[1],
    'promocion_id', ARGV[1],
    'promocion_nombre', ARGV[2],
    'departamento', ARGV[3],
    'cupones_disponibles', ARGV[4]
)

redis.call('EXPIRE', KEYS[1], ARGV[5])

return 1
"""


def obtener_catalogo_promociones():
    return list(
        db["promociones"].find(
            {},
            {"_id": 1, "nombre": 1, "departamento": 1}
        ).sort("_id", 1)
    )


def activar_promocion(promocion_id, cupones, duracion_minutos):
    if not isinstance(cupones, int) or isinstance(cupones, bool) or cupones <= 0:
        raise ValueError("La cantidad de cupones debe ser mayor que cero.")

    if not isinstance(duracion_minutos, int) or isinstance(duracion_minutos, bool) or duracion_minutos <= 0:
        raise ValueError("La duración debe ser mayor que cero.")

    promocion = db["promociones"].find_one({"_id": promocion_id})

    if not promocion:
        raise ValueError("La promoción seleccionada no existe en el catálogo.")

    clave = f"{PREFIJO_CLAVE}{promocion_id}"

    resultado = cliente_redis.eval(
        SCRIPT_ACTIVAR,
        1,
        clave,
        promocion_id,
        promocion["nombre"],
        promocion["departamento"],
        cupones,
        duracion_minutos * 60
    )

    if resultado == 0:
        raise ValueError("Esta promoción ya se encuentra activa.")

    return {
        "promocion_id": promocion_id,
        "promocion_nombre": promocion["nombre"],
        "departamento": promocion["departamento"],
        "cupones_disponibles": cupones,
        "duracion_minutos": duracion_minutos
    }


def obtener_promociones_activas():
    promociones = []

    for clave in cliente_redis.scan_iter(match=f"{PREFIJO_CLAVE}*"):
        datos = cliente_redis.hgetall(clave)
        tiempo_restante = cliente_redis.ttl(clave)

        if not datos or tiempo_restante <= 0:
            continue

        datos["cupones_disponibles"] = int(
            datos["cupones_disponibles"]
        )
        datos["tiempo_restante"] = tiempo_restante

        promociones.append(datos)

    return sorted(
        promociones,
        key=lambda promocion: promocion["promocion_id"]
    )
