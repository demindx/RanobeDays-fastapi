<script setup>
const props = defineProps({
  as: {
    type: String,
    default: 'h2',
    validator: (value) => ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(value),
  },
})
</script>

<template>
  <component
    :is="props.as"
    class="section-accent-title"
  >
    <slot />
  </component>
</template>

<style scoped>
.section-accent-title {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: var(--foreground-third-color);
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.section-accent-title::before {
  content: '';
  width: 0.38rem;
  height: 1.05rem;
  border-radius: 999px;
  background: linear-gradient(180deg, var(--first-color), color-mix(in srgb, var(--first-color) 55%, transparent));
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--first-color) 32%, transparent);
}

@media (max-width: 767px) {
  .section-accent-title {
    font-size: 1rem;
  }
}
</style>
