from flask import Flask




def create_app():
    app = Flask(__name__, template_folder="../template", static_url_path="/", static_folder="../resource")
    init_blueprint(app)
    return app

def init_blueprint(app):
    from controller.user import user
    app.register_blueprint(user)