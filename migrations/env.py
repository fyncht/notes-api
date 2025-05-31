# migrations/env.py
from __future__ import with_statement
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Этот код генерировался Flask-Migrate, но мы подправляем 'online' часть

# Пасём конфиг Alembic из alembic.ini
config = context.config
fileConfig(config.config_file_name)

# Чтобы импортировать наше Flask-приложение и метаданные модели
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "app")))
from app import create_app, db
from app.models import Note  # чтобы Alembic знал о модели Note

# Создаём Flask-приложение и берём metadata
flask_app = create_app()
with flask_app.app_context():
    target_metadata = db.metadata


def run_migrations_offline():
    """Запуск миграций в 'offline' режиме: просто генерируем SQL скрипты"""
    # Берём URL из переменной окружения, или из Config.SQLALCHEMY_DATABASE_URI
    url = flask_app.config.get("SQLALCHEMY_DATABASE_URI")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в 'online' режиме: напрямую подключаемся к БД через SQLAlchemy Engine."""
    # Берём URL из Flask-конфига
    url = flask_app.config.get("SQLALCHEMY_DATABASE_URI")

    # Создаём SQLAlchemy Engine напрямую, минуя engine_from_config
    connectable = create_engine(
        url,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # чтобы Alembic отслеживал изменения типов колонок
        )

        with context.begin_transaction():
            context.run_migrations()


# Выбираем режим (offline/online) автоматически
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
