<script setup>
import ProfileHeader from '../components/profile/ProfileHeader.vue'
import ReadingCalendar from '../components/profile/ReadingCalendar.vue'
import ProfileTabs from '../components/profile/ProfileTabs.vue'
import ProfileSettingsModal from '../components/profile/ProfileSettingsModal.vue'
import AppButton from '../components/shared/AppButton.vue'
import { useProfile } from '../composables/useProfile'

const { isSettingsOpen, openSettings, closeSettings } = useProfile()
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-bold text-white sm:text-2xl">Профиль</h1>
      <AppButton variant="neutral" size="sm" @click="openSettings"> Настройки </AppButton>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <ProfileHeader />
      <ReadingCalendar />
    </div>

    <ProfileTabs />

    <ProfileSettingsModal :open="isSettingsOpen" @close="closeSettings" />
  </div>
</template>
