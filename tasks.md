# tasks.md — Интеграция фронтенда с бэкендом

## Решения (зафиксированы)

- **Сторона выравнивания API — фронтенд под бэкенд.** Префикс `/api/v1`, ресурсы в единственном числе (`/novel`, `/chapter`, `/category`, `/lang`, `/country`, `/teams`, `/users`, `/auth`).
- **CORS — на бэке через `CORSMiddleware`** (задача бэка, см. `backend/tasks.md`). Фронт ходит на абсолютный `http://localhost:8080`.
- **Подключаем только то, что уже реализовано на бэке.** Остальное (каталог, главная, страница новеллы, закладки, профиль-статистика, уведомления, команды) остаётся на моках до появления эндпоинтов на бэке.
- **Обёртка ответов** `GenericResponse { code, message, data }` разворачивается на клиенте в `api/client.js`.

---

## 1. Контракт API (актуально на текущий бэкенд)

Все ответы обёрнуты: `{ "code": 200, "message": "success", "data": ... }`. Ошибки — `{ "code", "message" }` (из `AppException`) или `{ "detail": [...] }` (валидация FastAPI).

| Метод | Путь | Payload → Ответ (`data`) |
|---|---|---|
| POST | `/api/v1/auth/register` | `{login, email, nickname, password1, password2}` → `null` |
| POST | `/api/v1/auth/login` | `{login, password, fingerprint}` → `{access_token, refresh_token}` |
| POST | `/api/v1/auth/refresh` | cookie `refresh_token` → `{access_token, refresh_token}` |
| POST | `/api/v1/auth/logout` | cookie `refresh_token` → `null` |
| GET | `/api/v1/users/me` | → `{email, role, user_profile: {nickname, readed_chapters}}` |
| GET | `/api/v1/users/` | → список `UserResponse` |
| GET | `/api/v1/users/{id}` | → `UserResponse` |
| GET | `/api/v1/users/{id}/profile` | → `{nickname, readed_chapters}` |
| PATCH | `/api/v1/users/{id}/profile` | `{nickname?, readed_chapters?}` → профиль |
| GET | `/api/v1/novel/` | → список `{title, slug, description, type, publish_date, language:{name}, country:{name}}` |
| GET | `/api/v1/novel/{id}` | → `NovelResponse` |
| POST/PATCH/DELETE | `/api/v1/novel/`, `/api/v1/novel/{id}` | CRUD |
| GET | `/api/v1/chapter/` | → список `{title, number, content, is_published}` |
| GET | `/api/v1/chapter/{id}` | → `ChapterResponse` |
| GET/POST/PATCH/DELETE | `/api/v1/category/`, `/api/v1/category/{id}` | → `{name, type}` |
| GET/POST/PATCH/DELETE | `/api/v1/lang/`, `/api/v1/lang/{id}` | → `{name}` |
| GET/POST/PATCH/DELETE | `/api/v1/country/`, `/api/v1/country/{id}` | → `{name}` |
| GET/POST | `/api/v1/teams/` | CRUD команды |
| GET | `/api/v1/teams/{id}/users`, `/api/v1/teams/{id}/novels` | связи команды |

### Разрывы контракта (фронту нужно, бэк пока не отдаёт)

- `NovelResponse` уже содержит `id`, `age_limit`, `status`, `cover_path`, `categories` (добавлено). Ещё не хватает: `rating`, `rating_count`, `team` (переводчики), `reading_progress`, число глав — без них карточки/рейтинг/прогресс пустые.
- `ChapterResponse` не содержит `id`, `novel_id`, `published_at`, `is_read`; `content` — строка, а фронт рендерит массив абзацев.
- Нет эндпоинтов: `/novel/featured`, `/novel/updates`, `/novel/continue-reading`, `/novel/recommendations`, `/novel/{id}/chapters`, `/novel/{id}/comments`, `/auth/profile`.
- Нет сущностей: закладки, комментарии, уведомления, рейтинги, история чтения, статистика профиля/календарь.
- `init_db()` делает `drop_all` на каждый старт и нет сидирования — каталог пуст, пользователей нет (логин невозможен).

---

## 2. Выполнено (этот этап)

- [x] `api/client.js` — разворачивание `data` из обёртки, извлечение `message`/`detail` из ошибок, хранение токена в `localStorage`.
- [x] `api/auth.js` — пути `/api/v1/auth/*`; `fingerprint`; `registerUser` шлёт `nickname/password1/password2` + автологин; `fetchProfile` → `/api/v1/users/me`; `access_token` → токен.
- [x] `api/{novels,chapters,categories,languages,countries,teams,users}.js` — префикс `/api/v1` + единственное число имён ресурсов. Убраны несуществующие эндпоинты (`featured/updates/continue-reading/recommendations/novel/{id}/chapters|comments`).
- [x] `composables/useAuth.js` — `login`/`register`/`logout`/`fetchProfile` на API (async).
- [x] `components/home/AuthModal.vue` — async вход/регистрация, ошибки, убран хардкод демо-логина.
- [x] `api/mapper.js` — `mapNovel` (status→RU, `age_limit`→ageRating, `categories`→genres/tags, `cover_path` только http, устойчивый `id`) и `mapChapter` (`content` строка → массив абзацев, `created_at`→publishedAt, `is_read`).
- [x] `views/CatalogView.vue` — новеллы из `fetchNovels()`; фильтры-опции собраны из `fetchCategories` (жанры/теги), `fetchLanguages` (язык оригинала), `fetchCountries` (язык перевода) + `ageRatings`/`releaseYears` из списка новелл. Без фоллбэка на моки.
- [x] `composables/useNovelPage.js` — новелла из `fetchNovelById(id)`, главы из `fetchChapters()` (фильтр по `novel_id`). Без моков.
- [x] `composables/useChapter.js` — главы и контент из `fetchChapters()`/`fetchChapterById(id)`. Без моков.
- [x] `composables/useTeamPage.js` — команда/участники/новеллы из `fetchTeam/fetchTeamUsers/fetchTeamNovels`. Без моков.
- [x] `api/fallback.js` — удалён.

### Правки бэка (сделаны ранее; дальше бэк трогать не буду)

- [x] `novel/schemas.py` — `NovelResponse`: `id`, `age_limit`, `status`, `cover_path`, `categories`.
- [x] `novel/models.py` — `Novel.categories` → `lazy="selectin"`.
- [x] `chapter/schemas.py` — `ChapterResponse`: `id`, `novel_id`, `created_at`.

---

## 3. Оставшиеся задачи фронтенда (когда бэк дополнит контракт)

- [ ] `views/HomeView.vue` — нет эндпоинтов для `featured/updates/continue-reading/recommendations`; пока моки.
- [ ] `views/BookmarksView.vue`, `views/NotificationsView.vue` — нет эндпоинтов/сущностей (bookmark без роутера, notifications нет); пока моки.
- [ ] `composables/useProfile.js` — статистика/календарь/закладки/комментарии без эндпоинтов; пока мок (никнейм/email уже из `/users/me`).
- [ ] Состояния загрузки/ошибки/пустоты на всех страницах (`AppErrorBoundary`/`AppEmptyState`).
- [ ] `frontend/.env` из `.env.example`; `VITE_API_BASE_URL` для Docker (`backend` внутри сети, `localhost` снаружи).

## 4. Минимум от бэка для «живой» связки

1. CORS (иначе браузер блокирует запросы с 5173 → 8080).
2. Сидирование: пользователь, новеллы, жанры/языки/страны, главы (иначе каталог/главы пустые).

Полный список задач бэка — в `backend/tasks.md` (пишется отдельно).
