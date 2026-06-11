<script setup>
import { computed, ref } from 'vue'
import { useClickOutside } from '../../composables/useClickOutside'
import { useChapterSettings } from '../../composables/useChapterSettings'
import AppButton from '../shared/AppButton.vue'
import CloseIcon from '../icons/CloseIcon.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const rootRef = ref(null)
const {
  settings,
  fontOptions,
  bgPresets,
  widthOptions,
  currentBg,
  setFont,
  setFontSize,
  setBgColor,
  setContentWidth,
  reset,
} = useChapterSettings()

const panelBg = computed(() => currentBg()?.bg || '#0f0f11')
const panelText = computed(() => currentBg()?.text || '#e4e4e7')
const panelBorder = computed(() =>
  panelBg.value === '#0f0f11' ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)',
)
const panelInputBg = computed(() =>
  panelBg.value === '#0f0f11' || panelBg.value === '#ffffff'
    ? 'rgba(128,128,128,0.1)'
    : 'rgba(128,128,128,0.08)',
)

const close = () => emit('close')
useClickOutside(rootRef, () => props.open, close)
</script>

<template>
  <Teleport to="body">
    <div
      :class="[
        'fixed inset-0 z-50 transition-opacity duration-300',
        props.open ? 'pointer-events-auto' : 'pointer-events-none',
      ]"
    >
      <div
        :class="[
          'absolute inset-0 bg-black/30 transition-opacity duration-300',
          props.open ? 'opacity-100' : 'opacity-0',
        ]"
        @click="close"
      />

      <aside
        ref="rootRef"
        :class="[
          'absolute right-0 top-0 flex h-full w-80 max-w-[88vw] flex-col shadow-2xl transition-transform duration-300',
          props.open ? 'translate-x-0' : 'translate-x-full',
        ]"
        :style="{
          backgroundColor: panelBg,
          color: panelText,
          borderLeft: `1px solid ${panelBorder}`,
        }"
      >
        <div
          class="flex items-center justify-between border-b px-5 py-4"
          :style="{ borderColor: panelBorder }"
        >
          <div>
            <h3 class="text-base font-semibold">Настройки чтения</h3>
          </div>
          <button
            type="button"
            class="cursor-pointer rounded-md p-1.5 opacity-60 transition hover:opacity-100"
            @click="close"
          >
            <CloseIcon />
          </button>
        </div>

        <div class="flex-1 space-y-6 overflow-y-auto px-5 py-5">
          <div>
            <label class="mb-2 block text-sm font-medium opacity-70">Шрифт</label>
            <div class="grid grid-cols-2 gap-1.5">
              <button
                v-for="font in fontOptions"
                :key="font.value"
                type="button"
                :class="[
                  'rounded-lg border px-3 py-2 text-left text-sm transition',
                  settings.fontFamily === font.value
                    ? 'opacity-100'
                    : 'opacity-50 hover:opacity-80',
                ]"
                :style="{
                  fontFamily: font.family,
                  borderColor: settings.fontFamily === font.value ? 'currentColor' : panelBorder,
                  backgroundColor:
                    settings.fontFamily === font.value ? panelInputBg : 'transparent',
                }"
                @click="setFont(font.value)"
              >
                {{ font.label }}
              </button>
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium opacity-70">
              Размер: {{ settings.fontSize }}px
            </label>
            <div class="flex items-center gap-2">
              <button
                type="button"
                class="flex h-8 w-8 cursor-pointer items-center justify-center rounded-lg border text-sm transition hover:opacity-80"
                :style="{ borderColor: panelBorder }"
                @click="setFontSize(settings.fontSize - 1)"
              >
                −
              </button>
              <input
                type="range"
                min="12"
                max="28"
                :value="settings.fontSize"
                class="h-2 flex-1 cursor-pointer appearance-none rounded-full"
                :style="{ accentColor: panelText }"
                @input="setFontSize(Number($event.target.value))"
              />
              <button
                type="button"
                class="flex h-8 w-8 cursor-pointer items-center justify-center rounded-lg border text-sm transition hover:opacity-80"
                :style="{ borderColor: panelBorder }"
                @click="setFontSize(settings.fontSize + 1)"
              >
                +
              </button>
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium opacity-70">Ширина текста</label>
            <div class="flex gap-1.5">
              <button
                v-for="w in widthOptions"
                :key="w.value"
                type="button"
                :class="[
                  'flex-1 rounded-lg border px-2 py-2 text-center text-xs transition',
                  settings.contentWidth === w.value ? 'opacity-100' : 'opacity-50 hover:opacity-80',
                ]"
                :style="{
                  borderColor: settings.contentWidth === w.value ? 'currentColor' : panelBorder,
                  backgroundColor: settings.contentWidth === w.value ? panelInputBg : 'transparent',
                }"
                @click="setContentWidth(w.value)"
              >
                {{ w.label }}
              </button>
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium opacity-70">Цвет фона</label>
            <div class="flex gap-2">
              <button
                v-for="preset in bgPresets"
                :key="preset.value"
                type="button"
                :class="[
                  'flex h-10 w-10 items-center justify-center rounded-full border-2 text-xs font-bold transition',
                  settings.bgColor === preset.value
                    ? 'opacity-100'
                    : 'border-transparent opacity-50 hover:opacity-80',
                ]"
                :style="{
                  backgroundColor: preset.bg,
                  color: preset.text,
                  borderColor: settings.bgColor === preset.value ? preset.text : 'transparent',
                }"
                :title="preset.label"
                @click="setBgColor(preset.value)"
              >
                A
              </button>
            </div>
          </div>
        </div>

        <div class="border-t px-5 py-4" :style="{ borderColor: panelBorder }">
          <AppButton variant="neutral" block @click="reset"> Сбросить </AppButton>
        </div>
      </aside>
    </div>
  </Teleport>
</template>
