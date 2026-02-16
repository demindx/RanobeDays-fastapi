import { describe, expect, it } from 'vitest'
import { mount, RouterLinkStub } from '@vue/test-utils'
import NovelDetailCard from './NovelDetailCard.vue'

describe('NovelDetailCard', () => {
  const baseProps = {
    title: 'Re:Zero',
    description: 'A fantasy story',
    imageSrc: 'https://example.com/cover.jpg',
    tags: [
      { id: 1, name: 'Isekai' },
      { id: 2, name: 'Drama' },
    ],
  }

  it('renders router-link when slug is provided', () => {
    const wrapper = mount(NovelDetailCard, {
      props: {
        ...baseProps,
        slug: 'rezero',
      },
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const link = wrapper.findComponent(RouterLinkStub)
    expect(link.exists()).toBe(true)
    expect(link.props('to')).toBe('/novel/rezero')
  })

  it('renders disabled container when slug is empty', () => {
    const wrapper = mount(NovelDetailCard, {
      props: {
        ...baseProps,
        slug: '',
      },
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const link = wrapper.find('.novel-detail-card__link')
    expect(link.element.tagName).toBe('DIV')
    expect(link.attributes('aria-disabled')).toBe('true')
    expect(link.classes()).toContain('novel-detail-card__link--disabled')
  })

  it('renders tags and handles image load/error states', async () => {
    const wrapper = mount(NovelDetailCard, {
      props: {
        ...baseProps,
        slug: 'rezero',
      },
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    expect(wrapper.text()).toContain('Isekai')
    expect(wrapper.text()).toContain('Drama')
    expect(wrapper.find('.novel-detail-card__skeleton').exists()).toBe(true)

    const image = wrapper.find('img')
    await image.trigger('load')

    expect(wrapper.find('.novel-detail-card__skeleton').exists()).toBe(false)
    expect(image.classes()).toContain('novel-detail-card__image--loaded')

    await image.trigger('error')
    expect(image.attributes('src')).toContain('data:image/svg+xml')
  })

  it('renders bookmark status badge when status provided', () => {
    const wrapper = mount(NovelDetailCard, {
      props: {
        ...baseProps,
        slug: 'rezero',
        bookmarkStatus: 'Любимые',
      },
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    })

    const badge = wrapper.find('.novel-detail-card__bookmark-badge')
    expect(badge.exists()).toBe(true)
    expect(badge.text()).toContain('Любимые')
  })
})
