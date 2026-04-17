import { computed, reactive } from 'vue'

const AUTH_KEY = 'ranobe-auth'

const state = reactive({
	isAuthenticated: false,
	user: null,
	hasUnreadNotifications: false
})

const mockCredentials = {
	login: 'demo',
	password: 'demo123'
}

const saveState = () => {
	if (typeof window === 'undefined') return
	window.localStorage.setItem(
		AUTH_KEY,
		JSON.stringify({
			isAuthenticated: state.isAuthenticated,
			user: state.user,
			hasUnreadNotifications: state.hasUnreadNotifications
		})
	)
}

const restoreState = () => {
	if (typeof window === 'undefined') return
	const saved = window.localStorage.getItem(AUTH_KEY)
	if (!saved) return
	try {
		const parsed = JSON.parse(saved)
		state.isAuthenticated = !!parsed?.isAuthenticated
		state.user = parsed?.user ?? null
		state.hasUnreadNotifications = !!parsed?.hasUnreadNotifications
	} catch {
		state.isAuthenticated = false
		state.user = null
		state.hasUnreadNotifications = false
	}
}

restoreState()

const login = (loginValue, passwordValue) => {
	const loginNormalized = loginValue.trim()
	if (loginNormalized !== mockCredentials.login || passwordValue !== mockCredentials.password) {
		return {
			ok: false,
			error: `Неверный логин или пароль. Тестовые данные: ${mockCredentials.login} / ${mockCredentials.password}`
		}
	}

	state.isAuthenticated = true
	state.user = {
		login: 'DemoReader',
		avatarColorClass: 'bg-emerald-500'
	}
	state.hasUnreadNotifications = true
	saveState()

	return { ok: true }
}

const logout = () => {
	state.isAuthenticated = false
	state.user = null
	state.hasUnreadNotifications = false
	saveState()
}

export const useAuth = () => ({
	isAuthenticated: computed(() => state.isAuthenticated),
	user: computed(() => state.user),
	hasUnreadNotifications: computed(() => state.hasUnreadNotifications),
	mockCredentials,
	login,
	logout
})
