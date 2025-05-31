import os
from flask_migrate import Migrate
from app import create_app, db
from app.models import Note  # Чтобы Alembic видел модели

# Устанавливаем переменную окружения для Flask
os.environ.setdefault("FLASK_APP", "manage.py")
os.environ.setdefault("FLASK_ENV", "development")

app = create_app()

# Объект Migrate, но он уже инициализирован внутри create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Если хотим делать что-то вручную, но обычно запускаем через flask cli
    app.run(host="0.0.0.0", port=5000)
