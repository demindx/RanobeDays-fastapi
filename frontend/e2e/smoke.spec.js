import { test, expect } from '@playwright/test'

test('home page renders and navigates to catalog', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByRole('heading', { name: 'Ранобэ', exact: true })).toBeVisible()
  await page.getByRole('link', { name: 'Каталог' }).first().click()

  await expect(page).toHaveURL(/\/catalog/)
  await expect(page.getByRole('heading', { name: 'Каталог' })).toBeVisible()
})

test('unknown route shows not found page', async ({ page }) => {
  await page.goto('/definitely-not-found')

  await expect(page.getByRole('heading', { name: '404' })).toBeVisible()
  await expect(page.getByText('Страница не найдена.')).toBeVisible()
})
