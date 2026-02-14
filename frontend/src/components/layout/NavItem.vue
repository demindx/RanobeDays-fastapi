<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  to: {
    type: String,
    required: true,
  },
  icon: {
    type: Object,
    default: null,
  },
  activeIcon: {
    type: Object,
    default: null,
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  external: {
    type: Boolean,
    default: false,
  },
})

const sizeClass = computed(() => `nav-item--${props.size}`)

const linkProps = computed(() => {
  if (props.external) {
    return {
      href: props.to,
      target: '_blank',
      rel: 'noopener noreferrer',
    }
  }
  return {}
})
</script>

<template>
  <component
    :is="external ? 'a' : 'router-link'"
    v-bind="linkProps"
    :to="external ? undefined : to"
    class="nav-item"
    :class="sizeClass"
    :aria-current="$route.path === to ? 'page' : undefined"
  >
    <span
      v-if="icon"
      class="nav-item__icon"
    >
      <component :is="icon" />
    </span>
    <span class="nav-item__text">{{ name }}</span>
  </component>
</template>

<style scoped>
.nav-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--first-color);
  transition: width 0.2s ease;
}

.nav-item:hover {
  color: var(--first-color);
}

.nav-item:hover::after {
  width: 100%;
}

.nav-item:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 4px;
  border-radius: 4px;
}

.nav-item--sm {
  font-size: 0.75rem;
  padding: 0.25rem 0;
}

.nav-item--md {
  font-size: 0.875rem;
  padding: 0.375rem 0;
}

.nav-item--lg {
  font-size: 1rem;
  padding: 0.5rem 0;
}

.nav-item__icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-item.router-link-exact-active,
.nav-item[aria-current='page'] {
  color: var(--first-color);
}

.nav-item.router-link-exact-active::after,
.nav-item[aria-current='page']::after {
  width: 100%;
}
</style>
