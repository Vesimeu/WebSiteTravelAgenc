# Travel Agency Website

Веб-приложение для туристического агентства, разработанное на Flask. Позволяет пользователям просматривать туры, бронировать путевки, оставлять отзывы и управлять своим профилем.

## Функциональность

- Регистрация и авторизация пользователей
- Просмотр доступных туров
- Бронирование путевок
- Управление профилем пользователя
- Система отзывов для туров
- Административная панель для управления турами и пользователями

## Требования

- Python 3.8+
- PostgreSQL 12+
- pip (менеджер пакетов Python)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd TravelAgencyWebsite
```

2. Создайте и активируйте виртуальное окружение:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. В файле .env укажите данные для подключения к бд, вот пример:
```python
DB_SERVER=localhost
DB_USER=postgres
DB_NAME=travel
DB_PASSWORD=123123
SECRET_KEY=abcde
```

## Настройка базы данных

1. Создайте базу данных PostgreSQL:
```sql
CREATE DATABASE travel_agency;
```

2. Выполните SQL-скрипты для создания таблиц:
```bash
# Подключитесь к базе данных
psql -U ваш-пользователь -d travel_agency

# Выполните скрипты из директории app/sql
\i app/sql/create_tables.sql
\i app/sql/insert_initial_data.sql
```

## Запуск приложения

1. Убедитесь, что виртуальное окружение активировано:
```bash
# Windows
.venv\Scripts\activate

# Linux/MacOS
source .venv/bin/activate
```

2. Запустите приложение:
```bash
flask run
```

Приложение будет доступно по адресу: http://localhost:5000

## Структура проекта

```
TravelAgencyWebsite/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── dbInterface.py
│   ├── sql/
│   │   ├── create_tables.sql
│   │   └── insert_initial_data.sql
│   ├── static/
│   │   ├── css/
│   │   └── img/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── ...
├── config.py
├── requirements.txt
└── README.md
```

## ERD диаграмма базы данных
![image](https://github.com/user-attachments/assets/2dbbf834-bb8b-4e33-a991-93bbc5de8194)

## Роли пользователей

1. Администратор (role = 1):
   - Управление турами
   - Управление пользователями
   - Добавление/удаление пунктов назначения
   - Модерация отзывов

2. Обычный пользователь (role = 2):
   - Просмотр туров
   - Бронирование путевок
   - Управление профилем
   - Оставление отзывов

## Возможные проблемы и их решение

1. Ошибка подключения к базе данных:
   - Проверьте правильность данных в config.py
   - Убедитесь, что PostgreSQL запущен
   - Проверьте права доступа пользователя базы данных

2. Ошибка при выполнении SQL-скриптов:
   - Убедитесь, что скрипты выполняются в правильном порядке
   - Проверьте синтаксис SQL-запросов
   - Проверьте права доступа к базе данных

3. Проблемы с зависимостями:
   - Удалите и пересоздайте виртуальное окружение
   - Обновите pip: `python -m pip install --upgrade pip`
   - Переустановите зависимости: `pip install -r requirements.txt`
