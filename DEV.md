# Руководство по разработке

Данный документ содержит информацию о процессе разработки, инструментах проверки кода, работе с базой данных и других аспектах разработки проекта.

## Содержание

- [Быстрый старт](#быстрый-старт)
- [Проверка кода](#проверка-кода)
- [Работа с базой данных](#работа-с-базой-данных)
- [Инструменты разработки](#инструменты-разработки)
- [Интеграция с IDE](#интеграция-с-ide)
- [CI/CD](#cicd)

## Быстрый старт

### 1. Установка инструментов разработки

```bash
# Установить dev-зависимости
pip install -r requirements-dev.txt

# Или используйте Makefile
make install-dev
```

### 2. Настройка pre-commit hooks (рекомендуется)

Для автоматической проверки кода перед каждым коммитом:

```bash
pre-commit install

# Или через Makefile
make pre-commit-install
```

После установки все проверки будут запускаться автоматически перед каждым коммитом.

## Проверка кода

Проект использует современные инструменты для обеспечения качества кода:

- **Ruff** - быстрый линтер и форматтер (заменяет flake8, pylint, isort, black)
- **MyPy** - статический анализатор типов
- **Pre-commit** - автоматические проверки перед коммитом

### Использование через Makefile (Linux/Mac/WSL)

```bash
make lint          # Проверка кода линтером
make format        # Форматирование кода
make type-check    # Проверка типов
make fix           # Автоматическое исправление проблем (включая небезопасные)
make fix-safe      # Автоматическое исправление только безопасных проблем
make check-all     # Все проверки
make lint-errors   # Показать только ошибки (без предупреждений)
```

### Прямые команды

```bash
# Линтинг
ruff check .

# Форматирование
ruff format .

# Проверка типов
mypy app

# Исправление проблем
ruff check --fix .
ruff format .
```

### Игнорирование правил

Если нужно игнорировать конкретное правило:

```python
# ruff: noqa: PLR0913
def function_with_many_args(...):
    pass
```

Или для всей строки:

```python
some_code()  # noqa
```

Для MyPy:

```python
some_code()  # type: ignore
```

## Работа с базой данных

### Миграции Alembic

Проект использует Alembic для управления миграциями базы данных.

#### Создание новой миграции

```bash
# Автоматическое создание миграции на основе изменений моделей
alembic revision --autogenerate -m "описание изменений"

# Ручное создание пустой миграции
alembic revision -m "описание изменений"
```

#### Применение миграций

```bash
# Применить все миграции до последней
alembic upgrade head

# Применить конкретную миграцию
alembic upgrade <revision_id>

# Откатить последнюю миграцию
alembic downgrade -1

# Откатить все миграции
alembic downgrade base
```

#### С Docker Compose

```bash
# Применить миграции
docker-compose exec app alembic upgrade head

# Создать новую миграцию
docker-compose exec app alembic revision --autogenerate -m "описание"
```

### Структура миграций

Миграции находятся в директории `alembic/versions/`:

- `001_initial_migration.py` - начальная миграция (создание таблиц)
- `002_add_test_data.py` - добавление тестовых данных

### Тестовые данные

После применения миграций в базе данных автоматически создаются:

**Пользователь:**
- Email: `user@test.com`
- Password: `user123`
- Full Name: `Test User`
- Счет с ID = 1 и балансом 0.00

**Администратор:**
- Email: `admin@test.com`
- Password: `admin123`
- Full Name: `Test Admin`

## Инструменты разработки

### Ruff

**Ruff** - современный, очень быстрый линтер и форматтер для Python, который заменяет:
- flake8
- pylint
- isort
- black
- и многие другие инструменты

**Преимущества:**
- В 10-100 раз быстрее традиционных инструментов
- Один инструмент вместо множества
- Активная разработка и поддержка
- Отличная интеграция с современными проектами

**Конфигурация:** `pyproject.toml` (секция `[tool.ruff]`)

**Основные правила:**
- Длина строки: 100 символов
- Python версия: 3.9+
- Включены правила из pycodestyle, pyflakes, flake8-bugbear, pylint и других

### MyPy

**MyPy** - статический анализатор типов для Python. Проверяет соответствие кода аннотациям типов.

**Конфигурация:** `pyproject.toml` (секция `[tool.mypy]`)

**Особенности:**
- Проверка типов с учетом аннотаций
- Игнорирование некоторых модулей (alembic, sqlalchemy и др.)
- Предупреждения о неиспользуемых игнорированиях

### Pre-commit

**Pre-commit** - фреймворк для управления git hooks. Автоматически запускает проверки перед коммитом.

**Конфигурация:** `.pre-commit-config.yaml`

**Установленные хуки:**
- Ruff (линтер и форматтер)
- MyPy (проверка типов)

## Разработка с hot-reload

Для разработки с автоматической перезагрузкой при изменении кода:

```bash
# Без Docker
uvicorn app.main:app --reload

# С Docker Compose (уже настроен в docker-compose.yml)
docker-compose up
```

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
├── pyproject.toml     # Конфигурация инструментов разработки
└── requirements.txt   # Зависимости Python
```

## Архитектурные паттерны

Проект следует принципам SOLID и использует следующие паттерны:

- **Repository Pattern** - для абстракции доступа к данным
- **Service Pattern** - для бизнес-логики
- **Dependency Injection** - для управления зависимостями

## Интеграция с IDE

### PyCharm

1. **Ruff:**
   - Установите плагин Ruff (если доступен)
   - Или настройте внешний инструмент:
     - File → Settings → Tools → External Tools
     - Добавьте Ruff с командой: `ruff check $FilePath$`

2. **MyPy:**
   - PyCharm имеет встроенную поддержку MyPy
   - Включите проверку типов в Settings → Editor → Inspections → Python → Type checker

### VS Code

1. **Ruff:**
   - Установите расширение "Ruff" из маркетплейса VS Code
   - Настройки автоматически подхватываются из `pyproject.toml`

2. **MyPy:**
   - Установите расширение "Pylance" (встроено в Python extension)
   - Настройки типов автоматически подхватываются из `pyproject.toml`

## CI/CD

Для автоматической проверки в CI/CD добавьте в ваш workflow:

```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

- name: Run Ruff
  run: ruff check .

- name: Run Ruff format check
  run: ruff format --check .

- name: Run MyPy
  run: mypy app

- name: Run tests (если есть)
  run: pytest
```

## Отладка

### Логирование

Приложение использует стандартное логирование Python. Для настройки уровня логирования измените переменные окружения или конфигурацию.

### Работа с базой данных

Для прямого доступа к базе данных:

```bash
# С Docker Compose
docker-compose exec db psql -U postgres -d payment_system

# Без Docker
psql -U postgres -d payment_system
```

## Дополнительная информация

- [Документация Ruff](https://docs.astral.sh/ruff/)
- [Документация MyPy](https://mypy.readthedocs.io/)
- [Документация Pre-commit](https://pre-commit.com/)
- [Документация Alembic](https://alembic.sqlalchemy.org/)
- [Документация FastAPI](https://fastapi.tiangolo.com/)
- [Документация SQLAlchemy](https://docs.sqlalchemy.org/)
