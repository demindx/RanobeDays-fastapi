import { describe, expect, it, vi } from 'vitest'
import { reactive } from 'vue'
import { mount, RouterLinkStub } from '@vue/test-utils'

const routeState = reactive({ path: '/' })

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    useRoute: () => routeState,
  }
})

import HeaderMobileNav from './HeaderMobileNav.vue'

const mountNav = (props = {}) =>
  mount(HeaderMobileNav, {
    props: {
      isLoggedIn: true,
      hasNotifications: true,
      userInitials: 'A',
      ...props,
    },
    global: {
      stubs: {
        RouterLink: RouterLinkStub,
      },
    },
  })

describe('HeaderMobileNav', () => {
  it('sets aria-current on active route', () => {
    routeState.path = '/catalog'
    const wrapper = mountNav()

    const links = wrapper.findAllComponents(RouterLinkStub)
    const catalog = links.find((link) => link.props('to') === '/catalog')
    const favorites = links.find((link) => link.props('to') === '/top')

    expect(catalog).toBeTruthy()
    expect(catalog.attributes('aria-current')).toBe('page')
    expect(favorites.attributes('aria-current')).toBeUndefined()
  })

  it('marks login route as current for guest nav item', () => {
    routeState.path = '/login'
    const wrapper = mountNav({ isLoggedIn: false })

    const links = wrapper.findAllComponents(RouterLinkStub)
    const login = links.find((link) => link.props('to') === '/login')

    expect(login).toBeTruthy()
    expect(login.attributes('aria-current')).toBe('page')
  })
})
