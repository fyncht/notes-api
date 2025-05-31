
# Notes REST API

## Запуск
```bash
git clone git@github.com:fyncht/notes-api.git && cd notes-api
docker compose up --build
```

## Эндпоинты:

#### POST /notes → создаёт заметку, возвращает { "id": <new_id> } и статус 201.

#### GET /notes → возвращает массив всех заметок: [{"id":1,"title":"…","content":"…"}, …].

#### GET /notes/<id> → возвращает объект заметки или 404, если её нет.

#### DELETE /notes/<id> → удаляет заметку, возвращает 204 или 404, если заметки нет.

## Технологии:

 #### Flask + Flask-SQLAlchemy + Flask-Migrate.

#### База данных: MySQL (в Docker) или SQLite (для локального теста).

#### Полностью контейнеризовано с помощью Docker + docker-compose.

