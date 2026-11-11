
from pymongo import MongoClient
from config import Config

# Crear conexión con MongoDB
cliente = MongoClient(
    Config.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

# Seleccionar la base de datos del proyecto
db = cliente[Config.MONGO_DB]


def verificar_conexion():
    """
    Comprueba que la conexión con MongoDB
    esté funcionando correctamente.
    """
    try:
        cliente.admin.command("ping")
        return True
    except Exception as error:
        print(f"Error al conectar con MongoDB: {error}")
        return False
