<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'horizontal',
    validator: (value) => ['horizontal', 'vertical', 'centered'].includes(value),
  },
  sticky: {
    type: Boolean,
    default: false,
  },
  shadow: {
    type: Boolean,
    default: false,
  },
})

const navbarClass = computed(() => {
  const base = 'navbar'
  const variantClass = `navbar--${props.variant}`
  const stickyClass = props.sticky ? 'navbar--sticky' : ''
  const shadowClass = props.shadow ? 'navbar--shadow' : ''

  return [base, variantClass, stickyClass, shadowClass].filter(Boolean).join(' ')
})
</script>

<template>
  <nav
    :class="navbarClass"
    role="navigation"
    aria-label="Основная навигация"
  >
    <div class="navbar__container">
      <slot />
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  background: var(--fourth-color);
}

.navbar__container {
  display: flex;
  width: 100%;
  max-width: 1250px;
  margin: 0 auto;
  padding: 0 1rem;
}

.navbar--horizontal .navbar__container {
  justify-content: space-between;
  align-items: center;
}

.navbar--vertical .navbar__container {
  flex-direction: column;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
}

.navbar--centered .navbar__container {
  justify-content: center;
  align-items: center;
}

.navbar--sticky {
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar--shadow {
  box-shadow: var(--shadow-soft);
}
</style>
