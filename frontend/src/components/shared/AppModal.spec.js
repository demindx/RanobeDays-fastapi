import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import AppModal from './AppModal.vue'

describe('AppModal', () => {
  it('exposes dialog semantics and closes on Escape', async () => {
    const wrapper = mount(AppModal, {
      props: { open: true },
      slots: { default: '<button type="button">Action</button>' },
      attachTo: document.body,
    })

    const dialog = wrapper.get('[role="dialog"]')
    expect(dialog.attributes('aria-modal')).toBe('true')

    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted('close')).toHaveLength(1)

    wrapper.unmount()
  })
})
