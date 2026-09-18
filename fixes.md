# Review последних пяти pull request

Дата ревью: 2026-08-24. Проверены merge-diff и итоговое состояние `master` для:

- PR #11 `novels` (`713c2cf`)
- PR #12 `chapters` (`70f5bc6`)
- PR #13 `paginated-responses` (`3777313`)
- PR #14 `frontend` (`f910572`)
- PR #15 `fixes` (`4c0bc51`)

Baseline, подтверждённый владельцем проекта: `uv run pytest` — **87 passed in 25.30s**. Frontend: **13 tests passed**, `npm run lint` и `npm run build` успешны.

Зелёный baseline означает, что реализация соответствует существующим тестам. Он не означает, что проверены права доступа, безопасность refresh-токена, все внешние ключи и граничные значения: таких контрактов в текущем наборе почти нет.

## Итог ревью

Сейчас принимать новые CRUD-функции поверх этой архитектуры рискованно. Главные блокеры: приложение удаляет схему БД при старте, изменяющие ручки не имеют authorization/ownership-проверок, а refresh-cookie не работает из frontend при cross-origin запросах. После них следует стабилизировать доменные ограничения, пагинацию и контракт ошибок.

## P0 — блокирует production/merge следующей функциональности

> Решение владельца от 2026-08-24: пункты 1–2 являются сознательным dev-режимом. Они допустимы локально, но перед staging должны быть закрыты либо защищены явными настройками, которые по умолчанию выключены.

### 1. Приложение удаляет все данные при каждом старте

**Где:** `backend/src/main.py`, `backend/src/core/database.py:init_db`.

Lifespan всегда вызывает `init_db()`, а функция выполняет `Base.metadata.drop_all()` перед `create_all()`. Рестарт backend уничтожает пользователей, refresh-сессии, команды, новеллы и главы. PR #14 менял startup/CORS и интеграцию, но опасное поведение осталось частью production startup.

**Исправление:** убрать DDL из lifespan; добавить Alembic и выполнять миграции отдельным deployment-шагом. Создание extension также должно быть миграцией/операционной подготовкой с отдельными правами.

**Красный тест:** поднять приложение дважды на БД с заранее созданной записью и подтвердить, что запись сохранилась.

### 2. Все изменяющие доменные ручки доступны анонимно

**Где:** routers `users`, `teams`, `novel`, `chapter`, `category`, `country`, `language`.

Без токена сейчас можно:

- изменить любой профиль, включая `readed_chapters`;
- создать, изменить или удалить команду;
- добавить/удалить любого участника команды, в том числе создателя;
- создать, изменить или удалить новеллу и главу;
- менять справочники.

Текущие endpoint-тесты вызывают эти операции без `Authorization` и ожидают 200, то есть закрепляют уязвимость как контракт.

**Исправление:** аутентификацию оставить FastAPI dependency, а решение по правам вынести в явные policy/use-case функции сервисного слоя. Правила должны учитывать actor, resource и action. Router не должен быть единственным местом защиты, иначе другой entry point сможет обойти правило.

**Минимальный контракт:** anonymous → 401; authenticated, но без права → 403; отсутствующий ресурс для допустимого actor → 404. Нужно отдельно решить, скрывать ли существование чужого ресурса через 404 вместо 403.

### 3. Refresh/logout из браузерного frontend фактически не работают

> Статус после frontend TDD-пакета: `credentials: 'include'` добавлен и покрыт тестом. Backend-настройки cookie и выбор единой модели хранения refresh-token остаются открытыми.

**Где:** `frontend/src/api/client.js`, `frontend/src/api/auth.js`, `backend/src/auth/router.py`.

Frontend обращается с `localhost:5173` к `localhost:8080`, но `fetch` не получает `credentials: 'include'`. Поэтому браузер не обязан сохранить и отправить `refresh_token` cookie. CORS backend уже разрешает credentials, но клиент эту возможность не включает.

Дополнительно cookie устанавливается без `HttpOnly`, `Secure`, явного `SameSite`, `Path` и срока жизни, а сам refresh-token одновременно возвращается в JSON. Это размывает выбранную модель хранения и увеличивает последствия XSS.

**Исправление:** сначала выбрать один контракт:

- browser/BFF-подход: refresh только в `HttpOnly` cookie, access в памяти, `credentials: 'include'`, CSRF-модель документирована;
- token API для недоверенного native-клиента: оба токена в body, без притворной cookie-схемы.

Для текущего Vue SPA предпочтительнее первый вариант. Не хранить долгоживущий refresh-token в доступном JavaScript месте.

**Красный тест frontend:** login response с `Set-Cookie`, затем refresh/logout; проверить `credentials: 'include'`. **Backend-тест:** проверить атрибуты `Set-Cookie`.

### 4. Интеграционные тесты могут уничтожить ошибочно указанную БД

**Где:** `backend/tests/conftest.py`.

Session fixture без защитной проверки выполняет `drop_all()` для любого значения `TEST_DATABASE_URL`. Опечатка в окружении может направить тесты на рабочую БД.

**Исправление:** перед destructive DDL проверять отдельный явный флаг и allowlist имени/хоста БД (например, имя обязано оканчиваться `_test`); production-like URL должен приводить к немедленному отказу до подключения/DDL.

## P1 — ошибки поведения и контракта

### 5. Неизвестный или повторно использованный refresh-token приводит к 500

**Где:** `backend/src/auth/service.py`, `backend/src/auth/repository.py`.

- `uuid.UUID(hex=refresh_token)` выбрасывает необработанный `ValueError` для мусорной cookie.
- `scalar_one()` выбрасывает `NoResultFound`; последующий `if not session` недостижим.
- тестируется отсутствие cookie и happy path, но не malformed, expired, revoked и replayed token.
- fingerprint при refresh заменяется случайным UUID и нигде не проверяется, поэтому заявленная привязка сессии к устройству не действует.

**Исправление:** нормализовать malformed/unknown/expired/replayed в согласованный 401; rotation выполнять атомарно; определить и проверить политику reuse detection; либо реально валидировать fingerprint, либо удалить его из контракта.

### 6. Пагинация новелл команды режет список неправильно

**Внесено:** PR #13. **Где:** `backend/src/teams/repository.py:get_novels`.

Используется `team.novels[offset:limit]`, тогда как верхняя граница должна быть `offset + limit`. Например, `offset=10&limit=20` возвращает только элементы с индексами 10..19, а не 20 элементов. При `offset >= limit` результат всегда пуст. Кроме того, сначала загружаются все новеллы, а пагинация делается в Python.

**Исправление:** отдельный SQL query с `WHERE team_id`, детерминированным `ORDER BY`, `OFFSET`, `LIMIT`. Добавить тесты `offset=1, limit=2`, `offset > limit`, последняя страница.

### 7. Общая пагинация недетерминирована и не ограничена

**Внесено:** PR #13. **Где:** list routers и `PostgresRepository.get_all`.

Нет `ORDER BY`, поэтому между запросами возможны пропуски/дубли. `limit` и `offset` принимают отрицательные и чрезмерные значения. В response отсутствуют `total`/`has_next`, поэтому клиент не знает, существует ли следующая страница.

**Исправление:** общий `PaginationParams` через `Query(ge=0/le=...)`, стабильная сортировка с уникальным tie-breaker, единый `Page[T]`. Решить сейчас, будет ли публичный контракт offset- или cursor-based; не поддерживать оба без реальной потребности.

### 8. Внешние ключи и доменные инварианты дают 500 либо допускают противоречивые данные

**Где:** services/models/repositories `novel`, `chapter`, `teams`, справочники.

- `NovelService.create` проверяет только `team_id`; неизвестные `language_id`/`country_id` уходят в raw `IntegrityError`.
- `ChapterService` не проверяет `novel_id` и `team_id`.
- для `(novel_id, number)` нет uniqueness: у новеллы могут быть две главы №1.
- можно создать главу от команды, не связанной с новеллой; допустимость этого должна стать явным доменным решением.
- `add_user` не различает отсутствующую команду/пользователя и конфликт членства.
- `/teams/{missing}/users` возвращает пустой список вместо 404.
- создателя команды можно удалить из membership, оставив `creator_id` и роли в противоречии.
- удаление используемых language/country/category/novel может завершиться необработанным constraint error; cascade/restrict политика не описана.

**Исправление:** определить aggregate boundaries и инварианты, продублировать критичные правила DB constraints, а ошибки БД переводить в стабильные 404/409. Не использовать 400 для любого нарушения ссылки.

### 9. Входные схемы почти не задают границы сущностей

**Где:** Pydantic schemas всех модулей.

Принимаются пустые строки, отрицательные `age_limit`, `chapter.number <= 0`, отрицательный `readed_chapters`, очень длинные значения до ошибки БД и пароль из одного символа. Ограничения SQL `String(50/100/255)` не отражены в API-схемах, поэтому часть плохих данных превращается в 500 вместо 422.

**Исправление:** constrained fields/annotated value objects для Login, Password, DisplayName, Title, ChapterNumber, AgeLimit; `extra='forbid'` для command-схем; одинаковые ограничения в Pydantic и БД.

### 10. Аутентификация раскрывает существование аккаунта и игнорирует статус пользователя

**Где:** `backend/src/auth/service.py`, `backend/src/auth/dependencies.py`.

Неизвестный login/email даёт 404, неверный пароль — 401: это позволяет перечислять аккаунты. `is_active` и `is_verified` не участвуют ни во входе, ни в проверке access-token.

**Исправление:** одинаковый внешний ответ/тайминг для неверных credentials; отдельное решение продукта для verified login; заблокированный пользователь не должен продолжать работать со старым access-token.

### 11. Публичная модель пользователя раскрывает email в списках

**Где:** `GET /users/`, `GET /users/{id}`, team users; `UserResponse`.

Анонимный список пользователей и участников команды содержит email, но при этом не содержит стабильного публичного `id`. Нужно отделить `PublicUserResponse` от `CurrentUserResponse`/admin response.

### 12. `Base.from_data()` молча проглатывает поля

**Внесено/закреплено:** PR #15. **Где:** `backend/src/core/models.py`.

Универсальный mapper проходит по `model_dump()` и устанавливает только уже существующие атрибуты. Если schema и model разойдутся, запрос будет принят, а поле бесшумно потеряется. Это скрывает ошибки контракта.

**Исправление:** явные фабрики для агрегатов или строгий mapper, который имеет осознанный allowlist и падает на неожиданном поле. Хеширование пароля и создание профиля остаются domain/application logic, а не обязанностью универсальной ORM-базы.

### 13. API использует несколько несовместимых форматов ответа

**Где:** `GenericResponse`, FastAPI validation, delete handlers.

- успешные операции возвращают `{code, message, data}`;
- `AppException` возвращает ту же обёртку;
- 422 возвращает стандартный `{detail: [...]}`;
- delete возвращает HTTP 200 с JSON `null`;
- поле `code` дублирует HTTP status и может с ним разойтись.

**Исправление:** считать HTTP status единственным источником статуса. Выбрать один error envelope (желательно problem-details-подобный), нормализовать validation errors, для create использовать 201, для delete — согласованные 204 или 200 response. Идемпотентность DELETE и ответ для отсутствующего ресурса нужно зафиксировать тестом, а не случайным `rowcount`.

### 14. Конфигурация небезопасна и плохо переносима

**Где:** `backend/src/config.py`.

Слабый `SECRET_KEY` задан по умолчанию, `DB_ECHO=True`, а validator всегда перезаписывает `POSTGRES_URL` и жёстко задаёт host `db`. В production приложение может стартовать с известным JWT secret и логировать SQL; переданный полный DSN игнорируется.

**Исправление:** обязательные production secrets без дефолта, environment-aware settings, уважать явно переданный DSN, `DB_ECHO=False` по умолчанию, отдельные development/test presets.

### 15. Имена enum/полей уже становятся ошибочным внешним контрактом

**Где:** `NovelStatus.ABADONED`, `UserProfile.readed_chapters`, `NovelType.AUTHORS`.

Опечатки (`abandoned`, `read_chapters`) и неясное значение `authors` будут дорого исправляться после появления клиентов и сохранённых строк enum. Нужны миграция и версия/переходный alias до расширения API.

## P2 — качество и поддерживаемость

### 16. PR #14 слишком велик и смешивает независимые риски

152 файла и около 11 тысяч добавленных строк включают frontend redesign, API integration, Docker, backend auth/CORS/models, документацию и тестовую инфраструктуру. Такой PR невозможно надёжно откатить или ревьюить по одной причине изменения.

Разделять минимум на: infrastructure, API client/auth, backend contract, feature slices, UI redesign. Не хранить одновременно `bun.lock` и `package-lock.json`; выбрать один package manager. Удалить случайные артефакты `uvx` и `frontend/test-results/.last-run.json`, если они не являются осознанными fixtures.

### 17. Нет миграций и CI-gate

Изменения моделей в PR #11/#12/#14/#15 не сопровождаются миграциями. В репозитории нет CI workflow, который поднимает PostgreSQL/pgvector и запускает backend + frontend проверки. Локально зелёные тесты не защищают merge.

Минимальный gate: backend `ruff check --no-fix`, type check, `pytest`; frontend lint, test, build; migration upgrade на пустой БД и upgrade с предыдущей схемы.

### 18. `ruff check` в проекте мутирует файлы

В `[tool.ruff]` включены `fix=true` и `unsafe-fixes=true`, поэтому обычная проверка меняет рабочее дерево. Сейчас остаются четыре lint finding: три unused imports и устаревший второй type argument у `AsyncGenerator` в fixture.

Для CI/review использовать `ruff check --no-fix`; автоисправление вынести в отдельную явную команду. `unsafe-fixes` не должно быть неявным поведением проверки.

## Что уже исправлено внутри диапазона PR #11–#15

Не нужно повторно заводить эти defects без регрессии:

- PR #11 и #12 забывали `await service.get_by_id(...)`; исправлено в PR #14.
- response глав/новелл не содержал необходимых идентификаторов; часть полей добавлена в PR #14.
- PR #14 превращал отсутствующую refresh-cookie в ошибку до сервиса; PR #15 добавил обработку `None`. Malformed/revoked token всё ещё не обработан.
- проблемы composite PK главы, ORM relationships и async lazy loading исправлялись в PR #15; существующие response-shape тесты это частично покрывают.

## TDD-план для следующего PR

В review-only режиме тестовые файлы не изменялись. Следующий авторский PR стоит начинать с небольших красных наборов в таком порядке:

1. **Safety:** `test_startup_preserves_existing_data`, `test_test_database_guard_rejects_non_test_db`.
2. **Authorization matrix:** параметризованные anonymous/reader/member/manager/creator/admin тесты для каждой command-ручки.
3. **Refresh rotation:** malformed, unknown, expired, replayed, logout replay, cookie attributes и frontend credentials.
4. **Domain invariants:** неизвестные FK, duplicate chapter number, creator removal, referenced dictionary deletion.
5. **Pagination contract:** negative/oversized params, stable ordering, second/last/empty page, team novels с `offset > 0`.
6. **Schema boundaries:** пустые/слишком длинные строки, числовые границы, слабые пароли, extra fields.
7. **OpenAPI/error contract:** snapshot значимых schemas и одинаковый error envelope для 401/403/404/409/422.

Для TDD один цикл должен менять одно наблюдаемое правило: красный тест → минимальная реализация → рефакторинг при зелёном наборе. Не писать десятки тестов после готовой реализации: тогда они снова будут описывать случайное текущее поведение.

## Как хранить контракты сущностей

Не нужен один большой документ «все сущности». Источник истины лучше разделить по типу гарантии:

- **HTTP wire contract:** строгие Pydantic request/response/error schemas; из них FastAPI генерирует OpenAPI.
- **Persistence contract:** Alembic migrations и DB constraints.
- **Domain contract:** короткие policy/value-object/service tests для инвариантов, которые не выражаются одной схемой БД.
- **Архитектурные решения:** `docs/adr/NNNN-*.md` — почему выбран cookie refresh, RBAC/ownership, pagination, delete semantics.
- **Совместимость клиента:** небольшие consumer-contract тесты frontend против сохранённого OpenAPI или поднятого test app.

В OpenAPI не следует публиковать ORM-модели напрямую. Для одного понятия нужны отдельные контракты по намерению: `NovelCreate`, `NovelPatch`, `NovelPublic`, при необходимости `NovelAdmin`; `PublicUser` отдельно от `CurrentUser`.

## Вопросы владельцу перед архитектурным PR

1. Кто имеет право создавать новеллу/главу: глобальная роль, участник команды или только manager/creator конкретной команды?
2. Может ли одна команда владеть новеллой, а другая публиковать её главы? Ответ определяет модель ownership главы.
3. Профиль по `/users/{id}/profile` адресуется `user.id` или `user_profile.id`? Текущие тесты используют `profile.id`; совпадение первых sequence-значений может скрывать ошибку контракта.
4. Должны email и login быть публичными? Если нет, какие поля образуют публичную идентичность пользователя?
5. Нужна ли строгая идемпотентность DELETE (`204` даже при отсутствии) или отсутствие должно быть `404`?
6. Нужна ли fingerprint-привязка refresh-сессии? Если да, откуда браузер безопасно и стабильно получает fingerprint и что происходит при его смене?
7. Нужны ли номера глав уникальными только внутри новеллы, и допускаются ли дробные/специальные главы?
8. Что является источником истины для ошибок клиента: HTTP status или поле `code`? Рекомендуется оставить только HTTP status.

Пока эти ответы не зафиксированы ADR и красными контрактными тестами, выбор конкретных классов/паттернов authorization будет преждевременным.
