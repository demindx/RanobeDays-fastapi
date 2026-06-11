<script setup>
import { ref } from 'vue'
import { useProfile } from '../../composables/useProfile'
import AppButton from '../shared/AppButton.vue'
import AppInput from '../shared/AppInput.vue'
import AppModal from '../shared/AppModal.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const { user, updateNickname, updateAvatarColor } = useProfile()
const nickname = ref(user.value.login)
const error = ref('')

const avatarColors = [
  { label: 'Изумрудный', class: 'bg-emerald-500' },
  { label: 'Синий', class: 'bg-blue-500' },
  { label: 'Фиолетовый', class: 'bg-violet-500' },
  { label: 'Оранжевый', class: 'bg-orange-500' },
  { label: 'Розовый', class: 'bg-rose-500' },
  { label: 'Янтарный', class: 'bg-amber-500' },
  { label: 'Красный', class: 'bg-red-500' },
  { label: 'Циановый', class: 'bg-cyan-500' },
]

const handleSave = () => {
  error.value = ''
  const result = updateNickname(nickname.value)
  if (!result.ok) {
    error.value = result.error
    return
  }
  emit('close')
}
</script>

<template>
  <AppModal :open="props.open" @close="emit('close')">
    <div class="mb-6 flex items-center justify-between gap-3">
      <h3 class="text-base font-semibold text-white sm:text-lg">Настройки профиля</h3>
      <AppButton variant="neutral" size="sm" @click="emit('close')"> Закрыть </AppButton>
    </div>

    <div class="space-y-5">
      <div>
        <label class="mb-2 block text-sm text-zinc-400">Никнейм</label>
        <AppInput v-model="nickname" type="text" />
        <p v-if="error" class="mt-1 text-xs text-red-400">{{ error }}</p>
      </div>

      <div>
        <label class="mb-2 block text-sm text-zinc-400">Цвет аватарки</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="color in avatarColors"
            :key="color.class"
            type="button"
            :class="[
              'flex h-10 w-10 items-center justify-center rounded-full text-lg font-bold text-white transition',
              color.class,
              user.avatarColorClass === color.class
                ? 'ring-2 ring-lime-300 ring-offset-2 ring-offset-zinc-900'
                : 'hover:opacity-80',
            ]"
            :aria-label="color.label"
            @click="updateAvatarColor(color.class)"
          >
            {{ user.login.slice(0, 1).toUpperCase() }}
          </button>
        </div>
      </div>
    </div>

    <div class="mt-6 flex justify-end gap-2">
      <AppButton variant="neutral" @click="emit('close')"> Отмена </AppButton>
      <AppButton variant="primary" @click="handleSave"> Сохранить </AppButton>
    </div>
  </AppModal>
</template>
