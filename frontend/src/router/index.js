import { createRouter, createWebHistory } from 'vue-router'
import AppMainLayout from '../layouts/AppMainLayout.vue'
import ChapterLayout from '../layouts/ChapterLayout.vue'
import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import BookmarksView from '../views/BookmarksView.vue'
import NovelView from '../views/NovelView.vue'
import ChapterView from '../views/ChapterView.vue'
import ProfileView from '../views/ProfileView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import TeamView from '../views/TeamView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/novel/:id/chapter/:chapterId',
      component: ChapterLayout,
      children: [
        {
          path: '',
          name: 'chapter',
          component: ChapterView,
        },
      ],
    },
    {
      path: '/',
      component: AppMainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: 'catalog',
          name: 'catalog',
          component: CatalogView,
        },
        {
          path: 'bookmarks',
          name: 'bookmarks',
          component: BookmarksView,
        },
        {
          path: 'novel/:id',
          name: 'novel',
          component: NovelView,
        },
        {
          path: 'profile',
          name: 'profile',
          component: ProfileView,
        },
        {
          path: 'notifications',
          name: 'notifications',
          component: NotificationsView,
        },
        {
          path: 'team/:id',
          name: 'team',
          component: TeamView,
        },
      ],
    },
  ],
})

export default router
