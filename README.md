
# Notes REST API

## Запуск
```bash
git clone git@github.com:fyncht/notes-api.git && cd notes-api
docker compose up --build
```

## Эндпоинты:
```bash
 POST /notes → создаёт заметку, возвращает { "id": <new_id> } и статус 201.

 GET /notes → возвращает массив всех заметок: [{"id":1,"title":"…","content":"…"}, …].

 GET /notes/<id> → возвращает объект заметки или 404, если её нет.

 DELETE /notes/<id> → удаляет заметку, возвращает 204 или 404, если заметки нет.
```
## Технологии:

 #### Flask + Flask-SQLAlchemy + Flask-Migrate.

#### База данных: MySQL (в Docker) или SQLite (для локального теста).

#### Полностью контейнеризовано с помощью Docker + docker-compose.

# Тестовые запросы к REST API «Заметки»

Ниже приведены примеры запросов (curl) для всех эндпоинтов API. 

- **Локально (Flask Dev Server / SQLite)** — на порту **5001**  
  ```bash
  source venv/bin/activate
  export DATABASE_URL="sqlite:///app.db"
  python -m flask db upgrade
  python -m flask run --host=0.0.0.0 --port=5001
  ```
  ### 2.1 Создание новой заметки  
**Endpoint:** `POST /notes`  
**URL:** `{{BASE_URL}}/notes`  
**Метод:** `POST`  
**Заголовки:**  
```
Content-Type: application/json
```
**Тело запроса (пример):**
```json
{
  "title": "Первая заметка",
  "content": "Это содержимое первой заметки."
}
```
**Ожидаемый ответ:**
- **Статус:** `201 Created`
- **Тело (JSON):**
  ```json
  {
    "id": 1
  }
  ```

#### Пример `curl`-запроса
```bash
curl -X POST {{BASE_URL}}/notes \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Первая заметка",
           "content": "Это содержимое первой заметки."
         }'
```

---

### 2.2 Получение списка всех заметок  
**Endpoint:** `GET /notes`  
**URL:** `{{BASE_URL}}/notes`  
**Метод:** `GET`  
**Ожидаемый ответ:**
- **Статус:** `200 OK`
- **Тело (JSON):**
```
[
  {
    "id": 1,
    "title": "Первая заметка",
    "content": "Это содержимое первой заметки."
  },
  {
    "id": 2,
    "title": "Вторая заметка",
    "content": "Текст второй заметки."
  }
]
```

#### Пример `curl`-запроса
```bash
curl {{BASE_URL}}/notes
```

---


## 2. Эндпоинты и примеры запросов

> Замените `{{BASE_URL}}` на:
> - `http://localhost:5001`, если вы запустили локально на 5001 или через Docker с `"5001:5000"`. 

---
### 2.3 Получение заметки по ID  
**Endpoint:** `GET /notes/<id>`  
**URL:** `{{BASE_URL}}/notes/1` (замените `1` на нужный ID)  
**Метод:** `GET`  
**Ожидаемый ответ (если заметка существует):**
```
{
  "id": 1,
  "title": "Первая заметка",
  "content": "Это содержимое первой заметки."
}
```
**Если заметка с указанным ID отсутствует:**
- **Статус:** `404 Not Found`

#### Пример `curl`-запроса
```bash
curl {{BASE_URL}}/notes/1
```

---

### 2.4 Удаление заметки по ID  
**Endpoint:** `DELETE /notes/<id>`  
**URL:** `{{BASE_URL}}/notes/1` (замените `1` на нужный ID)  
**Метод:** `DELETE`  
**Ожидаемый ответ (если заметка удалена):**
- **Статус:** `204 No Content`
- Тело ответа отсутствует.  
**Если заметка с указанным ID не найдена:**
- **Статус:** `404 Not Found`

#### Пример `curl`-запроса
```bash
curl -X DELETE {{BASE_URL}}/notes/1
```

---

## 3. Полный сценарий использования

1. **Создаём заметку**  
```bash
curl -X POST {{BASE_URL}}/notes \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Тестовая заметка",
           "content": "Проверка API"
         }'
```
**Ожидаемый ответ:**
```
{
  "id": 1
}
```

2. **Получаем список всех заметок**  
```bash
curl {{BASE_URL}}/notes
```
**Ожидаемый ответ:**
```
[
  {
    "id": 1,
    "title": "Тестовая заметка",
    "content": "Проверка API"
  }
]
```

3. **Получаем заметку по ID = 1**  
```bash
curl {{BASE_URL}}/notes/1
```
**Ожидаемый ответ:**
```
{
  "id": 1,
  "title": "Тестовая заметка",
  "content": "Проверка API"
}
```

4. **Удаляем заметку по ID = 1**  
```bash
curl -X DELETE {{BASE_URL}}/notes/1
```
**Ожидаемый ответ:** статус **204 No Content** (тело отсутствует).

5. **Проверяем, что список пуст**  
```bash
curl {{BASE_URL}}/notes
```
**Ожидаемый ответ:**
```
[]
```

---

## 4. Обработка ошибок

### 4.1 Ошибка при создании заметки без обязательных полей  
- **Запрос:**
  ```bash
  curl -X POST {{BASE_URL}}/notes \
       -H "Content-Type: application/json" \
       -d '{}'
  ```
- **Ответ:**
  - **Статус:** `400 Bad Request`
  - **Тело (JSON):**  
    ```json
    {
      "message": "Both 'title' and 'content' are required"
    }
    ```

### 4.2 Получение или удаление несуществующей заметки  
- **Запрос:**
  ```bash
  curl {{BASE_URL}}/notes/999
  ```
- **Ответ:**
  - **Статус:** `404 Not Found`
  - Тело ответа отсутствует (или содержит короткое сообщение об ошибке).
