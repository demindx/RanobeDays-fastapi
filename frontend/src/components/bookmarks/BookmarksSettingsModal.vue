<script setup>
import { reactive, ref, watch } from 'vue'
import { useBookmarks } from '../../composables/useBookmarks'
import AppInput from '../shared/AppInput.vue'
import AppButton from '../shared/AppButton.vue'
import AppModal from '../shared/AppModal.vue'

const props = defineProps({
  open: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const { bookmarks, renameBookmark, createBookmark, togglePrivacy } = useBookmarks()

const createName = ref('')
const createError = ref('')
const drafts = reactive({})
const errors = reactive({})

const syncDrafts = () => {
  bookmarks.value.forEach((b) => {
    drafts[b.id] = b.name
  })
}

syncDrafts()

watch(
  () => props.open,
  (next) => {
    if (!next) {
      createName.value = ''
      createError.value = ''
      syncDrafts()
    }
  },
)

const handleSave = (bookmarkId) => {
  const result = renameBookmark(bookmarkId, drafts[bookmarkId])
  errors[bookmarkId] = result.ok ? '' : result.error
}

const handleCreate = () => {
  const result = createBookmark(createName.value)
  createError.value = result.ok ? '' : result.error
  if (result.ok) {
    createName.value = ''
    syncDrafts()
  }
}
</script>

<template>
  <AppModal
    :open="props.open"
    container-class="flex items-end justify-center px-3 py-3 sm:items-center sm:px-4 sm:py-6"
    panel-class="max-h-[92vh] w-full max-w-lg overflow-y-auto rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5"
    @close="emit('close')"
  >
    <div class="mb-4 flex items-center justify-between gap-2">
      <div>
        <h3 class="text-base font-semibold text-white sm:text-lg">Настройки закладок</h3>
        <p class="text-xs text-zinc-400">Управляйте названиями и видимостью.</p>
      </div>
      <AppButton variant="neutral" size="sm" @click="emit('close')"> Закрыть </AppButton>
    </div>

    <div class="space-y-2">
      <div
        v-for="bookmark in bookmarks"
        :key="bookmark.id"
        class="rounded-lg border border-zinc-700 bg-zinc-800/50 px-3 py-2"
      >
        <div class="flex items-center gap-2">
          <AppInput v-model="drafts[bookmark.id]" type="text" class="flex-1" />
          <span class="shrink-0 rounded-full bg-zinc-700/50 px-2 py-0.5 text-xs text-zinc-400">
            {{ bookmark.items.length }}
          </span>
        </div>

        <div v-if="errors[bookmark.id]" class="mt-1 text-xs text-red-400">
          {{ errors[bookmark.id] }}
        </div>

        <div class="mt-2 flex items-center justify-between gap-2">
          <button
            type="button"
            :class="[
              'rounded-full px-2.5 py-1 text-xs font-medium transition',
              bookmark.isPublic
                ? 'border border-emerald-300/40 bg-emerald-400/15 text-emerald-300 hover:bg-emerald-400/25'
                : 'border border-rose-300/40 bg-rose-400/15 text-rose-300 hover:bg-rose-400/25',
            ]"
            @click="togglePrivacy(bookmark.id)"
          >
            {{ bookmark.isPublic ? 'Публичная' : 'Приватная' }}
          </button>

          <AppButton
            variant="neutral"
            size="sm"
            :disabled="drafts[bookmark.id] === bookmark.name"
            @click="handleSave(bookmark.id)"
          >
            Сохранить
          </AppButton>
        </div>
      </div>
    </div>

    <div class="mt-3 space-y-2 border-t border-zinc-800 pt-3">
      <p class="text-xs font-medium text-zinc-400">Новая закладка</p>
      <div class="flex gap-2">
        <AppInput
          v-model="createName"
          type="text"
          placeholder="Название"
          class="flex-1"
          @keyup.enter="handleCreate"
        />
        <AppButton variant="primary" size="sm" @click="handleCreate"> Создать </AppButton>
      </div>
      <p v-if="createError" class="text-xs text-red-400">{{ createError }}</p>
    </div>
  </AppModal>
</template>
