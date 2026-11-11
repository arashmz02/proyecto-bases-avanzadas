
from flask import Flask, render_template, request

from app.services.promociones_service import cargar_promociones
from app.services.consultas_service import consultar_cupones_por_departamento


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def inicio():
        return render_template("index.html")

    @app.route("/cargar-promociones", methods=["POST"])
    def cargar_catalogo():
        archivo = request.files.get("archivo")

        if archivo is None or archivo.filename == "":
            return render_template(
                "index.html",
                mensaje="Debes seleccionar un archivo JSON.",
                tipo="danger"
            )

        if not archivo.filename.lower().endswith(".json"):
            return render_template(
                "index.html",
                mensaje="El archivo seleccionado debe tener formato JSON.",
                tipo="danger"
            )

        try:
            resultado = cargar_promociones(archivo)

            mensaje = (
                f"Proceso completado. "
                f"Promociones insertadas: {resultado['insertadas']}. "
                f"Ya existentes: {resultado['existentes']}."
            )

            return render_template(
                "index.html",
                mensaje=mensaje,
                tipo="success"
            )

        except Exception as error:
            return render_template(
                "index.html",
                mensaje=f"No se pudo cargar el archivo: {error}",
                tipo="danger"
            )

    @app.route("/consultar-departamentos", methods=["POST"])
    def consultar_departamentos():
        try:
            resultados = consultar_cupones_por_departamento()

            return render_template(
                "index.html",
                resultados=resultados
            )

        except Exception as error:
            return render_template(
                "index.html",
                mensaje=f"No se pudo realizar la consulta: {error}",
                tipo="danger"
            )

    return app
