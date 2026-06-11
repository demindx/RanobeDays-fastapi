export function getEmailValidationError(rawEmail, { strict = true } = {}) {
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

export function validateEmail(email, { strict = true } = {}) {
  return !getEmailValidationError(email, { strict })
}
