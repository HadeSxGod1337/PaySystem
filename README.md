# Payment System API

Асинхронное REST API приложение для системы платежей, реализованное на FastAPI с использованием PostgreSQL и SQLAlchemy.

## Технологический стек

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - база данных
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - миграции БД
- **Docker Compose** - для развертывания
- **JWT** - аутентификация
- **bcrypt** - хеширование паролей
- **Ruff** - линтер и форматтер кода
- **MyPy** - проверка типов
- **Pre-commit** - автоматические проверки перед коммитом

## Структура проекта

```
PaymentSystem/
├── app/
│   ├── api/           # API роуты
│   │   └── v1/
│   ├── core/          # Основные компоненты (security, dependencies)
│   ├── models/        # Модели SQLAlchemy
│   ├── repositories/  # Репозитории (Repository pattern)
│   ├── schemas/       # Pydantic схемы
│   ├── services/      # Бизнес-логика (Service pattern)
│   ├── config.py      # Конфигурация
│   ├── database.py    # Настройка БД
│   └── main.py        # Точка входа
├── alembic/           # Миграции БД
├── docker-compose.yml # Docker Compose конфигурация
├── Dockerfile         # Docker образ приложения
└── requirements.txt   # Зависимости Python
```

## Установка и запуск

### Вариант 1: Запуск с использованием Docker Compose

1. **Клонируйте репозиторий и перейдите в директорию проекта:**
   ```bash
   cd PaymentSystem
   ```

2. **Создайте файл `.env` на основе `.env.example`:**
   ```bash
   cp .env.example .env
   ```

3. **Запустите приложение с помощью Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Выполните миграции БД:**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

5. **Приложение будет доступно по адресу:**
   - API: http://localhost:8000
   - Документация API: http://localhost:8000/docs
   - Альтернативная документация: http://localhost:8000/redoc

### Вариант 2: Запуск без Docker Compose

1. **Установите PostgreSQL** и создайте базу данных:
   ```sql
   CREATE DATABASE payment_system;
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   ```

3. **Активируйте виртуальное окружение:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Создайте файл `.env` и настройте переменные окружения:**
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/payment_system
   SECRET_KEY=your-secret-key-change-in-production
   WEBHOOK_SECRET_KEY=gfdmhghif38yrf9ew0jkf32
   JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

6. **Выполните миграции БД:**
   ```bash
   alembic upgrade head
   ```

7. **Запустите приложение:**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Приложение будет доступно по адресу:**
   - API: http://localhost:8000
   - Документация API: http://localhost:8000/docs

## Тестовые данные

После выполнения миграций в базе данных создаются следующие тестовые пользователи:

### Пользователь
- **Email:** `user@test.com`
- **Password:** `user123`
- **Full Name:** `Test User`

### Администратор
- **Email:** `admin@test.com`
- **Password:** `admin123`
- **Full Name:** `Test Admin`

Для тестового пользователя автоматически создается счет с ID = 1 и балансом 0.00.

## API Endpoints

### Аутентификация

- `POST /api/v1/auth/login/access-token` - Универсальная авторизация (работает для пользователей и администраторов)

### Пользователь (требует аутентификации)

- `GET /api/v1/users/me` - Получить данные о себе
- `GET /api/v1/users/accounts` - Получить список своих счетов
- `GET /api/v1/users/payments` - Получить список своих платежей

### Администратор (требует аутентификации)

- `GET /api/v1/admin/me` - Получить данные о себе
- `POST /api/v1/admin/users` - Создать пользователя
- `GET /api/v1/admin/users` - Получить список всех пользователей
- `GET /api/v1/admin/users/{user_id}` - Получить пользователя по ID
- `PUT /api/v1/admin/users/{user_id}` - Обновить пользователя
- `DELETE /api/v1/admin/users/{user_id}` - Удалить пользователя
- `GET /api/v1/admin/users/{user_id}/accounts` - Получить счета пользователя

### Webhook

- `POST /api/v1/webhook` - Обработка webhook от платежной системы

## Пример использования Webhook

Для обработки платежа необходимо отправить POST запрос на `/api/v1/webhook` со следующим JSON:

```json
{
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 1,
  "account_id": 1,
  "amount": 100,
  "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
}
```

Подпись (`signature`) формируется как SHA256 хеш от строки, состоящей из конкатенации значений объекта в алфавитном порядке ключей и секретного ключа:
```
{account_id}{amount}{transaction_id}{user_id}{secret_key}
```

Пример для `secret_key = "gfdmhghif38yrf9ew0jkf32"`:
```
11005eae174f-7cd0-472c-bd36-35660f00132b1gfdmhghif38yrf9ew0jkf32
```

## Архитектура

Проект следует принципам SOLID и использует следующие паттерны проектирования:

- **Repository Pattern** - для абстракции доступа к данным
- **Service Pattern** - для бизнес-логики
- **Dependency Injection** - для управления зависимостями

## Безопасность

- Пароли хешируются с использованием bcrypt
- JWT токены для аутентификации
- Проверка подписи для webhook запросов
- Валидация данных через Pydantic схемы

## Разработка

Для разработки с hot-reload:

```bash
uvicorn app.main:app --reload
```

Или с Docker Compose (уже настроен в docker-compose.yml):

```bash
docker-compose up
```

## Разработка

Подробная информация о процессе разработки, проверке кода, работе с базой данных и инструментах разработки находится в файле [DEV.md](DEV.md).

### Быстрый старт для разработчиков

```bash
# Установить dev-зависимости
make install-dev

# Установить pre-commit hooks
make pre-commit-install

# Запустить проверки
make check-all
```

## Лицензия

Этот проект создан в образовательных целях.
