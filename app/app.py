from flask import Flask
import os 



def create_app():
    app = Flask(__name__, template_folder="../template", static_url_path="/", static_folder="../resource")
    init_blueprint(app)
    app.config['SECRET_KEY'] = os.urandom(24)
    return app

def init_blueprint(app):
    from controller.user import user
    app.register_blueprint(user)

    from controller.index import index
    app.register_blueprint(index)