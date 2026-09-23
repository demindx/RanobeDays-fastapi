# Backend Tasks

> Контракт API, который ждёт фронтенд, описан в корневом `tasks.md` (раздел «Контракт API» и «Разрывы контракта»).
> Задачи ниже расположены в рекомендуемом порядке. Одна задача — одна ветка и один PR.

## Как мы работаем по TDD

Для каждой задачи используем один цикл:

1. Сначала согласовываем бизнес-правила и наблюдаемое поведение.
2. Я подготавливаю или ревьюю падающие тесты — стадия **Red**.
3. Ты пишешь минимальную реализацию, которая делает тесты зелёными — стадия **Green**.
4. Я делаю review кода и тестов; после этого выполняется рефакторинг — стадия **Refactor**.
5. Перед merge запускаются `uv run pytest` и проверки проекта.

Тесты делим по назначению:

- `tests/unit/` — сервисы и бизнес-правила без PostgreSQL;
- `tests/integration/` — SQLAlchemy-модели, constraints, repositories и Alembic;
- `tests/api/` — HTTP-контракт FastAPI целиком.

Не нужно сразу переносить существующие 87 тестов. Новую структуру начинаем применять с новых задач, старые тесты переносим только при изменении соответствующего модуля.

## Рекомендуемый порядок

### Этап 1 — фундамент

#### B-001 — Настроить Alembic

- [x] Инициализировать async Alembic environment в `backend/`.
- [x] Подключить `Base.metadata` и импорт всех ORM-моделей в `alembic/env.py`.
- [x] Получать URL базы из `src.config`, не хранить пароль в `alembic.ini`.
- [x] Создать начальную миграцию со всеми существующими таблицами и `pgvector` extension.
- [x] Проверить миграцию вручную: пустая БД → `upgrade head` → приложение запускается.
- [x] Добавить integration-тест: `upgrade head` создаёт схему, повторный `upgrade head` безопасен.
- [x] Убрать `drop_all/create_all` из обычного startup. Если dev-reset нужен, оформить его отдельной явной командой.
- [ ] Добавить в README команды `revision --autogenerate`, `upgrade head`, `downgrade -1`.

**Готово, когда:** схема создаётся только миграциями, а `uv run alembic check` не обнаруживает незаписанных изменений моделей.

#### B-002 — Привести конфигурацию к разным окружениям

- [ ] Написать unit-тесты конфигурации: явный `POSTGRES_URL` не перезаписывается; host для local/test/docker задаётся окружением.
- [ ] Убрать неиспользуемый `POSTGRES_DB_HOST_PORT`.
- [ ] Убрать слабый production-default у `SECRET_KEY`; приложение должно явно сообщать об отсутствующем секрете вне dev.
- [x] Сделать `DB_ECHO=false` значением по умолчанию.
- [ ] Обновить `.env.example` без реальных секретов.

#### B-003 — Зафиксировать контракт транзакции

- [ ] Добавить integration-тест: многошаговый сценарий `AuthService.register()` полностью откатывается, если профиль не создался.
- [ ] Добавить аналогичный тест для `TeamService.create()`: команда и membership создаются атомарно.
- [ ] Переписать session dependency на явный `async with session.begin()` либо документировать текущий commit/rollback контракт.
- [ ] Зафиксировать правило: repositories делают `flush`, но никогда не делают `commit`.

**Архитектурное решение:** отдельный Unit of Work пока не вводим. Возвращаемся к нему, когда появятся фоновые задачи или use case вне HTTP.

### Этап 2 — надёжные базовые слои

#### B-004 — Уточнить семантику Repository

- [ ] Сначала написать contract-тесты для `PostgresRepository`.
- [ ] Зафиксировать поведение отсутствующего объекта для `get`, `get_or_raise`, `update`, `delete`.
- [ ] `delete` отсутствующего объекта не должен молча возвращать успешный результат.
- [ ] Все списки должны иметь стабильный `ORDER BY`.
- [ ] Проверять `limit >= 1`, верхний предел `limit` и `offset >= 0` на HTTP-границе.
- [ ] Не распознавать unique violation через поиск строки `"unique"`; использовать constraint/SQLSTATE и возвращать `409 Conflict`.

#### B-005 — Ограничить универсальный `Base.from_data`

- [ ] Написать тест, доказывающий текущее опасное поведение: неизвестное или обязательное поле может быть молча отброшено.
- [ ] Не связывать базовую SQLAlchemy-модель с конкретной Pydantic create-схемой.
- [ ] Для простого CRUD разрешить явный mapper/helper.
- [ ] Для сущностей с actor/ownership использовать именованные методы сервиса и явный конструктор ORM-модели.
- [ ] Существующие сервисы переводить постепенно, без массового переписывания всех модулей.

#### B-006 — Разделить общие типы и ORM

- [ ] При первом изменении каждого модуля переносить общие enum/value types из `models.py` в независимый `types.py`.
- [ ] Pydantic schemas и ORM models должны импортировать общий тип, но не импортировать друг друга.
- [ ] Начать с `UserRoleEnum`, `TeamType`, `TeamUserRole`, `NovelType`, `NovelStatus`.
- [ ] Добавить тесты сериализации значений enum в API.

#### B-007 — Исправить query/pagination для relationships

- [ ] Написать regression-тест `TeamRepository.get_novels(offset=50, limit=50)`.
- [ ] Выполнять фильтрацию, сортировку, offset и limit в SQL, не загружать всю `team.novels` в память.
- [ ] Убрать `run_sync` для ленивой загрузки из routers/repositories.
- [ ] Для каждого response явно выбирать `selectinload`/`joinedload` в query-методе.

### Этап 3 — Bookmarks как первый эталонный TDD-модуль

#### B-010 — Согласовать доменный и HTTP-контракт bookmarks

- [ ] Ответить и записать в `docs/domain/bookmarks.md`:
  - является bookmark папкой пользователя, публичной коллекцией или обоими вариантами;
  - уникально ли имя в пределах одного пользователя;
  - кто может читать приватную/публичную коллекцию;
  - кто может менять название, публичность и items;
  - что происходит с items при удалении bookmark или novel.
- [ ] Зафиксировать endpoints, request/response и HTTP-коды до реализации.
- [ ] Владельца брать только из `CurrentUser`, никогда не принимать `user_id` из body.
- [ ] Согласовать минимальный response: `id`, `name`, `is_public`, `owner_id`, `items`, timestamps при необходимости.

#### B-011 — Модели и миграция bookmarks

- [ ] Написать integration-тесты constraints до миграции.
- [ ] Добавить unique constraint `(user_id, name)`, если он подтверждён контрактом.
- [ ] Проверить составной PK `(bookmark_id, novel_id)` и каскадное удаление.
- [ ] Сделать relationship `Bookmark.items` ↔ `BookmarkItem.bookmark` симметричным через `back_populates`.
- [ ] Создать и вручную просмотреть Alembic migration.

#### B-012 — BookmarkRepository

- [ ] Тест: получить только bookmarks конкретного владельца с пагинацией и стабильной сортировкой.
- [ ] Тест: получить публичную коллекцию по id.
- [ ] Тест: повторное добавление novel возвращает domain/app conflict, а не сырой `IntegrityError`.
- [ ] Тест: отсутствующие bookmark/novel дают определённую ошибку.
- [ ] Реализовать только query-методы, необходимые этим сценариям.

#### B-013 — BookmarkService

- [ ] Создать `FakeBookmarkRepository` для unit-тестов.
- [ ] Тест: `create_for_user(actor_id, data)` устанавливает владельца из actor.
- [ ] Тест: пользователь не меняет и не удаляет чужой bookmark.
- [ ] Тест: приватный bookmark недоступен постороннему.
- [ ] Тест: novel нельзя добавить повторно.
- [ ] Тест: одна бизнес-операция атомарна.
- [ ] Реализовать именованные методы; общий `AbstractService` оставить для подходящего CRUD.

#### B-014 — Bookmark API

- [ ] Написать API-тесты на успешные сценарии, `401`, `403`, `404`, `409`, `422`.
- [ ] Добавить router/dependencies и подключить router к `/api/v1`.
- [ ] Заполнить `BookmarkItemResponse` и `BookmarkResponse`.
- [ ] Проверить OpenAPI и обновить контракт в корневом `tasks.md` для frontend.

### Этап 4 — безопасность и существующие модули

#### B-020 — Укрепить refresh-token flow

- [ ] Тест: некорректный UUID cookie возвращает контролируемый `401`, а не `500`.
- [ ] Тест: неизвестная, истёкшая и повторно использованная refresh-session отклоняются.
- [ ] Тест: logout с неизвестным token имеет согласованную идемпотентную семантику.
- [ ] Инъецировать clock/token generator в `AuthService`, если это упростит детерминированные unit-тесты.
- [ ] Проверить rotation, fingerprint и cookie attributes (`HttpOnly`, `Secure`, `SameSite`).

#### B-021 — Авторизация мутаций

- [ ] Составить таблицу ролей и действий для users, teams, novels и chapters.
- [ ] Написать API-тесты прав до добавления dependencies/policies.
- [ ] Авторизация должна использовать `CurrentUser`, а не actor id из body.
- [ ] Запретить назначение роли `CREATOR` обычным add-user endpoint.

#### B-022 — Устранить двойной источник истины создателя команды

- [ ] Принять решение: источник истины — `Team.creator_id` или membership с ролью `CREATOR`.
- [ ] Тест: создателя нельзя случайно удалить из команды.
- [ ] Тест: у команды ровно один creator согласно выбранной модели.
- [ ] Зафиксировать решение коротким ADR в `docs/architecture/decisions/`.

#### B-023 — One-to-one User ↔ UserProfile

- [ ] Тест: у пользователя невозможно создать второй профиль.
- [ ] Добавить unique constraint на `user_profiles.user_id` и миграцию.
- [ ] Проверить cascade при удалении пользователя.

### Этап 5 — API, нужное frontend

#### B-030 — Контракт novel details

- [ ] Согласовать `rating`, `rating_count`, `team`, `chapter_count`, `reading_progress`.
- [ ] Не добавлять заглушечные поля без источника данных.
- [ ] Написать API-тест response schema и query-count/N+1 для novel list/details.

#### B-031 — Главы конкретной новеллы

- [ ] Добавить тесты `GET /novel/{id}/chapters`: сортировка по номеру, пагинация, только опубликованные главы для обычного пользователя.
- [ ] Уточнить контракт `content`: строка или структурированные блоки; хранение и API-представление могут различаться.
- [ ] Добавить недостающие поля response только после согласования с frontend.

#### B-032 — Reading progress

- [ ] Сначала описать правило «глава прочитана» и способ вычисления процента.
- [ ] Добавить модель/constraints/migration.
- [ ] Unit-тесты сервиса: прогресс не уменьшается случайно, чужой прогресс недоступен.
- [ ] API-тесты continue-reading и отметки прочтения.

### Этап 6 — следующие сущности

- [ ] **Ratings:** один рейтинг пользователя на novel, допустимый диапазон, пересчёт aggregate.
- [ ] **Comments:** ownership, edit/delete window, moderation, пагинация, ответы на комментарии.
- [ ] **Notifications:** сначала определить события-источники; не создавать notification из router напрямую.
- [ ] **Profile statistics:** определить, какие показатели хранятся, а какие вычисляются запросом.
- [ ] **Featured/updates/recommendations:** сначала простые query rules; ML/embeddings вводить только после появления измеримого требования.

## Общие критерии готовности любого backend PR

- [ ] Тест сначала воспроизводил отсутствие нужного поведения или баг.
- [ ] Есть happy path и основные отрицательные сценарии.
- [ ] Router не содержит SQL и бизнес-правил.
- [ ] Repository не делает `commit` и не возвращает HTTPException.
- [ ] Service не зависит от FastAPI Request/Response.
- [ ] Изменение модели сопровождается проверенной Alembic migration.
- [ ] Пагинация выполняется в SQL и имеет стабильную сортировку.
- [ ] Ошибки не раскрывают детали SQL/секреты.
- [ ] `uv run pytest` проходит полностью.
- [ ] Контракт frontend/OpenAPI обновлён, если изменился HTTP API.

## История выполненного архитектурного ревью

### P0 — критические баги моделей

- [x] `chapter/models.py` — убрать `primary_key=True` у `novel_id` и `team_id` (сейчас композитный PK `(id, novel_id, team_id)`). PK — только `id`.
- [x] `teams/models.py` + `users/models.py` — починить связь `Team.users` ↔ `User.teams`: `User.teams` → `Mapped[list[Team]]`, добавить `secondary="team_users"` (или association-объект). Сейчас связь «команда↔участник» делается вручную через JOIN в репозитории.
- [x] Ленивые связи в async-ответах: `Novel.chapters`, `Team.novels`, `Team.users` — перевести на `lazy="selectin"`/`selectinload`, иначе будет `MissingGreenlet` при добавлении в response-схемы (как было с `user_profile`).
- [x] `users/repository.py` — в `get_by_login`/`get_by_email` в `NotFound(...)` передаётся встроенная функция `id` вместо `login`/`email`.

### P1 — слои / DRY

- [x] `users/service.py` — `UserService.create` дублирует `User.from_data()`; сам `from_data()` сломан (не исключает `nickname`, которого нет в модели). Убрать дублирование, починить/использовать `from_data`.
- [x] `teams/service.py` — `get_users()` возвращает `list[tuple]` (сырые строки БД), роутер мапит через `UserTeamResponse.from_tuple`. Возвращать типизированные объекты из service.
- [x] `auth/repository.py` — `AuthRepository` не наследует `AbstractRepository`/`PostgresRepository`; привести к общему паттерну (или осознанно задокументировать отклонение).

### P2 — нейминг / консистентность

- [x] Опечатки: `CategoryResponse` → `CategoryResponse`, `LanguageResponse` → `LanguageResponse`, `NoneObjectEncoutered` → `NoneObjectEncountered`.
- [x] `country/router.py` — переименовать `get_languages`/`create_language`/... → `get_countries`/`create_country`/... (copy-paste).
- [x] Response-схемы `Category`/`Language`/`Country` не содержат `id` — добавить.
- [x] `core/database.py` — `echo=True` вынести в конфиг (убрать хардкод SQL-логов).
- [ ] `config.py` — убрать неиспользуемый `POSTGRES_DB_HOST_PORT`; усилить дефолт `SECRET_KEY` (см. B-002).
- [ ] `bookmark/` — доделать модуль (см. B-010—B-014).
- [x] `AbstractRepository` — вынести `model` в класс-атрибут вместо name-mangled `__model`/`__session` (неидиоматично).
