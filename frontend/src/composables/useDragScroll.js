import { onBeforeUnmount, ref } from 'vue'

export function useDragScroll() {
  const trackRef = ref(null)
  const isDragging = ref(false)
  const suppressCardClick = ref(false)

  let dragStartX = 0
  let dragStartScrollLeft = 0
  let dragHasMoved = false
  const DRAG_THRESHOLD = 6
  let lastPointerX = 0
  let lastPointerTime = 0
  let velocity = 0
  let inertiaFrameId = null
  const VELOCITY_DAMPING = 0.95
  const VELOCITY_STOP = 0.02

  const stopInertia = () => {
    if (inertiaFrameId !== null) {
      cancelAnimationFrame(inertiaFrameId)
      inertiaFrameId = null
    }
  }

  const runInertia = () => {
    const track = trackRef.value
    if (!track || Math.abs(velocity) < VELOCITY_STOP) {
      stopInertia()
      return
    }

    track.scrollLeft -= velocity * 16
    velocity *= VELOCITY_DAMPING
    inertiaFrameId = requestAnimationFrame(runInertia)
  }

  const startDrag = (event) => {
    if (event.button !== 0) return
    const track = trackRef.value
    if (!track) return

    stopInertia()
    isDragging.value = true
    dragHasMoved = false
    velocity = 0
    dragStartX = event.clientX
    dragStartScrollLeft = track.scrollLeft
    lastPointerX = event.clientX
    lastPointerTime = performance.now()
    window.addEventListener('mousemove', dragScroll)
    window.addEventListener('mouseup', stopDrag)
  }

  const dragScroll = (event) => {
    if (!isDragging.value) return
    const track = trackRef.value
    if (!track) return

    const delta = event.clientX - dragStartX
    if (!dragHasMoved && Math.abs(delta) >= DRAG_THRESHOLD) {
      dragHasMoved = true
    }
    if (!dragHasMoved) return

    event.preventDefault()
    track.scrollLeft = dragStartScrollLeft - delta

    const now = performance.now()
    const dt = Math.max(now - lastPointerTime, 1)
    const dx = event.clientX - lastPointerX
    const instantVelocity = dx / dt
    velocity = velocity * 0.7 + instantVelocity * 0.3
    lastPointerX = event.clientX
    lastPointerTime = now
  }

  const stopDrag = () => {
    if (dragHasMoved) {
      suppressCardClick.value = true
      stopInertia()
      inertiaFrameId = requestAnimationFrame(runInertia)
    }
    isDragging.value = false
    window.removeEventListener('mousemove', dragScroll)
    window.removeEventListener('mouseup', stopDrag)
  }

  const handleTrackClickCapture = (event) => {
    if (!suppressCardClick.value) return
    event.preventDefault()
    event.stopPropagation()
    suppressCardClick.value = false
  }

  onBeforeUnmount(() => {
    stopInertia()
    window.removeEventListener('mousemove', dragScroll)
    window.removeEventListener('mouseup', stopDrag)
  })

  return {
    trackRef,
    isDragging,
    startDrag,
    handleTrackClickCapture,
  }
}
