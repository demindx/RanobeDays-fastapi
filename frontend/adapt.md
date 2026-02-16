# План исправления адаптивности фронтенда

## Что проверено
Проведен статический аудит основных страниц и компонентов:
- `frontend/src/views/HomeView.vue`
- `frontend/src/views/CatalogView.vue`
- `frontend/src/components/layout/Header.vue`
- `frontend/src/components/layout/HeaderMobileNav.vue`
- `frontend/src/components/novel/NovelHeroCarousel.vue`
- `frontend/src/components/novel/NovelPosterCard.vue`
- `frontend/src/components/novel/NovelDetailCard.vue`
- `frontend/src/components/novel/NovelCompactCard.vue`
- `frontend/src/components/common/TextInputField.vue`
- `frontend/src/components/common/DropdownSelectField.vue`
- `frontend/src/components/common/TagDropdownSelector.vue`

## Ключевые наблюдения
1. Есть фиксированные размеры в карточках и формах (`px`), что может ухудшать поведение на узких экранах.
2. У полей формы дефолтная ширина `229px`, из-за чего блок «Пример полей» может смотреться перегруженно на мобилке.
3. В `CatalogView` строка с заголовком и поисковым запросом (`justify-between`) при длинном запросе может ломать перенос.
4. Карусель и карточки уже имеют базовую адаптацию, но нет единого «контракта размеров» для компонентной системы.
5. Для фиксированного mobile-header и bottom-nav не заложены safe-area отступы (`env(safe-area-inset-*)`) для устройств с вырезами.

## Приоритетный план работ

### Этап 1. Быстрые фиксы (высокий приоритет)
1. Нормализовать адаптивную ширину полей формы.
Файлы:
- `frontend/src/components/common/TextInputField.vue`
- `frontend/src/components/common/DropdownSelectField.vue`
- `frontend/src/components/common/TagDropdownSelector.vue`
- `frontend/src/views/HomeView.vue`
Действия:
- заменить жесткое поведение `width: 229px` на мобильный режим `width: 100%` (через проп или media rule);
- для демо-блока в `HomeView` включить `w-full sm:w-auto` и адекватные `min-width`.

2. Исправить поведение шапки каталога при длинном поисковом запросе.
Файл:
- `frontend/src/views/CatalogView.vue`
Действия:
- на маленьких экранах переключать контейнер в `flex-col items-start`;
- добавить перенос строки/ограничение длины для текста запроса (`break-words`, `max-w`, `truncate` по дизайну).

3. Добавить safe-area для мобильных фиксированных панелей.
Файлы:
- `frontend/src/components/layout/Header.vue`
- `frontend/src/components/layout/HeaderMobileNav.vue`
- `frontend/src/App.vue`
Действия:
- добавить `padding-top: env(safe-area-inset-top)` для mobile header;
- добавить `padding-bottom: env(safe-area-inset-bottom)` для нижней навигации;
- синхронизировать отступы `main` (`pt/pb`) под новую фактическую высоту.

### Этап 2. Унификация размеров компонентов (средний приоритет)
4. Ввести scale-токены размеров карточек (S/M/L) и применить их в Novel-компонентах.
Файлы:
- `frontend/src/components/novel/NovelPosterCard.vue`
- `frontend/src/components/novel/NovelDetailCard.vue`
- `frontend/src/components/novel/NovelCompactCard.vue`
- `frontend/src/assets/_variables.css`
Действия:
- вынести повторяющиеся размеры (`width`, `height`, `min-height`, `padding`, `font-size`) в CSS-переменные;
- зафиксировать единое поведение на брейкпоинтах `<=767`, `768-1023`, `>=1024`.

5. Снизить риск горизонтального скролла в длинных подписях и бейджах.
Файлы:
- `frontend/src/components/novel/NovelDetailCard.vue`
- `frontend/src/components/novel/NovelCompactCard.vue`
- `frontend/src/components/common/TagDropdownSelector.vue`
Действия:
- перепроверить ограничения `max-width`, `white-space`, `text-overflow`;
- для длинных текстов в бейджах применить единый паттерн обрезки и min/max ширины.

### Этап 3. Контроль качества адаптива (средний приоритет)
6. Создать чек-лист визуального регресса по брейкпоинтам.
Брейкпоинты:
- 320x568
- 360x800
- 390x844
- 768x1024
- 1024x1366
- 1280+
Действия:
- проверить отсутствие горизонтального скролла на страницах `Home`, `Catalog`, `NovelDetail`;
- проверить кликабельность и фокус-стили в хедере, мобильной навигации, карусели и формах;
- проверить работу колесика/тачпада в карусели на desktop + touch drag на mobile.

## Критерии готовности
1. На ширинах 320-430px нет горизонтального скролла страницы.
2. Все form controls корректно встают в 1 колонку и не обрезаются.
3. Mobile header и bottom-nav не конфликтуют с safe-area и контентом.
4. Карточки Novel выглядят консистентно и масштабируются по единой схеме размеров.
5. `bun run lint` и целевые `vitest`-тесты проходят после правок.

## Порядок внедрения
1. Этап 1 полностью.
2. Этап 2 (после визуальной проверки Этапа 1).
3. Этап 3 + фиксация результатов (скриншоты/чек-лист).

## Статус выполнения
1. Этап 1: выполнен.
2. Этап 2: выполнен.
3. Этап 3: чек-лист создан в `frontend/adapt-checklist.md`.
4. Автопроверки: `bun run lint` (целевые файлы) и `bun run test -- src/components/novel/NovelPosterCard.spec.js src/components/novel/NovelDetailCard.spec.js` пройдены.
