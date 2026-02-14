<script setup>
import NavItem from '@/components/layout/NavItem.vue'

defineProps({
  navItems: {
    type: Array,
    required: true,
  },
})
</script>

<template>
  <nav class="hidden md:flex items-center space-x-6 ml-8">
    <NavItem
      v-for="item in navItems"
      :key="item.to"
      :to="item.to"
      :name="item.name"
    />
  </nav>
</template>
