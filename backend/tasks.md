# Backend Tasks: Full Frontend Integration

## 1. Bookmarks (New Entity)

### 1.1 Database Models
- [ ] Create `BookmarkCategory` model: `id` (PK), `user_id` (FK→users, CASCADE), `name`, `is_public`, `order`
- [ ] Create `BookmarkItem` model: `id` (PK), `category_id` (FK→bookmark_categories, CASCADE), `novel_id` (FK→novels), `added_at`

### 1.2 Pydantic Schemas
- [ ] `BookmarkCategoryCreate`: `name` (str), `is_public` (bool, default true)
- [ ] `BookmarkCategoryUpdate`: `name` (optional), `is_public` (optional), `order` (optional)
- [ ] `BookmarkCategoryResponse`: `id`, `name`, `is_public`, `order`, `items: list[BookmarkItemResponse]`
- [ ] `BookmarkItemCreate`: `novel_id` (int)
- [ ] `BookmarkItemResponse`: `id`, `novel_id`, `title`, `author`, `cover_url`, `cover_style`, `rating`, `added_at`

### 1.3 Repository / Service
- [ ] Create `BookmarkRepository` (extends PostgresRepository)
- [ ] Create `BookmarkService` with: get_all(user_id), create(user_id, data), rename(id, user_id, name), toggle_privacy(id, user_id), reorder(user_id, ordered_ids), add_item(category_id, user_id, novel_id), remove_item(item_id, user_id)

### 1.4 Router (`/api/bookmarks`)
- [ ] `GET /bookmarks` — all categories with items for current user
- [ ] `POST /bookmarks` — create category
- [ ] `PATCH /bookmarks/{id}` — rename category
- [ ] `PATCH /bookmarks/{id}/privacy` — toggle public/private
- [ ] `PATCH /bookmarks/reorder` — reorder categories
- [ ] `POST /bookmarks/{id}/items` — add novel to bookmark
- [ ] `DELETE /bookmarks/{id}/items/{item_id}` — remove novel from bookmark

---

## 2. Comments (New Entity)

### 2.1 Database Model
- [ ] Create `Comment` model: `id` (PK), `user_id` (FK→users, CASCADE), `novel_id` (FK→novels, CASCADE), `text`, `created_at`

### 2.2 Pydantic Schemas
- [ ] `CommentCreate`: `text` (str)
- [ ] `CommentResponse`: `id`, `author` (nickname), `text`, `time_ago` (computed), `date`, `likes`, `novel_id`, `novel_title`

### 2.3 Repository / Service
- [ ] Create `CommentRepository`
- [ ] Create `CommentService` with: get_by_novel(novel_id, page, limit), create(user_id, novel_id, text), get_by_user(user_id, page, limit)

### 2.4 Router
- [ ] `GET /novels/{id}/comments?page=&limit=` — paginated comments for novel
- [ ] `POST /novels/{id}/comments` — add comment (auth required)
- [ ] `GET /users/me/comments?page=&limit=` — user comment history

---

## 3. Notifications (New Entity)

### 3.1 Database Model
- [ ] Create `Notification` model: `id` (PK), `user_id` (FK→users, CASCADE), `type` (enum: free_chapter, paid_chapter, system), `title`, `text`, `is_read` (default false), `metadata` (JSON: novel_id, chapter, price, etc.), `created_at`

### 3.2 Pydantic Schemas
- [ ] `NotificationResponse`: `id`, `type`, `title`, `text`, `is_read`, `time_ago` (computed), `metadata`

### 3.3 Repository / Service
- [ ] Create `NotificationRepository`
- [ ] Create `NotificationService` with: get_all(user_id, type_filter), mark_read(notification_id, user_id), mark_all_read(user_id)

### 3.4 Router (`/api/notifications`)
- [ ] `GET /notifications?type=free|paid|system` — all notifications for user (auth required)
- [ ] `PATCH /notifications/{id}/read` — mark single as read
- [ ] `PATCH /notifications/read-all` — mark all as read

---

## 4. Ratings (New Entity)

### 4.1 Database Model
- [ ] Create `NovelRating` model: `user_id` (FK→users, CASCADE), `novel_id` (FK→novels, CASCADE), `rating` (int, 1-5), unique constraint on (user_id, novel_id)

### 4.2 Pydantic Schemas
- [ ] `RatingSubmit`: `rating` (int, 1-5)
- [ ] `RatingResponse`: `rating` (int)

### 4.3 Service additions
- [ ] Add `get_average_rating(novel_id)` to NovelService
- [ ] Add `get_user_rating(user_id, novel_id)` to NovelService
- [ ] Add `set_rating(user_id, novel_id, rating)` to NovelService (upsert)

### 4.4 Router additions (`/api/novels`)
- [ ] `POST /novels/{id}/rating` — rate novel (auth required)
- [ ] `GET /novels/{id}/rating` — get current user's rating (auth required)
- [ ] Add `rating` (float) and `rating_count` (int) to `NovelResponse`

---

## 5. Reading History & Progress (New Entity)

### 5.1 Database Models
- [ ] Create `ReadingHistory` model: `id` (PK), `user_id` (FK→users, CASCADE), `novel_id` (FK→novels, CASCADE), `chapter_id` (FK→chapters, CASCADE), `read_at` (timestamp), unique constraint on (user_id, novel_id, chapter_id)

### 5.2 Service
- [ ] Create `ReadingService` with:
  - `mark_read(user_id, novel_id, chapter_id)` — record read chapter
  - `get_continue_reading(user_id)` — novels with progress < 100%
  - `get_calendar(user_id, year, month)` — daily read counts per day
  - `get_progress(user_id, novel_id)` — percent + last chapter

### 5.3 Router additions
- [ ] `POST /novels/{novel_id}/chapters/{chapter_id}/mark-read` — mark chapter read (auth)
- [ ] `GET /users/me/continue-reading` — continue reading list
- [ ] `GET /users/me/calendar?year=&month=` — reading activity calendar
- [ ] Add `reading_progress` (int, 0-100) to `NovelResponse` when user is authenticated

---

## 6. User Profile — Expansion

### 6.1 Database
- [ ] Extend `UserProfile` model: add `avatar_url` (str, nullable), `joined_at` (datetime, default now), `settings` (JSONB: `blacklisted_genres`, `blacklisted_tags`, `hide_adult_content`)
- [ ] Migration for new columns

### 6.2 Pydantic Schemas
- [ ] `UserSettingsUpdate`: `blacklisted_genres` (optional), `blacklisted_tags` (optional), `hide_adult_content` (optional)
- [ ] `UserPasswordUpdate`: `old_password` (str), `new_password` (str)
- [ ] Extend `UserProfileResponse`: add `avatar_url`, `joined_at`, `settings`, `teams` (list), stats fields (see 6.3)

### 6.3 Computed stats in UserProfileResponse
- [ ] `chapters_read` — count from ReadingHistory
- [ ] `novels_completed` — count novels where reading_progress = 100%
- [ ] `reading_hours` — estimate based on chapter count (e.g., chapters_read * 0.25)
- [ ] `streak_days` — consecutive days with at least 1 read chapter
- [ ] `bookmarks_count` — count of BookmarkCategory for user
- [ ] `comments_count` — count of Comment for user

### 6.4 Router additions (`/api/users`)
- [ ] `PATCH /users/me/password` — change password (auth required)
- [ ] `PATCH /users/me/settings` — update content filter settings (auth)
- [ ] `POST /users/me/avatar` — upload avatar file (auth, multipart)
- [ ] `GET /users/{id}/bookmarks` — user's public bookmark categories (was in profile, keep it here)

---

## 7. Novels — Endpoint Expansion

### 7.1 Filtered listing
- [ ] Upgrade `GET /novels/` with query parameters: `search`, `genres` (comma-separated), `tags`, `age_rating`, `status`, `year_from`, `year_to`, `original_language`, `translation_language`, `page`, `limit`
- [ ] Implement server-side filtering in `NovelRepository`

### 7.2 New endpoints in `novel/` router
- [ ] `GET /novels/featured` — top-rated / editor-picked novels (limit query param)
- [ ] `GET /novels/updates` — latest chapter updates across all novels
- [ ] `GET /novels/recommendations` — personalized recommendations (genre overlap or pgvector embedding similarity)
- [ ] `GET /novels/{id}/chapters` — chapters list (move from standalone chapter router)
- [ ] `GET /novels/{id}/chapters/{chapter_id}` — single chapter content (move from standalone)

### 7.3 Catalog filters
- [ ] Add `GET /catalog/filters` — returns available filter options: `release_years`, `age_ratings`, `genres`, `tags`, `original_languages`, `translation_languages` (aggregated from DB)

---

## 8. Chapters — Refinements

### 8.1 Response format
- [ ] Ensure `GET /novels/{id}/chapters` returns: `[{id, number, title, published_at, is_read}]`
- [ ] Ensure `GET /novels/{id}/chapters/{chapter_id}` returns: `{id, number, title, published_at, content: string[]}`
- [ ] `content` should be a list of paragraphs (split by `\n\n` or stored as JSON array)

### 8.2 Read status
- [ ] Add `is_read` boolean flag to chapter list response when user is authenticated (join with ReadingHistory)

---

## 9. Authentication — Fixes & Additions

### 9.1 Alias endpoint
- [ ] Add `GET /auth/profile` as alias for `GET /users/me` (frontend `fetchProfile()` expects this path)

### 9.2 Login fixes
- [ ] Fix `POST /auth/login`: validate that at least one of `login` / `email` is provided
- [ ] Make `fingerprint` optional in `UserLogin` schema (frontend doesn't send it)

### 9.3 Registration
- [ ] Ensure `POST /auth/register` maps from frontend `registerUser(login, email, password)`: reuse `login` as `nickname`, hash password → store

---

## 10. Integration Alignment (Frontend ↔ Backend)

### 10.1 URL prefix sync
- [ ] Change backend API prefix from `/api/v1/` to `/api/` — OR — update frontend `src/api/` modules to use `/api/v1/`
  - **Decision needed**: which side to change. Frontend has `fetchJson` calls to `/api/auth/*`, `/api/novels/`, etc.

### 10.2 Resource name sync
- [ ] Rename routers: `/novel` → `/novels`, `/chapter` → `/chapters`, `/lang` → `/languages`, `/country` → `/countries` — OR — update frontend paths
  - **Decision needed**: which side to change

### 10.3 Response format
- [ ] Backend wraps everything in `GenericResponse { code, message, data }`. Frontend `fetchJson()` may need an unwrap layer.
- [ ] Check if frontend `src/api/fetchJson` handles the envelope, or adapt.

### 10.4 Novel response fields
- [ ] Add `translators` field to `NovelResponse` (list of team names translating the novel)
- [ ] Add `cover_url` field — serve `cover_path` as full URL (add `/static/` or S3 URL)
- [ ] Flatten `language` / `country` from nested objects to strings: `{language: {name: "Китайский"}}` → `{original_language: "Китайский"}`
  - **Decision needed**: flatten on backend side, or adapt frontend `mapNovel()` mapper

### 10.5 Genres/Tags flattening
- [ ] Frontend expects separate `genres: []` and `tags: []` arrays. Backend uses unified `categories` with `type` discriminator.
- [ ] Add computed fields or transform in router: filter categories by `type="genre"` → `genres`, `type="tag"` → `tags`

---

## 11. Critical Bugs

### 11.1 Missing `await`
- [ ] Fix `GET /novel/{id}` router — `service.get_by_id(id)` is not awaited (returns coroutine, not result)
- [ ] Fix `GET /chapter/{id}` router — same missing `await`

### 11.2 Wrong base class
- [ ] Fix `Category` model: inherits from `Base["ChapterCreate"]` → should be `Base["CategoryCreate"]`

### 11.3 Database reset on startup
- [ ] Remove `await conn.run_sync(Base.metadata.drop_all)` from `init_db()` — destroys all data on every restart
- [ ] Replace with Alembic migrations or conditional drop (e.g., only in DEV with `RESET_DB=true` env flag)

---

## 12. Authorization Coverage

### 12.1 Protect mutating endpoints
- [ ] Add `CurrentUser` dependency to all POST/PATCH/DELETE endpoints:
  - Novels: create, update, delete
  - Chapters: create, update, delete
  - Categories: create, update, delete
  - Teams: create, update, delete
  - Languages, Countries: create, delete

### 12.2 Admin-only endpoints
- [ ] Wire `get_admin_user` dependency for: category CRUD, language CRUD, country CRUD, novel approval

---

## Task Priority Summary

| Priority | Domains | Why |
|----------|---------|-----|
| **P0 — Critical** | 11 (Bugs) | Broken endpoints, data loss on restart |
| **P1 — High** | 9 (Auth), 12 (Authorization) | Security, auth flow correctness |
| **P2 — High** | 7 (Novels), 8 (Chapters) | Core reading functionality |
| **P3 — Medium** | 1 (Bookmarks), 4 (Ratings) | Key user features |
| **P4 — Medium** | 2 (Comments), 5 (Reading History) | Social + tracking features |
| **P5 — Medium** | 6 (User Profile), 10 (Integration) | Profile completeness, frontend sync |
| **P6 — Lower** | 3 (Notifications) | Can be added after core is stable |
