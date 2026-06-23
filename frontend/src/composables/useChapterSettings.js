import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'ranobe-chapter-settings'

const defaultSettings = {
  fontFamily: 'Inter',
  fontSize: 16,
  bgColor: 'dark',
  contentWidth: 920,
}

const fontOptions = [
  { value: 'Inter', label: 'Inter', family: 'Inter, sans-serif' },
  { value: 'PT Serif', label: 'PT Serif', family: "'PT Serif', serif" },
  { value: 'PT Sans', label: 'PT Sans', family: "'PT Sans', sans-serif" },
  { value: 'Roboto', label: 'Roboto', family: 'Roboto, sans-serif' },
  { value: 'Roboto Slab', label: 'Roboto Slab', family: "'Roboto Slab', serif" },
  { value: 'Georgia', label: 'Georgia', family: 'Georgia, serif' },
  { value: 'Verdana', label: 'Verdana', family: 'Verdana, sans-serif' },
  { value: 'Times New Roman', label: 'Times', family: "'Times New Roman', serif" },
]

const bgPresets = [
  { value: 'dark', label: 'Тёмный', bg: '#0f0f11', text: '#e4e4e7' },
  { value: 'light', label: 'Светлый', bg: '#f4f6fb', text: '#18181b' },
  { value: 'sepia', label: 'Сепия', bg: '#f4ecd8', text: '#3d2b1f' },
  { value: 'white', label: 'Белый', bg: '#ffffff', text: '#18181b' },
]

const widthMin = 740
const widthStep = 20

const viewportWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1200)
if (typeof window !== 'undefined') {
  window.addEventListener('resize', () => {
    viewportWidth.value = window.innerWidth
  })
}

const widthMax = computed(() => Math.max(widthMin, viewportWidth.value - 200))

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { ...defaultSettings }
    const parsed = JSON.parse(raw)
    if (typeof parsed?.fontSize !== 'number') parsed.fontSize = defaultSettings.fontSize
    if (typeof parsed?.contentWidth !== 'number') parsed.contentWidth = defaultSettings.contentWidth
    return parsed
  } catch {
    return { ...defaultSettings }
  }
}

function save(settings) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
}

const settings = ref(load())

watch(settings, save, { deep: true })

export function useChapterSettings() {
  const currentFont = () => fontOptions.find((f) => f.value === settings.value.fontFamily)

  const currentBg = () => bgPresets.find((b) => b.value === settings.value.bgColor)

  const setFont = (value) => {
    settings.value.fontFamily = value
  }

  const setFontSize = (value) => {
    settings.value.fontSize = Math.max(12, Math.min(28, value))
  }

  const setBgColor = (value) => {
    settings.value.bgColor = value
  }

  const setContentWidth = (value) => {
    settings.value.contentWidth = Math.max(widthMin, Math.min(widthMax.value, value))
  }

  const reset = () => {
    settings.value = { ...defaultSettings }
  }

  return {
    settings,
    fontOptions,
    bgPresets,
    widthMin,
    widthMax,
    widthStep,
    currentFont,
    currentBg,
    setFont,
    setFontSize,
    setBgColor,
    setContentWidth,
    reset,
  }
}
