<script setup>
	import { reactive, ref, watch } from 'vue'

	const props = defineProps({
		open: {
			type: Boolean,
			default: false
		}
	})

	const emit = defineEmits(['close'])

	const mode = ref('login')

	const loginForm = reactive({
		login: '',
		password: ''
	})

	const registerForm = reactive({
		login: '',
		email: '',
		password: '',
		confirmPassword: ''
	})

	const registerErrors = reactive({
		email: ''
	})
	const isEmailFocused = ref(false)
	const isEmailTouched = ref(false)

	const getEmailValidationError = (rawEmail, { strict = true } = {}) => {
		const email = rawEmail.trim()
		if (!email) {
			return strict ? 'Введите email.' : ''
		}
		if (email.includes(' ')) {
			return 'Email не должен содержать пробелы.'
		}

		const atCount = (email.match(/@/g) || []).length
		if (atCount === 0) {
			return 'В email должен быть символ @.'
		}
		if (atCount > 1) {
			return 'В email может быть только один символ @.'
		}

		const [localPart, domainPart] = email.split('@')
		if (!localPart) {
			return 'Перед @ укажите имя почтового ящика.'
		}
		if (!domainPart) {
			return 'После @ укажите домен.'
		}
		if (domainPart.startsWith('.') || domainPart.endsWith('.')) {
			return 'Домен не может начинаться или заканчиваться точкой.'
		}
		if (!domainPart.includes('.')) {
			return 'Добавьте домен верхнего уровня, например: mail.ru.'
		}
		if (domainPart.split('.').some((part) => !part)) {
			return 'В домене пропущена часть между точками.'
		}
		if (!/^[A-Za-z0-9._%+-]+$/.test(localPart)) {
			return 'Недопустимые символы в части до @.'
		}
		if (!/^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(domainPart)) {
			return 'Некорректный формат домена.'
		}

		return ''
	}

	const validateRegisterEmail = ({ strict = true } = {}) => {
		registerErrors.email = getEmailValidationError(registerForm.email, { strict })
		return !registerErrors.email
	}

	const handleRegisterEmailInput = () => {
		isEmailTouched.value = true
		validateRegisterEmail({ strict: false })
	}

	const handleRegisterEmailBlur = () => {
		isEmailFocused.value = false
		validateRegisterEmail({ strict: true })
	}

	const handleRegisterSubmit = () => {
		isEmailTouched.value = true
		validateRegisterEmail({ strict: true })
	}

	watch(
		() => props.open,
		(next) => {
			if (!next) {
				mode.value = 'login'
				registerErrors.email = ''
				isEmailFocused.value = false
				isEmailTouched.value = false
			}
		}
	)
</script>

<template>
	<div
		v-if="props.open"
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/65 px-3 py-4 sm:px-4 sm:py-6"
		@click.self="emit('close')"
	>
		<div class="w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5">
			<div class="mb-4 flex items-center justify-between gap-3">
				<h3 class="text-base font-semibold text-white sm:text-lg">
					{{ mode === 'login' ? 'Войти в аккаунт' : 'Регистрация' }}
				</h3>
				<button
					type="button"
					class="shrink-0 rounded-md px-2 py-1 text-xs text-zinc-400 transition hover:bg-zinc-800 hover:text-white active:scale-95 sm:text-sm"
					@click="emit('close')"
				>
					Закрыть
				</button>
			</div>

			<form v-if="mode === 'login'" class="space-y-3" @submit.prevent>
				<input
					v-model="loginForm.login"
					type="text"
					placeholder="Логин"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<input
					v-model="loginForm.password"
					type="password"
					placeholder="Пароль"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<button
					type="submit"
					class="w-full rounded-lg bg-lime-300 px-4 py-2 text-sm font-semibold text-zinc-900 transition hover:bg-lime-200 active:scale-95"
				>
					Войти
				</button>
			</form>

			<form v-else novalidate class="space-y-3" @submit.prevent="handleRegisterSubmit">
				<input
					v-model="registerForm.login"
					type="text"
					placeholder="Логин"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<div class="relative">
					<input
						v-model="registerForm.email"
						type="text"
						placeholder="Почта"
						:class="[
							'w-full rounded-lg border bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition',
							registerErrors.email ? 'border-red-400 focus:border-red-400' : 'border-zinc-700 focus:border-lime-300'
						]"
						@focus="isEmailFocused = true"
						@blur="handleRegisterEmailBlur"
						@input="handleRegisterEmailInput"
					/>
					<div
						v-if="registerErrors.email && (isEmailFocused || isEmailTouched)"
						class="pointer-events-none absolute left-0 top-full z-10 mt-1 max-w-full rounded-md border border-red-300/60 bg-red-500/95 px-2 py-1 text-xs text-white shadow-lg"
					>
						{{ registerErrors.email }}
					</div>
				</div>
				<input
					v-model="registerForm.password"
					type="password"
					placeholder="Пароль"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<input
					v-model="registerForm.confirmPassword"
					type="password"
					placeholder="Повторите пароль"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<button
					type="submit"
					class="w-full rounded-lg bg-lime-300 px-4 py-2 text-sm font-semibold text-zinc-900 transition hover:bg-lime-200 active:scale-95"
				>
					Зарегистрироваться
				</button>
			</form>

			<div class="mt-4 border-t border-zinc-800 pt-4 text-center">
				<button
					type="button"
					class="text-sm text-zinc-300 transition hover:text-white active:scale-95"
					@click="mode = mode === 'login' ? 'register' : 'login'"
				>
					{{ mode === 'login' ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти' }}
				</button>
			</div>
		</div>
	</div>
</template>
