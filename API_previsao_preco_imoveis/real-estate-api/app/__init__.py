from flask import Flask
from app.routes import main
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    SWAGGER_URL = '/docs'  # URL para acessar a documentação
    API_URL = '/swagger.yaml'  # Localização do arquivo swagger.yaml

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "API Previsão Aluguel"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Servir o arquivo swagger.yaml estaticamente
    @app.route("/swagger.yaml")
    def swagger_yaml():
        return app.send_static_file("swagger.yaml")

    return app
