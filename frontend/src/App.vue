<script setup>
import MobileBottomNav from './components/home/MobileBottomNav.vue'
import AuthModal from './components/home/AuthModal.vue'
import { useAuth } from './composables/useAuth'

const { isAuthModalOpen } = useAuth()
</script>

<template>
  <RouterView />
  <MobileBottomNav />
  <AuthModal :open="isAuthModalOpen" @close="isAuthModalOpen = false" />
</template>
