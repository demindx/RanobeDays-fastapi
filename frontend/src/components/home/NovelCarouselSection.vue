<script setup>
	import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
	import SectionTitle from '../ui/SectionTitle.vue'
	import NovelCard from '../ui/NovelCard.vue'

	const props = defineProps({
		novels: {
			type: Array,
			default: () => []
		}
	})

	const trackRef = ref(null)
	const repeatedNovels = computed(() => [...props.novels, ...props.novels, ...props.novels])
	const isDragging = ref(false)
	const suppressCardClick = ref(false)
	const isInertiaActive = ref(false)
	let dragStartX = 0
	let dragStartScrollLeft = 0
	let dragHasMoved = false
	const DRAG_THRESHOLD = 6
	let lastPointerX = 0
	let lastPointerTime = 0
	let velocity = 0
	let inertiaFrameId = null
	const VELOCITY_DAMPING = 0.95
	const VELOCITY_STOP = 0.02

	const getStepWidth = () => {
		const track = trackRef.value
		const firstCard = track?.children?.[0]
		if (!track || !firstCard) return 0
		const gap = Number.parseFloat(window.getComputedStyle(track).columnGap || window.getComputedStyle(track).gap || '0')
		return firstCard.getBoundingClientRect().width + gap
	}

	const getSetWidth = () => getStepWidth() * props.novels.length

	const alignToCenterSet = async () => {
		await nextTick()
		const track = trackRef.value
		const setWidth = getSetWidth()
		if (!track || !setWidth) return
		track.scrollLeft = setWidth
	}

	const normalizeInfiniteScroll = () => {
		const track = trackRef.value
		const setWidth = getSetWidth()
		const step = getStepWidth()
		if (!track || !setWidth || !step) return
		if (track.scrollLeft <= step) {
			track.scrollLeft += setWidth
		} else if (track.scrollLeft >= setWidth * 2 - step) {
			track.scrollLeft -= setWidth
		}
	}

	const stopInertia = () => {
		if (inertiaFrameId !== null) {
			cancelAnimationFrame(inertiaFrameId)
			inertiaFrameId = null
		}
		isInertiaActive.value = false
	}

	const runInertia = () => {
		const track = trackRef.value
		if (!track) {
			stopInertia()
			return
		}
		if (Math.abs(velocity) < VELOCITY_STOP) {
			stopInertia()
			return
		}

		isInertiaActive.value = true
		track.scrollLeft -= velocity * 16
		velocity *= VELOCITY_DAMPING
		inertiaFrameId = requestAnimationFrame(runInertia)
	}

	const startDrag = (event) => {
		if (event.button !== 0) return
		const track = trackRef.value
		if (!track) return
		stopInertia()
		isDragging.value = true
		dragHasMoved = false
		velocity = 0
		dragStartX = event.clientX
		dragStartScrollLeft = track.scrollLeft
		lastPointerX = event.clientX
		lastPointerTime = performance.now()
		window.addEventListener('mousemove', dragScroll)
		window.addEventListener('mouseup', stopDrag)
	}

	const dragScroll = (event) => {
		if (!isDragging.value) return
		const track = trackRef.value
		if (!track) return
		const delta = event.clientX - dragStartX
		if (!dragHasMoved && Math.abs(delta) >= DRAG_THRESHOLD) {
			dragHasMoved = true
		}
		if (!dragHasMoved) return
		event.preventDefault()
		track.scrollLeft = dragStartScrollLeft - delta

		const now = performance.now()
		const dt = Math.max(now - lastPointerTime, 1)
		const dx = event.clientX - lastPointerX
		const instantVelocity = dx / dt
		velocity = velocity * 0.7 + instantVelocity * 0.3
		lastPointerX = event.clientX
		lastPointerTime = now
	}

	const stopDrag = () => {
		if (dragHasMoved) {
			suppressCardClick.value = true
			stopInertia()
			inertiaFrameId = requestAnimationFrame(runInertia)
		}
		isDragging.value = false
		window.removeEventListener('mousemove', dragScroll)
		window.removeEventListener('mouseup', stopDrag)
	}

	const handleTrackClickCapture = (event) => {
		if (!suppressCardClick.value) return
		event.preventDefault()
		event.stopPropagation()
		suppressCardClick.value = false
	}

	onMounted(() => {
		alignToCenterSet()
	})

	onBeforeUnmount(() => {
		stopInertia()
		window.removeEventListener('mousemove', dragScroll)
		window.removeEventListener('mouseup', stopDrag)
	})

	watch(
		() => props.novels.length,
		() => {
			alignToCenterSet()
		}
	)

</script>

<template>
	<section class="space-y-4">
		<SectionTitle title="Популярное" subtitle="Популярное прямо сейчас" />

		<p v-if="!props.novels.length" class="rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 py-6 text-sm text-zinc-400">
			Новелы пока не найдены.
		</p>

		<div
			v-else
			ref="trackRef"
			:class="[
				'carousel-track flex gap-3 overflow-x-auto pb-2 select-none sm:gap-4',
				isDragging ? 'cursor-grabbing' : 'cursor-grab'
			]"
			@scroll="normalizeInfiniteScroll"
			@mousedown="startDrag"
			@click.capture="handleTrackClickCapture"
			@dragstart.prevent
		>
			<NovelCard v-for="(novel, index) in repeatedNovels" :key="`${novel.id}-${index}`" :novel="novel" />
		</div>
	</section>
</template>
