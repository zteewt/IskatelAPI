# IskatelAPI

Backend-приложение на Django для работы с географическими точками на карте.

# Стек
- Python 3.12
- Django + Django REST Framework
- PostgreSQL
- GeoDjango 
- PostGIS
- pytest

# Возможности
- CRUD для Points
- Сообщения к точкам (api/points, api/messages)
- Поиск по радиусу (Points search / Messages search)
- Аутентификация и права доступа

# Быстрый старт (локально)

## 1) Клонирование и venv
```bash
git clone https://github.com/zteewt/IskatelAPI.git
cd /IskatelAPI
python -m venv .venv
source .venv/bin/activate
pip install -r /iskatelapi/requirements.txt
```

## 2) Основные эндпоинты
#### Авторизация
 - POST (/api/auth/register/) - Регистрация
 - POST (/api/auth/login/) - Вход
 - POST (/api/auth/logout/) - Выход 

 #### Получение и создание точек
 - GET, POST (/api/points/) - создание точек, либо получение списка всех точек

 #### Получение и создание сообщений к точкам
  - GET, POST (/api/points/messages/) - создание сообщений к точке (точка передается в json), либо получение списка всех сообщений
   - GET (/api/points/{point_id}/messages/) - получения списка сообщений конкретной точки

#### Поиск точек в определенной области
 - GET (/api/points/search/?latitude=&longitude=&radius=) - поиск точек в заданной области, параметры: latitude, longitude, radius (км)
 
 #### Поиск сообщений в определенной области
  - GET (/api/points/messages/search/?latitude=&longitude=&radius=) - поиск сообщений в заданной области, параметры: latitude, longitude, radius (км)


# Примеры запросов (curl)
## Переменные (удобно)

```bash
export BASE_URL="http://127.0.0.1:8000"
```
## Регистрация

```bash
curl -X POST "$BASE_URL/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "pass123"
  }'
```
## Логин (сохранить cookies)

```bash
curl -X POST "$BASE_URL/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user1",
    "password": "pass123"
  }' \
  -c cookies.txt
```
## Логаут (по cookies)

```bash
curl -X POST "$BASE_URL/api/auth/logout/" \
  -b cookies.txt
```

## Получить список точек

```bash
curl "$BASE_URL/api/points/" \
  -b cookies.txt
```

## Создать точку

```bash
curl -X POST "$BASE_URL/api/points/" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "Test Point",
    "location": { "type": "Point", "coordinates": [42.7352, 43.6130] }
  }'
```

## Получить список всех сообщений (global)

```bash
curl "$BASE_URL/api/points/messages/" \
  -b cookies.txt
```
## Создать сообщение к точке

```bash
curl -X POST "$BASE_URL/api/points/messages/" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "message": "Hello world!",
    "point": 1
  }'
```

## Поиск точек по радиусу (radius в км)

```bash
curl "$BASE_URL/api/points/search/?latitude=43.613&longitude=42.735&radius=2" \
  -b cookies.txt
```
## Поиск сообщений по радиусу (radius в км)

```bash
curl "$BASE_URL/api/points/messages/search/?latitude=43.613&longitude=42.735&radius=2" \
  -b cookies.txt
```


## Тесты (все)
```bash
pytest -v
```
При возможности, можно запустить разные тесты, они разложены по файлам и папкам /test_...
