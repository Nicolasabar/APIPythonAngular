from flask import Flask

from .routes import indexRoutes

app = Flask(__name__)

def init_app(config):
    app.config.from_object(config)


    app.register_blueprint(indexRoutes.main, url_prefix='/')

    return app