import { createRouter, createWebHistory } from 'vue-router'
import AppMainLayout from '../layouts/AppMainLayout.vue'
import HomeView from '../views/HomeView.vue'
import CatalogView from '../views/CatalogView.vue'
import BookmarksView from '../views/BookmarksView.vue'
import NovelView from '../views/NovelView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      ],
    },
  ],
})

export default router
