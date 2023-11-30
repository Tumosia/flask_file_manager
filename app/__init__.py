from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import secrets


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    Bootstrap5(app)
    CSRFProtect(app)


    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.files import bp as files_bp
    app.register_blueprint(files_bp, url_prefix='/files')

    from app.folders import bp as folders_bp
    app.register_blueprint(folders_bp, url_prefix='/folders')

   
    return app