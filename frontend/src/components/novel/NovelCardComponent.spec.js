import { describe, expect, it } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import NovelCardComponent from './NovelCardComponent.vue'

describe('NovelCardComponent', () => {
  const baseProps = {
    title: 'Solo Leveling',
    country: 'KR',
    slug: 'solo-leveling',
    imageSrc: 'https://example.com/cover.jpg',
  }

  it('renders link to novel detail page', () => {
    const wrapper = mount(NovelCardComponent, {
      props: baseProps,
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const link = wrapper.findComponent(RouterLinkStub)
    expect(link.exists()).toBe(true)
    expect(link.props('to')).toBe('/novel/solo-leveling')
  })

  it('removes skeleton and marks image as loaded on load event', async () => {
    const wrapper = mount(NovelCardComponent, {
      props: baseProps,
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    expect(wrapper.find('.novel-card__skeleton').exists()).toBe(true)

    const image = wrapper.find('img')
    await image.trigger('load')

    expect(wrapper.find('.novel-card__skeleton').exists()).toBe(false)
    expect(image.classes()).toContain('novel-card__image--loaded')
  })

  it('falls back to placeholder image on error', async () => {
    const wrapper = mount(NovelCardComponent, {
      props: baseProps,
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const image = wrapper.find('img')
    await image.trigger('error')

    expect(image.attributes('src')).toContain('data:image/svg+xml')
    expect(wrapper.find('.novel-card__skeleton').exists()).toBe(false)
  })

  it('renders bookmark status badge when status provided', () => {
    const wrapper = mount(NovelCardComponent, {
      props: {
        ...baseProps,
        bookmarkStatus: 'Читаю',
      },
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const badge = wrapper.find('.novel-card__bookmark-badge')
    expect(badge.exists()).toBe(true)
    expect(badge.text()).toBe('Читаю')
  })
})
