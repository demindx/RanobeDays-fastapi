<script setup>
	import { ref } from 'vue'
	import { RouterLink } from 'vue-router'
	import Icon from '../icons/Icon.vue'
	import SearchIcon from '../icons/SearchIcon.vue'
	import NotificationBellIcon from '../icons/NotificationBellIcon.vue'
	import AuthModal from './AuthModal.vue'
	import { useTheme } from '../../composables/useTheme'

	const props = defineProps({
		isAuthenticated: {
			type: Boolean,
			default: false
		},
		user: {
			type: Object,
			default: null
		},
		hasUnreadNotifications: {
			type: Boolean,
			default: false
		}
	})

	const isAuthModalOpen = ref(false)
	const { isDark, toggleTheme } = useTheme()

	const navLinks = [
		{ label: 'Главная', to: '/' },
		{ label: 'Каталог', to: '/catalog' },
		{ label: 'Закладки', href: '#' },
		{ label: 'Коллекции', href: '#' }
	]
</script>

<template>
	<header class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80 px-3 py-3 sm:px-4 sm:py-4 md:hidden">
		<div class="relative w-full">
			<input
				type="text"
				placeholder="Поиск новел..."
				class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white outline-none transition focus:border-lime-300"
			/>
			<SearchIcon class="pointer-events-none absolute right-2 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-300 [&>svg>path]:fill-current" />
		</div>
	</header>

	<header class="hidden rounded-2xl border border-zinc-700/70 bg-zinc-900/80 px-3 py-3 sm:px-4 sm:py-4 md:block">
		<div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between md:gap-4">
			<RouterLink to="/" class="rounded-md transition hover:opacity-90">
				<Icon class="h-7 w-auto sm:h-8" />
			</RouterLink>

			<nav class="flex flex-wrap items-center gap-1.5 text-xs text-zinc-300 sm:gap-2 sm:text-sm">
				<component
					v-for="link in navLinks"
					:key="link.label"
					:is="link.to ? RouterLink : 'a'"
					:to="link.to"
					:href="link.href"
					class="cursor-pointer select-none rounded-md px-2 py-1 transition hover:bg-zinc-800 hover:text-white"
				>
					{{ link.label }}
				</component>
			</nav>

			<div class="flex w-full flex-col gap-2 sm:flex-row sm:items-center sm:gap-3 md:w-auto">
				<div class="relative w-full sm:flex-1 md:w-72 md:min-w-72 md:flex-none">
					<input
						type="text"
						placeholder="Поиск новел..."
						class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white outline-none transition focus:border-lime-300"
					/>
					<SearchIcon class="pointer-events-none absolute right-2 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-300 [&>svg>path]:fill-current" />
				</div>

				<button
					type="button"
					class="shrink-0 cursor-pointer rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm font-medium text-zinc-200 transition hover:bg-zinc-700 active:scale-95"
					@click="toggleTheme"
				>
					{{ isDark ? 'Светлая' : 'Тёмная' }}
				</button>

				<button
					v-if="!props.isAuthenticated"
					type="button"
					class="shrink-0 cursor-pointer rounded-lg bg-lime-300 px-4 py-2 text-sm font-semibold text-zinc-900 transition hover:bg-lime-200 active:scale-95"
					@click="isAuthModalOpen = true"
				>
					Войти
				</button>

				<div v-else class="flex items-center gap-2">
					<button
						type="button"
						class="relative rounded-lg border border-zinc-700 bg-zinc-800 p-2 text-zinc-200 transition hover:bg-zinc-700 active:scale-95"
						aria-label="Уведомления"
					>
						<NotificationBellIcon />
						<span
							v-if="props.hasUnreadNotifications"
							class="absolute right-1 top-1 h-2.5 w-2.5 rounded-full border border-zinc-900 bg-emerald-400"
						/>
					</button>

					<button
						type="button"
						class="flex h-10 w-10 items-center justify-center rounded-full border border-zinc-700 text-sm font-semibold text-white transition hover:opacity-90 active:scale-95"
						:class="props.user?.avatarColorClass || 'bg-zinc-700'"
						:aria-label="`Профиль ${props.user?.login || ''}`"
					>
						{{ (props.user?.login || 'U').slice(0, 1).toUpperCase() }}
					</button>
				</div>
			</div>
		</div>
	</header>

	<AuthModal :open="isAuthModalOpen" @close="isAuthModalOpen = false" />
</template>
