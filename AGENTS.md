# AGENTS.md

## Project overview

RanobeDays is a monorepo: Vue 3 frontend (`frontend/`) and Python FastAPI backend (`backend/`), with PostgreSQL (pgvector) via Docker Compose.

## Essential commands

```bash
# Frontend (workdir: frontend/)
npm run dev        # Vite dev server (port 5173, polling enabled for Docker/WSL)
npm run build      # Production build (run before committing UI changes)
npm run format     # Prettier formatting (semi:false, singleQuote, printWidth:100)

# Backend (workdir: backend/)
# Python project managed via uv, config in pyproject.toml

# Full stack
docker compose up  # Starts backend:8080, frontend:5173, db:5432
```

## Architecture

### Frontend stack
- **Vue 3** Composition API (`<script setup>`), no TypeScript — plain `.js` and `.vue` files
- **Vue Router** with two layouts:
  - `AppMainLayout` — header, footer, mobile nav — wraps all routes except chapter reader
  - `ChapterLayout` — minimal wrapper for full-screen reading at `/novel/:id/chapter/:chapterId`
- **Tailwind CSS v4** — uses `@import 'tailwindcss'` (not v3 `@tailwind` directives). Config in `vite.config.js` via `@tailwindcss/vite` plugin
- **No state management library** — singleton composables with module-level `ref()`/`reactive()`
- **No tests yet** — despite CONSTITUTION.md requiring them. Test framework not installed
- **All data is mocked** — composables import from `src/mocks/`, no live API calls
- **Path alias**: `@` → `./src/` (defined in `vite.config.js` and `jsconfig.json`)

### Directory map (frontend/src/)
```
components/
  shared/     — Design system: AppButton, AppInput, AppSelect, AppModal, AppTabs, AppViewModeToggle, AppErrorBoundary, AppEmptyState, FilterGroup
  icons/      — SVG icon components (no size attrs, use Tailwind h-* w-*)
  cards/      — Novel cards (grid, list, bookmark)
  home/       — HomeHeader, MobileBottomNav, UserDropdown, sections, AuthModal
  catalog/    — Catalog layout, toolbar, filters
  bookmarks/  — BookmarksSettingsModal (self-contained, imports useBookmarks directly)
  novel/      — Novel page sidebar, tabs, chapters, meta chips
  chapter/    — ChapterContent, ChapterSettingsPanel
  profile/    — ProfileHeader, ReadingCalendar, ProfileTabs, TeamCard

composables/  — Singleton stores: useAuth, useBookmarks, useProfile, useTheme, useChapter, useChapterSettings, useClickOutside, useDragScroll
views/        — One per route, thin orchestrators
layouts/      — AppMainLayout, ChapterLayout
mocks/        — Static data, imported by composables
router/       — Single file, all routes
constants/    — Shared navLinks
utils/        — validateEmail
```

### Key patterns
- **useClickOutside(rootRef, isOpen, onClose)** — shared composable, used in AppSelect and UserDropdown
- **useDragScroll()** — returns `{ trackRef, isDragging, startDrag, handleTrackClickCapture }`
- **AppTabs** — `v-model:model-value` + `:tabs="[{ key, label, count? }]"`, animated lime indicator
- **AppViewModeToggle** — `v-model` for grid/list, used in 3 places
- **AppSectionSwitchTransition** — Vue `<Transition>` wrapper (opacity + translateY), wrap content with `:key` to animate

### State management (no Pinia!)
- `useAuth()` — module-level `reactive()`, persisted to localStorage. Returns `computed` refs. All components sharing auth call `useAuth()` directly — no prop drilling needed
- `useProfile()` — reads user from `useAuth()`, adds profile-specific data (stats, calendar). Mutations delegate to `useAuth().updateUser()`
- `useBookmarks()` — CRUD for bookmark categories. `BookmarksSettingsModal` imports it directly
- `useTheme()` — `isDark`/`toggleTheme`, sets `data-theme` on `<html>`, localStorage
- `useChapterSettings()` — font/size/bg/width, persisted to localStorage

### CSS/theme
- **Dark mode is default** — `:root` is dark. Light mode via `[data-theme='light']`
- **Light theme uses `!important` overrides** — attribute selectors like `[class*='text-lime-200']` in `main.css`. When adding new accent colors, add matching light-theme rules or text will be invisible
- **Fonts loaded via `<link>` in index.html** — `subset=cyrillic,latin` required for all fonts. `_fonts.css` is empty (was previously used for `@import`)
- **`.card-interactive`** CSS utility — replaces `hover:bg-zinc-800/70 active:scale-[0.99]` across cards

### Routes (order matters!)
```
/novel/:id/chapter/:chapterId  → ChapterLayout → ChapterView  (outside AppMainLayout)
/                              → AppMainLayout → HomeView
/catalog                       → CatalogView
/bookmarks                     → BookmarksView
/novel/:id                     → NovelView
/profile                       → ProfileView
/notifications                 → NotificationsView
```
Chapter route is first and separate — it renders full-screen without header/footer.

### Frontend gotchas
- **Vite polling** required for Docker/WSL: `server.watch.usePolling: true`
- **Prettier only** — no ESLint. Run `npm run format` before commits
- **Pre-commit hooks are Python-focused** (ruff, codespell) — no frontend linting in CI
- **`.env.example`** exists but no `.env` validation at startup — just a console.warn
- **Chapter data in `chapterData.js`** — uses `getNovelById` from `novelPageData.js` as fallback for novels without custom text. `getChapters(novelId)` returns chapters for ALL novels in catalog
- **Bookmark items** use BOTH `items` (in useBookmarks) and `novels` (in useProfile) — check both when accessing
- **Functions as props are anti-pattern** — prefer direct composable import (like `BookmarksSettingsModal` does)

### Backend
- Python FastAPI, Dockerfile, pyproject.toml with uv
- PostgreSQL with pgvector extension
- `.env` file exists (gitignored), environment in docker-compose
