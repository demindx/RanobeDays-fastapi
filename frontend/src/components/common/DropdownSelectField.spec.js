import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import DropdownSelectField from './DropdownSelectField.vue'

describe('DropdownSelectField', () => {
  const options = [
    { label: 'Option A', value: 'a' },
    { label: 'Option B', value: 'b' },
  ]

  it('renders selected label', () => {
    const wrapper = mount(DropdownSelectField, {
      props: {
        modelValue: 'a',
        options,
      },
    })

    expect(wrapper.find('.rd-select__label').text()).toBe('Option A')
  })

  it('opens menu and emits update:modelValue and change on option click', async () => {
    const wrapper = mount(DropdownSelectField, {
      props: {
        modelValue: 'a',
        options,
      },
    })

    await wrapper.find('.rd-select__trigger').trigger('click')
    const option = wrapper.findAll('.rd-select__option')[1]
    await option.trigger('click')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['b'])
    expect(wrapper.emitted('change')).toBeTruthy()
    expect(wrapper.emitted('change')[0]).toEqual(['b'])
  })
})
