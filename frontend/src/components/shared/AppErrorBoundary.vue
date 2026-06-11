<script setup>
import { onErrorCaptured, ref } from 'vue'
import AppButton from './AppButton.vue'

const error = ref(null)
const hasError = ref(false)

onErrorCaptured((err) => {
  error.value = err
  hasError.value = true
  console.error('[ErrorBoundary]', err)
  return false
})

const retry = () => {
  error.value = null
  hasError.value = false
}
</script>

<template>
  <slot v-if="!hasError" />

  <div v-else class="rounded-xl border border-red-500/30 bg-red-950/20 px-5 py-8 text-center">
    <p class="mb-1 text-sm font-semibold text-red-300">Что-то пошло не так</p>
    <p class="mb-4 text-sm text-zinc-400">
      {{ error?.message || 'Неизвестная ошибка' }}
    </p>
    <AppButton variant="neutral" size="sm" @click="retry"> Попробовать снова </AppButton>
  </div>
</template>
