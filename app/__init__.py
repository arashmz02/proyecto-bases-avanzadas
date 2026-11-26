from flask import Flask, render_template, request

from app.services.promociones_service import cargar_promociones
from app.services.consultas_service import consultar_cupones_por_departamento
from app.services.promociones_activas_service import (
    obtener_catalogo_promociones,
    activar_promocion as activar_promocion_servicio,
    obtener_promociones_activas
)


def create_app():
    app = Flask(__name__)

    def renderizar_inicio(
        mensaje=None,
        tipo="info",
        resultados=None,
        mostrar_resultados=False
    ):
        try:
            catalogo = obtener_catalogo_promociones()
        except Exception:
            catalogo = []

        try:
            promociones_activas = obtener_promociones_activas()
        except Exception:
            promociones_activas = []

        return render_template(
            "index.html",
            mensaje=mensaje,
            tipo=tipo,
            catalogo_promociones=catalogo,
            promociones_activas=promociones_activas,
            resultados=resultados,
            mostrar_resultados=mostrar_resultados
        )

    @app.route("/")
    def inicio():
        return renderizar_inicio()

    @app.route("/cargar-promociones", methods=["POST"])
    def cargar_catalogo():
        archivo = request.files.get("archivo")

        if archivo is None or archivo.filename == "":
            return renderizar_inicio(
                "Debes seleccionar un archivo JSON.",
                "danger"
            )

        if not archivo.filename.lower().endswith(".json"):
            return renderizar_inicio(
                "El archivo seleccionado debe tener formato JSON.",
                "danger"
            )

        try:
            resultado = cargar_promociones(archivo)

            mensaje = (
                f"Proceso completado. "
                f"Promociones insertadas: {resultado['insertadas']}. "
                f"Ya existentes: {resultado['existentes']}."
            )

            return renderizar_inicio(mensaje, "success")

        except Exception as error:
            return renderizar_inicio(
                f"No se pudo cargar el archivo: {error}",
                "danger"
            )

    @app.route("/consultar-departamentos", methods=["POST"])
    def consultar_departamentos():
        try:
            resultados = consultar_cupones_por_departamento()

            return renderizar_inicio(
                resultados=resultados,
                mostrar_resultados=True
            )

        except Exception as error:
            return renderizar_inicio(
                f"No se pudo realizar la consulta: {error}",
                "danger"
            )

    @app.route("/activar-promocion", methods=["POST"])
    def activar_promocion():
        promocion_id = request.form.get("promocion_id", "").strip()
        cupones_texto = request.form.get("cupones", "").strip()
        duracion_texto = request.form.get("duracion", "").strip()

        try:
            cupones = int(cupones_texto)
            duracion = int(duracion_texto)

            resultado = activar_promocion_servicio(
                promocion_id,
                cupones,
                duracion
            )

            mensaje = (
                f"Promoción {resultado['promocion_id']} activada "
                f"correctamente con {resultado['cupones_disponibles']} "
                f"cupones durante {resultado['duracion_minutos']} minutos."
            )

            return renderizar_inicio(mensaje, "success")

        except ValueError as error:
            return renderizar_inicio(str(error), "danger")

        except Exception as error:
            return renderizar_inicio(
                f"No se pudo activar la promoción: {error}",
                "danger"
            )

    return app
