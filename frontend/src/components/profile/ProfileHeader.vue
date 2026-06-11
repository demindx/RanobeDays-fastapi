<script setup>
import { useProfile } from '../../composables/useProfile'

const { user } = useProfile()

const formatNumber = (n) => new Intl.NumberFormat('ru-RU').format(n)
</script>

<template>
  <div
    class="flex flex-col gap-4 rounded-2xl border border-zinc-700/70 bg-zinc-900/80 px-4 py-5 sm:flex-row sm:items-center sm:gap-6 sm:px-6"
  >
    <div
      class="mx-auto flex h-20 w-20 shrink-0 items-center justify-center rounded-full text-2xl font-bold text-white sm:mx-0 sm:h-24 sm:w-24"
      :class="user.avatarColorClass"
    >
      {{ user.login.slice(0, 1).toUpperCase() }}
    </div>

    <div class="flex-1 text-center sm:text-left">
      <h1 class="text-xl font-bold text-white sm:text-2xl">{{ user.login }}</h1>
      <p class="text-sm text-zinc-500">
        На сайте с {{ new Date(user.joinDate).toLocaleDateString('ru-RU') }}
      </p>

      <div class="mt-3 grid grid-cols-2 gap-x-6 gap-y-2 text-sm sm:flex sm:flex-wrap sm:gap-4">
        <div class="text-center sm:text-left">
          <span class="font-semibold text-lime-300">{{
            formatNumber(user.stats.chaptersRead)
          }}</span>
          <span class="ml-1 text-zinc-400">глав</span>
        </div>
        <div class="text-center sm:text-left">
          <span class="font-semibold text-lime-300">{{ user.stats.novelsCompleted }}</span>
          <span class="ml-1 text-zinc-400">завершено</span>
        </div>
        <div class="text-center sm:text-left">
          <span class="font-semibold text-lime-300">{{ user.stats.readingHours }}ч</span>
          <span class="ml-1 text-zinc-400">чтения</span>
        </div>
        <div class="text-center sm:text-left">
          <span class="font-semibold text-lime-300">{{ user.stats.streakDays }}д</span>
          <span class="ml-1 text-zinc-400">подряд</span>
        </div>
      </div>
    </div>
  </div>
</template>
