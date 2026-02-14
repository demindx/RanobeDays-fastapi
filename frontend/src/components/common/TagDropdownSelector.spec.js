import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import TagDropdownSelector from './TagDropdownSelector.vue'

describe('TagDropdownSelector', () => {
  const options = [
    { label: 'Tag A', value: 'a' },
    { label: 'Tag B', value: 'b' },
    { label: 'Tag C', value: 'c' },
    { label: 'Tag D', value: 'd' },
    { label: 'Tag E', value: 'e' },
  ]

  it('renders selected tags and overflow chip', () => {
    const wrapper = mount(TagDropdownSelector, {
      props: {
        modelValue: ['a', 'b', 'c', 'd', 'e'],
        options,
        maxVisibleTags: 4,
      },
    })

    expect(wrapper.findAll('.rd-tag-select__chip')).toHaveLength(5)
    expect(wrapper.find('.rd-tag-select__chip--more').exists()).toBe(true)
  })

  it('opens menu and toggles tag value', async () => {
    const wrapper = mount(TagDropdownSelector, {
      props: {
        modelValue: ['a'],
        options,
      },
    })

    await wrapper.find('.rd-tag-select__trigger').trigger('click')
    const optionB = wrapper.findAll('.rd-tag-select__option')[1]
    await optionB.trigger('click')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual([['a', 'b']])
    expect(wrapper.emitted('change')).toBeTruthy()
  })
})
