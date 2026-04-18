<script setup>
	import NovelGridCard from '../cards/NovelGridCard.vue'

	const props = defineProps({
		novels: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<div class="grid items-stretch grid-cols-2 gap-2 min-[480px]:grid-cols-3 min-[480px]:gap-2.5 sm:grid-cols-3 sm:gap-3 lg:grid-cols-3 xl:grid-cols-4">
		<NovelGridCard v-for="item in props.novels" :key="item.id" :novel="item" />
	</div>
</template>
