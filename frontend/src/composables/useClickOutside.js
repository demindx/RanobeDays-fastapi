import { onBeforeUnmount, onMounted } from 'vue'

export function useClickOutside(rootRef, isOpen, onClose) {
  const handleClickOutside = (event) => {
    if (!isOpen.value) return
    if (!rootRef.value) return
    if (rootRef.value.contains(event.target)) return
    onClose()
  }

  const handleEscape = (event) => {
    if (event.key !== 'Escape') return
    if (!isOpen.value) return
    onClose()
  }

  onMounted(() => {
    document.addEventListener('mousedown', handleClickOutside)
    window.addEventListener('keydown', handleEscape)
  })

  onBeforeUnmount(() => {
    document.removeEventListener('mousedown', handleClickOutside)
    window.removeEventListener('keydown', handleEscape)
  })
}
