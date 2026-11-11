
from app.database.mongodb import db
from app.services.consultas_service import consultar_cupones_por_departamento


def preparar_datos():
    coleccion = db["cupones"]

    # Limpiar únicamente los datos de prueba anteriores
    coleccion.delete_many({
        "_id": {
            "$in": [
                "CUP-TEST-001",
                "CUP-TEST-002",
                "CUP-TEST-003",
                "CUP-TEST-004",
                "CUP-TEST-005"
            ]
        }
    })

    cupones_prueba = [
        {
            "_id": "CUP-TEST-001",
            "cliente_nombre": "Carlos",
            "cliente_nombre_normalizado": "carlos",
            "promocion_id": "P001",
            "departamento": "Ropa"
        },
        {
            "_id": "CUP-TEST-002",
            "cliente_nombre": "Carlos",
            "cliente_nombre_normalizado": "carlos",
            "promocion_id": "P002",
            "departamento": "Ropa"
        },
        {
            "_id": "CUP-TEST-003",
            "cliente_nombre": "María",
            "cliente_nombre_normalizado": "maría",
            "promocion_id": "P001",
            "departamento": "Ropa"
        },
        {
            "_id": "CUP-TEST-004",
            "cliente_nombre": "Carlos",
            "cliente_nombre_normalizado": "carlos",
            "promocion_id": "P003",
            "departamento": "Electrónica"
        },
        {
            "_id": "CUP-TEST-005",
            "cliente_nombre": "Pedro",
            "cliente_nombre_normalizado": "pedro",
            "promocion_id": "P004",
            "departamento": "Electrónica"
        }
    ]

    coleccion.insert_many(cupones_prueba)

    print("Datos de prueba insertados correctamente.")


if __name__ == "__main__":
    preparar_datos()

    resultados = consultar_cupones_por_departamento()

    print("\nResultados de la consulta:")
    for resultado in resultados:
        print(resultado)
