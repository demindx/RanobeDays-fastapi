<script setup>
	import { ref } from 'vue'
	import { RouterLink } from 'vue-router'
	import Icon from '../icons/Icon.vue'
	import SearchIcon from '../icons/SearchIcon.vue'
	import NavHomeIcon from '../icons/NavHomeIcon.vue'
	import NavCatalogIcon from '../icons/NavCatalogIcon.vue'
	import NavBookmarkIcon from '../icons/NavBookmarkIcon.vue'
	import NavCollectionIcon from '../icons/NavCollectionIcon.vue'
	import NavMenuIcon from '../icons/NavMenuIcon.vue'
	import CloseIcon from '../icons/CloseIcon.vue'
	import ChevronRightIcon from '../icons/ChevronRightIcon.vue'
	import NotificationBellIcon from '../icons/NotificationBellIcon.vue'
	import AuthModal from './AuthModal.vue'
	import { useTheme } from '../../composables/useTheme'
	import { useAuth } from '../../composables/useAuth'

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

	const isMenuOpen = ref(false)
	const isAuthModalOpen = ref(false)
	const { isDark, toggleTheme } = useTheme()
	const { logout } = useAuth()

	const mainLinks = [
		{ label: 'Главная', to: '/', icon: NavHomeIcon },
		{ label: 'Каталог', to: '/catalog', icon: NavCatalogIcon },
		{ label: 'Закладки', href: '#', icon: NavBookmarkIcon }
	]

	const fullMenuLinks = [
		{ label: 'Главная', to: '/', icon: NavHomeIcon },
		{ label: 'Каталог', to: '/catalog', icon: NavCatalogIcon },
		{ label: 'Закладки', href: '#', icon: NavBookmarkIcon },
		{ label: 'Коллекции', href: '#', icon: NavCollectionIcon }
	]

	const openAuthFromMenu = () => {
		isMenuOpen.value = false
		isAuthModalOpen.value = true
	}

	const handleLogout = () => {
		logout()
		isMenuOpen.value = false
	}
</script>

<template>
	<nav class="fixed inset-x-0 bottom-0 z-40 border-t border-zinc-700/80 bg-zinc-900/95 backdrop-blur md:hidden">
		<div class="mx-auto w-full max-w-6xl px-2 pb-[calc(env(safe-area-inset-bottom)+8px)] pt-2">
			<div class="grid grid-cols-5 items-end gap-1 text-zinc-300">
				<component
					:is="mainLinks[0].to ? RouterLink : 'a'"
					:to="mainLinks[0].to"
					:href="mainLinks[0].href"
					class="flex cursor-pointer select-none flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] transition hover:bg-zinc-800 active:scale-95"
				>
					<component :is="mainLinks[0].icon" />
					<span>{{ mainLinks[0].label }}</span>
				</component>
				<component
					:is="mainLinks[1].to ? RouterLink : 'a'"
					:to="mainLinks[1].to"
					:href="mainLinks[1].href"
					class="flex cursor-pointer select-none flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] transition hover:bg-zinc-800 active:scale-95"
				>
					<component :is="mainLinks[1].icon" />
					<span>{{ mainLinks[1].label }}</span>
				</component>

				<RouterLink to="/" class="mx-auto -mt-6 rounded-full border border-zinc-700/80 bg-zinc-950 p-2.5 shadow-lg transition hover:opacity-90 active:scale-95">
					<Icon class="h-7 w-auto" />
				</RouterLink>

				<component
					:is="mainLinks[2].to ? RouterLink : 'a'"
					:to="mainLinks[2].to"
					:href="mainLinks[2].href"
					class="flex cursor-pointer select-none flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] transition hover:bg-zinc-800 active:scale-95"
				>
					<component :is="mainLinks[2].icon" />
					<span>{{ mainLinks[2].label }}</span>
				</component>
				<button
					type="button"
					class="flex cursor-pointer flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] transition hover:bg-zinc-800 active:scale-95"
					@click="isMenuOpen = true"
				>
					<NavMenuIcon />
					<span>Меню</span>
				</button>
			</div>
		</div>
	</nav>

	<div
		:class="[
			'fixed inset-0 z-50 md:hidden',
			isMenuOpen ? 'pointer-events-auto' : 'pointer-events-none'
		]"
	>
		<div
			:class="[
				'absolute inset-0 bg-black/50 transition-opacity duration-200',
				isMenuOpen ? 'opacity-100' : 'opacity-0'
			]"
			@click="isMenuOpen = false"
		/>

		<aside
			:class="[
				'absolute right-0 top-0 h-full w-[86%] max-w-sm border-l border-zinc-700 bg-zinc-900/98 p-4 shadow-2xl transition-transform duration-200',
				isMenuOpen ? 'translate-x-0' : 'translate-x-full'
			]"
		>
			<div class="mb-5 flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-900 p-3">
				<div>
					<p class="text-[11px] uppercase tracking-wide text-zinc-500">Навигация</p>
					<h3 class="text-base font-semibold text-white">Полное меню</h3>
				</div>
				<button
					type="button"
					class="cursor-pointer rounded-md p-2 text-zinc-300 transition hover:bg-zinc-800 active:scale-95"
					@click="isMenuOpen = false"
				>
					<CloseIcon />
				</button>
			</div>

			<div class="relative mb-4">
				<input
					type="text"
					placeholder="Поиск новел..."
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<SearchIcon class="pointer-events-none absolute right-2 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-300 [&>svg>path]:fill-current" />
			</div>

			<div class="space-y-2">
				<component
					v-for="link in fullMenuLinks"
					:key="link.label"
					:is="link.to ? RouterLink : 'a'"
					:to="link.to"
					:href="link.href"
					class="flex cursor-pointer select-none items-center justify-between rounded-lg border border-zinc-700/70 bg-zinc-900/70 px-3 py-2.5 text-sm text-zinc-200 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99]"
					@click="isMenuOpen = false"
				>
					<div class="flex items-center gap-2.5">
						<component :is="link.icon" class="text-zinc-300" />
						{{ link.label }}
					</div>
					<ChevronRightIcon class="text-zinc-500" />
				</component>
			</div>

			<div
				v-if="props.isAuthenticated"
				class="mt-4 flex items-center justify-between rounded-lg border border-zinc-700/70 bg-zinc-900/70 px-3 py-2.5"
			>
				<div class="flex items-center gap-2.5">
					<div
						class="flex h-9 w-9 items-center justify-center rounded-full text-sm font-semibold text-white"
						:class="props.user?.avatarColorClass || 'bg-zinc-700'"
					>
						{{ (props.user?.login || 'U').slice(0, 1).toUpperCase() }}
					</div>
					<div>
						<p class="text-sm font-medium text-zinc-200">{{ props.user?.login || 'Профиль' }}</p>
						<p class="text-xs text-zinc-500">Авторизован</p>
					</div>
				</div>

				<div class="relative rounded-md border border-zinc-700 bg-zinc-800 p-2 text-zinc-200">
					<NotificationBellIcon />
					<span
						v-if="props.hasUnreadNotifications"
						class="absolute right-1 top-1 h-2.5 w-2.5 rounded-full border border-zinc-900 bg-emerald-400"
					/>
				</div>
			</div>

			<button
				type="button"
				class="mt-4 flex w-full cursor-pointer items-center justify-between rounded-lg border border-zinc-700/70 bg-zinc-900/70 px-3 py-2.5 text-sm text-zinc-200 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99]"
				@click="toggleTheme"
			>
				<span>Тема: {{ isDark ? 'Тёмная' : 'Светлая' }}</span>
				<ChevronRightIcon class="text-zinc-500" />
			</button>

			<button
				v-if="!props.isAuthenticated"
				type="button"
				class="mt-5 w-full cursor-pointer rounded-lg bg-lime-300 px-4 py-2 text-sm font-semibold text-zinc-900 transition hover:bg-lime-200 active:scale-95"
				@click="openAuthFromMenu"
			>
				Войти
			</button>
			<button
				v-else
				type="button"
				class="mt-5 w-full cursor-pointer rounded-lg border border-zinc-700 bg-zinc-800 px-4 py-2 text-sm font-semibold text-zinc-200 transition hover:bg-zinc-700 active:scale-95"
				@click="handleLogout"
			>
				Выйти
			</button>
		</aside>
	</div>

	<AuthModal :open="isAuthModalOpen" @close="isAuthModalOpen = false" />
</template>
