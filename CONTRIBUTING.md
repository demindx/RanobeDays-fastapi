# Contributing to RanobeDays

Спасибо за интерес к проекту! Этот документ содержит инструкции для разработчиков.

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (для управления зависимостями)
- Git

### Настройка окружения
```bash
# Клонирование репозитория
git clone https://github.com/your-username/RanobeDays-fastapi.git
cd RanobeDays-fastapi

# Установка зависимостей
uv sync --group test

# Настройка pre-commit hooks
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Запуск тестов
uv run pytest
```

## 📋 Workflow разработки

### 1. Создание ветки
```bash
git checkout -b feature/your-feature-name
git checkout -b bugfix/issue-description
git checkout -b docs/update-readme
```

### 2. Разработка
- Пишите код следуя стилю проекта
- Добавляйте тесты для новой функциональности
- Обновляйте документацию при необходимости

### 3. Коммиты
Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve database connection issue"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for user service"
```

Типы коммитов:
- `feat`: новая функциональность
- `fix`: исправление багов
- `docs`: изменения в документации
- `test`: добавление/изменение тестов
- `refactor`: рефакторинг кода
- `style`: форматирование, отсутствующие точки с запятой
- `perf`: изменения производительности
- `ci`: изменения в CI/CD
- `chore`: обновление зависимостей, прочее

### 4. Тестирование
```bash
# Запуск всех тестов
uv run pytest

# Только unit тесты
uv run pytest tests/unit/

# С покрытием
uv run pytest --cov=src

# Линтинг
uv run ruff check .
uv run ruff format .
```

### 5. Pull Request
1. Убедитесь, что все тесты проходят
2. Проверьте что код отформатирован
3. Создайте PR с описанием изменений
4. Дождитесь ревью

## 🧪 Тестирование

### Структура тестов
```
tests/
├── unit/          # Unit тесты (моки)
├── integration/   # Integration тесты (БД)
└── api/          # API тесты (HTTP)
```

### Написание тестов
```python
# Unit тест
@pytest.mark.unit
async def test_create_user_success(mock_repository):
    # Arrange, Act, Assert
    pass

# Integration тест
@pytest.mark.integration
async def test_user_repository_create(test_session):
    pass

# API тест
@pytest.mark.api
async def test_get_users_endpoint(async_test_client):
    pass
```

### Запуск тестов
```bash
# По типу
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m api

# Конкретный файл
uv run pytest tests/unit/users/test_user_service.py

# Конкретный тест
uv run pytest tests/unit/users/test_user_service.py::TestUserService::test_create_user_success
```

## 📖 Стиль кода

### Python
- Используем **ruff** для форматирования и линтинга
- Максимальная длина строки: 88 символов
- Типизация обязательна для новых функций
- Docstrings для всех публичных методов

### Архитектура
Следуем **Clean Architecture**:
```
src/
├── core/          # Базовые компоненты
├── users/         # Модуль пользователей
│   ├── models.py     # SQLAlchemy модели
│   ├── schemas.py    # Pydantic схемы
│   ├── repository.py # Слой данных
│   ├── service.py    # Бизнес-логика
│   └── router.py     # HTTP эндпоинты
└── module_name/   # Новые модули
```

### Базы данных
- Используем **async SQLAlchemy**
- Миграции через **Alembic** (в будущем)
- Все изменения схемы документируем

## 🔍 Code Review

### Что проверяем
- [ ] Тесты написаны и проходят
- [ ] Код задокументирован
- [ ] Нет нарушений безопасности
- [ ] Производительность не ухудшилась
- [ ] API backward-compatible

### Ответ на ревью
- Отвечайте конструктивно
- Объясняйте сложные решения
- Не принимайте критику на личный счет
- Благодарите за фидбек

## 🎯 Приоритеты

### Высокий приоритет
- Тесты для существующего кода
- Исправление багов
- Документация API

### Средний приоритет
- Новая функциональность
- Оптимизация производительности
- Рефакторинг

### Низкий приоритет
- Косметические изменения
- Эксперименты

## 📞 Контакты

- GitHub Issues: для багов и фич
- Discussions: для вопросов
- Email: для приватных вопросов

## 📄 Лицензия

Внося изменения, вы соглашаетесь с лицензией проекта.
