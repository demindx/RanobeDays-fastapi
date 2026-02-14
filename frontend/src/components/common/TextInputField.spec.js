import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import TextInputField from './TextInputField.vue'

describe('TextInputField', () => {
  it('emits update:modelValue on input', async () => {
    const wrapper = mount(TextInputField, {
      props: {
        modelValue: '',
      },
    })

    await wrapper.find('input').setValue('hello')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['hello'])
  })

  it('emits enter with current value', async () => {
    const wrapper = mount(TextInputField, {
      props: {
        modelValue: 'abc',
      },
    })

    await wrapper.find('input').trigger('keydown', { key: 'Enter' })

    expect(wrapper.emitted('enter')).toBeTruthy()
    expect(wrapper.emitted('enter')[0]).toEqual(['abc'])
  })
})
