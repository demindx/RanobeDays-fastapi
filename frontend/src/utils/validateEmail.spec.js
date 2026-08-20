import { describe, it, expect } from 'vitest'
import { validateEmail, getEmailValidationError } from './validateEmail'

describe('validateEmail', () => {
  it('accepts valid emails', () => {
    expect(validateEmail('user@example.com')).toBe(true)
    expect(validateEmail('a.b+c@mail.ru')).toBe(true)
  })

  it('rejects invalid emails', () => {
    expect(validateEmail('')).toBe(false)
    expect(validateEmail('a b@c.ru')).toBe(false)
    expect(validateEmail('a@b')).toBe(false)
    expect(validateEmail('a@b@c.ru')).toBe(false)
  })
})

describe('getEmailValidationError', () => {
  it('returns message for empty input in strict mode', () => {
    expect(getEmailValidationError('')).toBe('Введите email.')
  })

  it('returns empty string for empty input in non-strict mode', () => {
    expect(getEmailValidationError('', { strict: false })).toBe('')
  })

  it('returns empty string for a valid email', () => {
    expect(getEmailValidationError('user@example.com')).toBe('')
  })
})
