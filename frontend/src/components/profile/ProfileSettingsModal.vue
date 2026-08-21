<script setup>
import { ref, computed } from 'vue'
import { useProfile } from '../../composables/useProfile'
import { catalogFilterOptions } from '../../mocks/catalogData'
import AppButton from '../shared/AppButton.vue'
import AppInput from '../shared/AppInput.vue'
import AppModal from '../shared/AppModal.vue'
import AppTabs from '../shared/AppTabs.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const {
  user,
  updateNickname,
  updateAvatar,
  updateEmail,
  updatePassword,
  toggleGenreBlacklist,
  toggleTagBlacklist,
  toggleAdultContent,
} = useProfile()

const activeTab = ref('profile')
const nickname = ref(user.value?.login || '')
const email = ref(user.value?.email || '')
const currentPassword = ref('')
const newPassword = ref('')
const error = ref('')
const success = ref('')

const tabs = [
  { key: 'profile', label: 'Профиль' },
  { key: 'content', label: 'Контент' },
  { key: 'account', label: 'Аккаунт' },
]

const fileInput = ref(null)

const handleAvatarUpload = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    error.value = 'Можно загружать только изображения.'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    error.value = 'Размер файла не должен превышать 5 МБ.'
    return
  }
  success.value = ''
  updateAvatar(file)
}

const handleAvatarRemove = () => {
  updateAvatar(null)
  success.value = 'Аватар удалён.'
}

const genres = computed(() => catalogFilterOptions.genres)
const tags = computed(() => catalogFilterOptions.tags)
const blacklistedGenres = computed(() => user.value?.settings?.blacklistedGenres || [])
const blacklistedTags = computed(() => user.value?.settings?.blacklistedTags || [])
const hideAdultContent = computed(() => user.value?.settings?.hideAdultContent || false)

const isGenreBlacklisted = (genre) => blacklistedGenres.value.includes(genre)
const isTagBlacklisted = (tag) => blacklistedTags.value.includes(tag)

const clearError = () => {
  error.value = ''
  success.value = ''
}

const handleSaveNickname = () => {
  clearError()
  const result = updateNickname(nickname.value)
  if (!result.ok) {
    error.value = result.error
    return
  }
  success.value = 'Никнейм обновлён.'
}

const handleSaveEmail = () => {
  clearError()
  const result = updateEmail(email.value)
  if (!result.ok) {
    error.value = result.error
    return
  }
  success.value = 'Email обновлён.'
}

const handleSavePassword = () => {
  clearError()
  const result = updatePassword(currentPassword.value, newPassword.value)
  if (!result.ok) {
    error.value = result.error
    return
  }
  success.value = 'Пароль обновлён.'
  currentPassword.value = ''
  newPassword.value = ''
}

const handleClose = () => {
  clearError()
  emit('close')
}
</script>

<template>
  <AppModal
    :open="props.open"
    container-class="flex items-end justify-center px-3 py-3 sm:items-center sm:px-4 sm:py-6"
    panel-class="max-h-[85vh] w-full max-w-xl overflow-y-auto rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5"
    @close="handleClose"
  >
    <div class="mb-4 flex items-center justify-between gap-3">
      <h3 class="text-base font-semibold text-white sm:text-lg">Настройки</h3>
      <AppButton variant="neutral" size="sm" @click="handleClose"> Закрыть </AppButton>
    </div>

    <AppTabs v-model="activeTab" :tabs="tabs" />

    <p v-if="error" class="mt-4 text-sm text-red-400">{{ error }}</p>
    <p v-if="success" class="mt-4 text-sm text-lime-300">{{ success }}</p>

    <!-- Профиль -->
    <div v-if="activeTab === 'profile'" class="mt-5 space-y-5">
      <div>
        <label class="mb-2 block text-sm text-zinc-400">Аватар</label>
        <div class="flex items-center gap-4">
          <div
            class="flex h-16 w-16 shrink-0 items-center justify-center overflow-hidden rounded-full text-lg font-bold text-white"
            :class="user?.avatarUrl ? '' : 'bg-emerald-500'"
          >
            <img
              v-if="user?.avatarUrl"
              :src="user.avatarUrl"
              alt="Аватар"
              class="h-full w-full object-cover"
            />
            <span v-else>{{ user?.login?.slice(0, 1).toUpperCase() }}</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleAvatarUpload"
            />
            <AppButton variant="neutral" size="sm" @click="fileInput?.click()">
              Загрузить фото
            </AppButton>
            <AppButton
              v-if="user?.avatarUrl"
              variant="neutral"
              size="sm"
              @click="handleAvatarRemove"
            >
              Удалить
            </AppButton>
          </div>
        </div>
      </div>

      <div>
        <label class="mb-2 block text-sm text-zinc-400">Никнейм</label>
        <AppInput v-model="nickname" type="text" />
      </div>

      <div class="flex justify-end">
        <AppButton variant="primary" @click="handleSaveNickname"> Сохранить </AppButton>
      </div>
    </div>

    <!-- Контент -->
    <div v-if="activeTab === 'content'" class="mt-5 space-y-6">
      <div
        class="flex items-center justify-between rounded-lg border border-zinc-700 bg-zinc-800/50 p-3"
      >
        <div>
          <p class="text-sm font-medium text-white">Скрывать 18+ контент</p>
          <p class="text-xs text-zinc-400">
            Новеллы с возрастным рейтингом 18+ не будут отображаться
          </p>
        </div>
        <button
          type="button"
          role="switch"
          :aria-checked="hideAdultContent"
          :class="[
            'relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors',
            hideAdultContent ? 'bg-lime-500' : 'bg-zinc-600',
          ]"
          @click="toggleAdultContent"
        >
          <span
            :class="[
              'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transition-transform',
              hideAdultContent ? 'translate-x-5' : 'translate-x-0',
            ]"
          />
        </button>
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-zinc-400">Чёрный список жанров</label>
        <p class="mb-2 text-xs text-zinc-500">Выбранные жанры будут скрыты из каталога</p>
        <div class="flex flex-wrap gap-1.5">
          <button
            v-for="genre in genres"
            :key="genre"
            type="button"
            :class="[
              'rounded-md border px-2.5 py-1 text-xs transition',
              isGenreBlacklisted(genre)
                ? 'border-rose-500/50 bg-rose-500/20 text-rose-300'
                : 'border-zinc-700 text-zinc-400 hover:border-zinc-600 hover:text-zinc-300',
            ]"
            @click="toggleGenreBlacklist(genre)"
          >
            {{ genre }}
          </button>
        </div>
      </div>

      <div>
        <label class="mb-2 block text-sm font-medium text-zinc-400">Чёрный список тегов</label>
        <p class="mb-2 text-xs text-zinc-500">Выбранные теги будут скрыты из каталога</p>
        <div class="flex flex-wrap gap-1.5">
          <button
            v-for="tag in tags"
            :key="tag"
            type="button"
            :class="[
              'rounded-md border px-2.5 py-1 text-xs transition',
              isTagBlacklisted(tag)
                ? 'border-rose-500/50 bg-rose-500/20 text-rose-300'
                : 'border-zinc-700 text-zinc-400 hover:border-zinc-600 hover:text-zinc-300',
            ]"
            @click="toggleTagBlacklist(tag)"
          >
            {{ tag }}
          </button>
        </div>
      </div>
    </div>

    <!-- Аккаунт -->
    <div v-if="activeTab === 'account'" class="mt-5 space-y-6">
      <div>
        <label class="mb-2 block text-sm text-zinc-400">Email</label>
        <AppInput v-model="email" type="email" placeholder="email@example.com" />
        <div class="mt-3 flex justify-end">
          <AppButton variant="primary" @click="handleSaveEmail"> Сменить email </AppButton>
        </div>
      </div>

      <div class="border-t border-zinc-800 pt-5">
        <label class="mb-2 block text-sm text-zinc-400">Сменить пароль</label>
        <div class="space-y-3">
          <div>
            <label class="mb-1 block text-xs text-zinc-500">Текущий пароль</label>
            <AppInput v-model="currentPassword" type="password" placeholder="••••••" />
          </div>
          <div>
            <label class="mb-1 block text-xs text-zinc-500">Новый пароль</label>
            <AppInput v-model="newPassword" type="password" placeholder="Минимум 6 символов" />
          </div>
        </div>
        <div class="mt-3 flex justify-end">
          <AppButton variant="primary" @click="handleSavePassword"> Сменить пароль </AppButton>
        </div>
      </div>
    </div>
  </AppModal>
</template>
