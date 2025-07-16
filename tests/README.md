# Тесты для RanobeDays

Этот проект использует comprehensive test suite с разными типами тестов.

## Структура тестов

```
tests/
├── conftest.py              # Общие фикстуры
├── factories.py             # Фабрики для тестовых данных
├── unit/                    # Unit тесты (изолированные)
│   └── users/
│       └── test_user_service.py
├── integration/             # Integration тесты (с реальной БД)
│   └── users/
│       └── test_user_repository.py
└── api/                     # API тесты (HTTP endpoints)
    └── users/
        └── test_user_endpoints.py
```

## Типы тестов

### 🔬 **Unit тесты** (`@pytest.mark.unit`)
- Тестируют бизнес-логику изолированно
- Используют моки для зависимостей
- Быстрые и надежные
- Покрывают все возможные сценарии UserService

### 🏗️ **Integration тесты** (`@pytest.mark.integration`)
- Тестируют работу с реальной БД (SQLite в памяти)
- Проверяют репозитории, модели, связи
- Тестируют каскадные удаления, уникальные ограничения
- Покрывают UserRepository

### 🌐 **API тесты** (`@pytest.mark.api`)
- Тестируют HTTP endpoints полностью
- Проверяют формат ответов, статус-коды
- Тестируют error handling
- Покрывают все user endpoints

## Запуск тестов

### Установка зависимостей
```bash
uv sync --group test
```

### Запуск всех тестов
```bash
uv run pytest
```

### Запуск по типам
```bash
# Только unit тесты
uv run pytest -m unit

# Только integration тесты
uv run pytest -m integration

# Только API тесты
uv run pytest -m api
```

### Запуск с покрытием
```bash
uv run pytest --cov=src --cov-report=html
```

### Запуск конкретного файла
```bash
uv run pytest tests/unit/users/test_user_service.py -v
```

## Фикстуры

### Основные фикстуры (conftest.py)
- `test_session` - асинхронная сессия БД для каждого теста
- `async_test_client` - асинхронный HTTP клиент
- `override_get_db_session` - переопределение зависимости БД

### Фабрики (factories.py)
- `UserModelFactory` - создание тестовых пользователей
- `AdminUserFactory` - создание администраторов
- `UserProfileModelFactory` - создание профилей

## Покрытие тестами

Текущее покрытие:
- ✅ **UserService** - 100% (все методы + edge cases)
- ✅ **UserRepository** - 100% (CRUD + связи + ограничения)
- ✅ **User Endpoints** - 100% (все HTTP методы + error cases)

## Лучшие практики

1. **Arrange-Act-Assert** паттерн во всех тестах
2. **Изоляция тестов** - каждый тест независим
3. **Descriptive names** - понятные имена тестов
4. **Фабрики вместо фикстур** для создания данных
5. **Моки для unit тестов**, реальная БД для integration

## Добавление новых тестов

При добавлении новых модулей следуйте этой структуре:
```
tests/
├── unit/
│   └── new_module/
│       └── test_new_service.py
├── integration/
│   └── new_module/
│       └── test_new_repository.py
└── api/
    └── new_module/
        └── test_new_endpoints.py
```

## Примеры команд

```bash
# Быстрые unit тесты (для development)
uv run pytest -m unit --tb=short

# Полный прогон (для CI/CD)
uv run pytest --cov=src --tb=short

# Debug конкретного теста
uv run pytest tests/unit/users/test_user_service.py::TestUserService::test_create_user_success -vvv

# Запуск только failed тестов
uv run pytest --lf
```
