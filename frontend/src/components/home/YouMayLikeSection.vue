<script setup>
	import SectionTitle from '../ui/SectionTitle.vue'

	const props = defineProps({
		items: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<section class="space-y-4">
		<SectionTitle title="Вам может понравиться" subtitle="Персональные рекомендации" />

		<p v-if="!props.items.length" class="rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 py-6 text-sm text-zinc-400">
			Пока нет рекомендаций.
		</p>

		<div v-else class="space-y-2">
			<a
				v-for="item in props.items"
				:key="item.id"
				:href="item.href || '#'"
				class="block rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-3 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99]"
			>
				<h3 class="line-clamp-2 text-sm font-semibold text-white">{{ item.title }}</h3>
				<p class="mt-1 text-xs text-zinc-400">{{ item.genre }} • ★ {{ item.rating }}</p>
			</a>
		</div>
	</section>
</template>
