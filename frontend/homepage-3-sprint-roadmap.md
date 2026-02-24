# Homepage Roadmap (3 Sprints)

## Context
- Product: главная страница RanobeDays.
- Goal: сделать главную полезной для возвратного чтения, свежих обновлений и навигации по контенту.
- Reference patterns: ReManga / MangaLib (лента обновлений, топы, персональный входной экран).

## Common Principles
- Mobile-first layout, затем desktop enhancement.
- Одинаковая высота карточек внутри одной секции.
- Каждая секция имеет отдельные состояния: `loading` / `empty` / `error`.
- Не блокировать весь экран одним большим `loading`.
- Все ключевые действия доступны клавиатурой и через screen reader.

---

## Sprint 1: Core Homepage Utility

### 1. Objectives
- Сделать главную функциональной с первого экрана.
- Дать пользователю быстрый путь к чтению и свежим обновлениям.
- Стабилизировать структуру секций и API-контракт для главной.

### 2. Scope
1. Hero-секция “Продолжить чтение”.
2. Секция “Новые главы сегодня”.
3. Секция “Последние обновления” (лента).
4. Базовые skeleton/loading/empty/error состояния для каждой секции.
5. Базовые e2e проверки доступности и адаптива этих секций.

### 3. Functional Tasks
1. Create `HomeSectionContinueReading`:
- карточка: `cover`, `title`, `lastReadChapter`, `progress`, CTA `Продолжить`.
- если пользователь не авторизован: компактный onboarding-block с CTA `Войти`.

2. Create `HomeSectionNewChapters`:
- горизонтальная карусель карточек.
- бейдж `NEW` для тайтлов с первым обновлением за 24 часа.

3. Create `HomeSectionLatestUpdates`:
- вертикальная лента: `title`, `chapter`, `updatedAt`, `bookmarkStatus`.
- действие: `Открыть главу`.

4. Data contract (frontend):
- `GET /home/continue-reading`
- `GET /home/new-chapters?period=today`
- `GET /home/latest-updates?limit=...`
- на этапе интеграции допустим fallback на mock adapter.

5. UX states:
- skeleton на каждую секцию.
- empty-state тексты и CTA.
- retry action при `error`.

### 4. Technical Tasks
1. Выделить composables:
- `useHomeContinueReading`
- `useHomeNewChapters`
- `useHomeLatestUpdates`

2. Нормализовать domain-модели:
- `HomeContinueItem`
- `HomeUpdateItem`
- `HomeNewChapterItem`

3. Пересобрать `HomeView` как композицию секций (без монолита).

4. Добавить telemetry events:
- `home_continue_click`
- `home_latest_update_click`
- `home_new_chapter_click`

### 5. QA / DoD
1. На мобильном (320/360/390) нет горизонтального скролла.
2. Все CTA доступны с клавиатуры (`Tab`, `Enter`).
3. Секции не прыгают по высоте на загрузке.
4. `lint`, unit tests, smoke e2e, adaptivity e2e проходят.

### 6. Metrics to Track
- CTR по “Продолжить чтение”.
- Доля сессий с кликом по “Последние обновления”.
- Time-to-first-action на главной.

### 7. Risks
- Неполные backend-данные для прогресса чтения.
- Перегруженный first-screen на мобилке.

---

## Sprint 2: Discovery & Ranking (without Collections)

### 1. Objectives
- Улучшить поиск контента прямо на главной.
- Добавить понятные рейтинговые блоки и быстрые фильтры.
- Убрать “подборки” из объема спринта.

### 2. Scope
1. Быстрые фильтры-чипы над лентой.
2. Секция “Топы” с периодами: `день / неделя / месяц`.
3. Расширенная секция “Горячие новинки” (за 7 дней).
4. Улучшенная навигация между секциями по якорям (desktop) / tab chips (mobile).
5. Подборки (`collections`) не включать.

### 3. Functional Tasks
1. Quick filters:
- фильтры: `жанр`, `страна`, `статус`, `год`, `рейтинг`.
- состояние фильтров синхронизировать с URL query.

2. Top block:
- переключатель периода (`day/week/month`).
- единый компонент ranking card с номером позиции.

3. Hot releases:
- отдельный блок с сортировкой по росту активности/просмотров за 7 дней.
- бейджи динамики: `+N%` или `в тренде`.

4. Navigation aids:
- sticky mini-nav по секциям на desktop.
- swipeable chip-nav на mobile.

### 4. Technical Tasks
1. `useHomeFilters` composable:
- query sync, reset, persist in session storage.

2. Ranking service adapter:
- `GET /home/top?period=day|week|month`
- `GET /home/hot?window=7d`

3. Performance:
- lazy-render нижних секций через intersection observer.
- оптимизация изображений (размеры, `srcset`, `loading=lazy`).

### 5. QA / DoD
1. Фильтры корректно сериализуются в URL и восстанавливаются после reload.
2. Переключение периода топа не вызывает layout shift.
3. Mobile UX: чипы фильтров прокручиваются, не ломают контейнер.
4. Нет регрессии по доступности в новых контролах.

### 6. Metrics to Track
- CTR по блоку “Топ”.
- Использование фильтров (% сессий с >=1 фильтром).
- Глубина просмотра после клика из “Горячих новинок”.

### 7. Risks
- Сложный query-state может конфликтовать с существующим поиском.
- Перегрузка интерфейса фильтрами на маленьких экранах.

---

## Sprint 3: Personalization, Content Freshness, Polish

### 1. Objectives
- Сделать главную “живой” и персональной.
- Повысить возвратность и частоту целевых действий.
- Завершить polish производительности и UX.

### 2. Scope
1. Секция “Для вас” (персональные рекомендации).
2. Блок “Новости и анонсы” (1-3 карточки).
3. Улучшение возвратного UX: сохранение позиции/состояния.
4. Lighthouse/performance pass и финальная UX-дошлифовка.

### 3. Functional Tasks
1. Personalized feed:
- рекомендации на основе закладок, последних открытий, жанров.
- fallback на “популярное” при холодном старте.

2. News/Announcements:
- компактные карточки с датой, заголовком, ссылкой.
- ограничение длины текста и единая высота карточек.

3. Return flow:
- restore scroll position при back navigation.
- restore active filters/chips и открытого периода топа.

4. Optional moved from previous backlog:
- editorial/user collections only if есть свободная емкость.

### 4. Technical Tasks
1. `useHomePersonalization` composable с graceful fallback.
2. Кеширование данных секций (stale-while-revalidate).
3. Аналитика:
- `home_reco_click`
- `home_news_click`
- `home_returned_session_engaged`

4. Perf budget hardening:
- уменьшить JS/CSS для Home critical path.
- deferring non-critical scripts/components.

### 5. QA / DoD
1. Поведение главной детерминировано после back/reload.
2. Lighthouse mobile: performance >= 88, accessibility >= 95.
3. Нет заметных CLS-прыжков в основных секциях.
4. Полный прогон: lint + unit + e2e smoke + adaptivity + lighthouse.

### 6. Metrics to Track
- Return user engagement rate.
- CTR персональных рекомендаций.
- Session depth from homepage.
- Доля “быстрых уходов” без целевого действия.

### 7. Risks
- Качество персонализации при низком объеме пользовательских данных.
- Риск усложнения главной без четкой приоритизации секций.

---

## Suggested Delivery Cadence
1. Sprint 1: 2 недели.
2. Sprint 2: 2 недели.
3. Sprint 3: 2 недели.

## Release Gates Per Sprint
1. Feature flag for new sections.
2. Canary rollout to small user cohort.
3. Metrics check after 48-72h.
4. Full rollout only if KPI baseline is stable.
