import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ref, nextTick } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import { mount, RouterLinkStub } from '@vue/test-utils'

const routerPush = vi.fn()
const searchSpy = vi.fn()

const mockUseRouter = vi.fn(() => ({
  push: routerPush,
}))

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useRouter: () => mockUseRouter(),
  }
})

vi.mock('@/composables/useSearch', () => ({
  useSearch: () => ({
    query: ref(''),
    search: searchSpy,
  }),
}))

import Header from './Header.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import HeaderUserControls from '@/components/layout/HeaderUserControls.vue'
import HeaderMobileNav from '@/components/layout/HeaderMobileNav.vue'
import { useAppStore } from '@/stores/app'

const mountHeader = () =>
  mount(Header, {
    global: {
      mocks: {
        $route: {
          path: '/',
        },
      },
      stubs: {
        RouterLink: RouterLinkStub,
      },
    },
  })

describe('Header', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    routerPush.mockReset()
    searchSpy.mockReset()
  })

  it('calls useSearch.search when SearchBar emits search', async () => {
    const wrapper = mountHeader()

    const searchBar = wrapper.findComponent(SearchBar)
    searchBar.vm.$emit('search', 'overlord')
    await nextTick()

    expect(searchSpy).toHaveBeenCalledWith('overlord')
  })

  it('logs in through store when HeaderUserControls emits login', async () => {
    const store = useAppStore()
    store.logout()

    const wrapper = mountHeader()
    const controls = wrapper.findComponent(HeaderUserControls)

    controls.vm.$emit('login')
    await nextTick()

    expect(store.isLoggedIn).toBe(true)
  })

  it('navigates to favorites when HeaderUserControls emits book-click', async () => {
    const wrapper = mountHeader()
    const controls = wrapper.findComponent(HeaderUserControls)

    controls.vm.$emit('book-click')
    await nextTick()

    expect(routerPush).toHaveBeenCalledWith('/favorites')
  })

  it('marks notifications as read from desktop and mobile controls', async () => {
    const store = useAppStore()
    store.hasNotifications = true

    const wrapper = mountHeader()

    const desktopControls = wrapper.findComponent(HeaderUserControls)
    const mobileNav = wrapper.findComponent(HeaderMobileNav)

    desktopControls.vm.$emit('notifications-click')
    await nextTick()
    expect(store.hasNotifications).toBe(false)

    store.hasNotifications = true
    mobileNav.vm.$emit('notifications-click')
    await nextTick()
    expect(store.hasNotifications).toBe(false)
  })

  it('hides mobile header on downward scroll after threshold', async () => {
    const wrapper = mountHeader()
    const stickyHeader = wrapper.find('header > div')

    Object.defineProperty(window, 'scrollY', {
      value: 120,
      configurable: true,
      writable: true,
    })

    window.dispatchEvent(new Event('scroll'))
    await nextTick()

    expect(stickyHeader.classes()).toContain('-translate-y-full')

    window.scrollY = 20
    window.dispatchEvent(new Event('scroll'))
    await nextTick()

    expect(stickyHeader.classes()).not.toContain('-translate-y-full')
  })
})
