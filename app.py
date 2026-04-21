from flask import Flask
from extensions import db, migrate, login_manager
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para continuar.'

    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.admin import admin_bp
    from routes.services import services_bp
    from routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(main_bp)

    return app

app = create_app()  # ← expõe o objeto para o gunicorn

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
