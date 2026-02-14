import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SearchBar from './SearchBar.vue'

describe('SearchBar', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: '',
      },
    })

    await wrapper.find('input').setValue('solo leveling')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['solo leveling'])
  })

  it('emits search with debounce', async () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: '',
        debounce: 300,
      },
    })

    await wrapper.find('input').setValue('re:zero')
    vi.advanceTimersByTime(299)

    expect(wrapper.emitted('search')).toBeFalsy()

    vi.advanceTimersByTime(1)

    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')[0]).toEqual(['re:zero'])
  })

  it('emits search on Enter', async () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: '',
        debounce: 0,
      },
    })

    const input = wrapper.find('input')
    await input.setValue('lord of the mysteries')
    await input.trigger('keydown', { key: 'Enter' })

    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')[0]).toEqual(['lord of the mysteries'])
  })

  it('clears input and emits clear', async () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: 'overlord',
      },
    })

    const clearButton = wrapper.find('.search-bar__clear')
    expect(clearButton.exists()).toBe(true)

    await clearButton.trigger('click')

    const updates = wrapper.emitted('update:modelValue') || []
    const clears = wrapper.emitted('clear') || []

    expect(updates.at(-1)).toEqual([''])
    expect(clears).toHaveLength(1)
  })
})
