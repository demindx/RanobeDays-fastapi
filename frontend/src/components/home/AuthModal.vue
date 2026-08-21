<script setup>
import { reactive, ref, watch } from 'vue'
import { useAuth } from '../../composables/useAuth'
import { getEmailValidationError } from '../../utils/validateEmail'
import AppButton from '../shared/AppButton.vue'
import AppInput from '../shared/AppInput.vue'
import AppModal from '../shared/AppModal.vue'
import AppSectionSwitchTransition from '../shared/AppSectionSwitchTransition.vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close'])

const mode = ref('login')
const loginError = ref('')
const registerError = ref('')
const isSubmitting = ref(false)
const { login, register } = useAuth()

const loginForm = reactive({
  login: '',
  password: '',
})

const registerForm = reactive({
  login: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const registerErrors = reactive({
  email: '',
})
const isEmailFocused = ref(false)
const isEmailTouched = ref(false)

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

const handleRegisterSubmit = async () => {
  isEmailTouched.value = true
  registerError.value = ''
  if (!validateRegisterEmail({ strict: true })) return
  if (registerForm.password !== registerForm.confirmPassword) {
    registerError.value = 'Пароли не совпадают.'
    return
  }

  isSubmitting.value = true
  const result = await register(registerForm.login, registerForm.email, registerForm.password)
  isSubmitting.value = false
  if (!result.ok) {
    registerError.value = result.error
    return
  }
  registerForm.login = ''
  registerForm.email = ''
  registerForm.password = ''
  registerForm.confirmPassword = ''
  emit('close')
}

const handleLoginSubmit = async () => {
  loginError.value = ''
  isSubmitting.value = true
  const result = await login(loginForm.login, loginForm.password)
  isSubmitting.value = false
  if (!result.ok) {
    loginError.value = result.error
    return
  }
  loginForm.login = ''
  loginForm.password = ''
  emit('close')
}

watch(
  () => props.open,
  (next) => {
    if (!next) {
      mode.value = 'login'
      loginError.value = ''
      registerError.value = ''
      registerErrors.email = ''
      isEmailFocused.value = false
      isEmailTouched.value = false
    }
  },
)
</script>

<template>
  <AppModal :open="props.open" @close="emit('close')">
    <div class="mb-4 flex items-center justify-between gap-3">
      <h3 class="text-base font-semibold text-white sm:text-lg">
        {{ mode === 'login' ? 'Войти в аккаунт' : 'Регистрация' }}
      </h3>
      <AppButton variant="neutral" size="sm" class="shrink-0 text-zinc-300" @click="emit('close')">
        Закрыть
      </AppButton>
    </div>

    <AppSectionSwitchTransition>
      <form
        v-if="mode === 'login'"
        key="login"
        class="space-y-3"
        @submit.prevent="handleLoginSubmit"
      >
        <AppInput
          v-model="loginForm.login"
          type="text"
          placeholder="Логин"
          @input="loginError = ''"
        />
        <AppInput
          v-model="loginForm.password"
          type="password"
          placeholder="Пароль"
          @input="loginError = ''"
        />
        <p v-if="loginError" class="text-xs text-red-400">{{ loginError }}</p>
        <AppButton
          type="submit"
          variant="primary"
          block
          class="font-semibold"
          :disabled="isSubmitting"
        >
          Войти
        </AppButton>
      </form>

      <form
        v-else
        key="register"
        novalidate
        class="space-y-3"
        @submit.prevent="handleRegisterSubmit"
      >
        <AppInput v-model="registerForm.login" type="text" placeholder="Логин" />
        <div class="relative">
          <AppInput
            v-model="registerForm.email"
            type="text"
            placeholder="Почта"
            :class="registerErrors.email ? 'border-red-400 focus:border-red-400' : ''"
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
        <AppInput v-model="registerForm.password" type="password" placeholder="Пароль" />
        <AppInput
          v-model="registerForm.confirmPassword"
          type="password"
          placeholder="Повторите пароль"
        />
        <p v-if="registerError" class="text-xs text-red-400">{{ registerError }}</p>
        <AppButton
          type="submit"
          variant="primary"
          block
          class="font-semibold"
          :disabled="isSubmitting"
        >
          Зарегистрироваться
        </AppButton>
      </form>
    </AppSectionSwitchTransition>

    <div class="mt-4 border-t border-zinc-800 pt-4 text-center">
      <AppButton
        variant="neutral"
        class="text-sm text-zinc-300"
        @click="mode = mode === 'login' ? 'register' : 'login'"
      >
        {{ mode === 'login' ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти' }}
      </AppButton>
    </div>
  </AppModal>
</template>
