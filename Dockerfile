# 1. Базовый образ: python:3.10-slim
FROM python:3.10-slim

# 2. Обновляем списки пакетов и устанавливаем нужные системные зависимости
#    (openssl, libffi, python3-dev и компиляторы) для корректной установки cryptography
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Назначаем рабочую директорию в контейнере
WORKDIR /app

# 4. Копируем файл зависимостей
COPY requirements.txt .

# 5. Устанавливаем Python-пакеты (в том числе cryptography)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем всё содержимое проекта внутрь /app
COPY . .

# 7. Экспортируем переменные окружения для Flask
ENV FLASK_APP=manage.py
ENV FLASK_ENV=production

# 8. Команда-обёртка:
#    - Сначала ждем, пока MySQL слушает (повторяем попытку, пока не получится подключиться)
#    - Затем запускаем миграции (flask db upgrade)
#    - После успешных миграций запускаем gunicorn
#
# В переменной DATABASE_URL будет то, что вы передадите из docker-compose.yml
CMD ["sh", "-c", "\
      echo 'Waiting for MySQL to be available...' && \
      until python - <<EOF\n\
import os\n\
from sqlalchemy import create_engine\n\
# берём строку из переменной окружения, переданной через docker-compose\n\
db_url = os.getenv('DATABASE_URL')\n\
engine = create_engine(db_url)\n\
try:\n\
    conn = engine.connect()\n\
    conn.close()\n\
    print('MySQL is up!')\n\
except Exception as e:\n\
    print('Still waiting for MySQL: ' + str(e))\n\
    exit(1)\n\
EOF\n\
        do sleep 2; done && \
      echo 'Running migrations...' && \
      flask db upgrade && \
      echo 'Starting Gunicorn...' && \
      exec gunicorn -b 0.0.0.0:5000 manage:app \
    "]
