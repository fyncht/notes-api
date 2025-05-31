import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Загружаем конфигурацию из файла config.py
    app.config.from_object("app.config.Config")

    # Инициализируем расширения
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрируем blueprints/маршруты
    from app.routes import notes_bp
    app.register_blueprint(notes_bp)

    return app
