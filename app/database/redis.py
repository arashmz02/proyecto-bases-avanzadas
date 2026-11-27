import redis

from config import Config

cliente_redis = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True
)


def verificar_conexion_redis():
    try:
        return cliente_redis.ping()
    except redis.RedisError as error:
        print(f"Error al conectar con Redis: {error}")
        return False
