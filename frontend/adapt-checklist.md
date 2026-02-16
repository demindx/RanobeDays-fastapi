# Адаптивный чек-лист

## Брейкпоинты
- [x] 320x568
- [x] 360x800
- [x] 390x844
- [x] 768x1024
- [x] 1024x1366
- [x] 1280+

## Страницы
- [x] `HomeView` без горизонтального скролла
- [x] `CatalogView` без горизонтального скролла
- [x] `NovelDetailView` без горизонтального скролла

## Компоненты и зоны риска
- [x] Mobile header: корректный safe-area сверху
- [x] Bottom mobile nav: корректный safe-area снизу
- [x] Основной контент (`main`) не перекрывается фиксированными панелями
- [x] Блок "Пример полей" на мобильном в 1 колонку, без обрезаний
- [x] `DropdownSelectField` и `TagDropdownSelector` не дают горизонтального переполнения
- [x] Бейджи статуса в `NovelDetailCard` и `NovelCompactCard` не выходят за карточку
- [x] Карусель: drag/touch работает, скролл колесиком/тачпадом работает на desktop

## Что уже подтверждено автоматически
- `bun run lint` для затронутых файлов
- `bun run test -- src/components/novel/NovelPosterCard.spec.js src/components/novel/NovelDetailCard.spec.js`
- `bun run test:e2e -- e2e/adaptivity-check.spec.js`

## Примечание
Полуавтоматическая визуальная проверка выполнена через Playwright (Chromium) на указанных брейкпоинтах.
