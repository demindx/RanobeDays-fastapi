import { expect, test } from '@playwright/test'

const viewports = [
  { width: 320, height: 568, label: '320x568' },
  { width: 360, height: 800, label: '360x800' },
  { width: 390, height: 844, label: '390x844' },
  { width: 768, height: 1024, label: '768x1024' },
  { width: 1024, height: 1366, label: '1024x1366' },
  { width: 1280, height: 800, label: '1280+' },
]

const assertNoHorizontalOverflow = async (page, route) => {
  await page.goto(route)
  await page.waitForLoadState('networkidle')

  const metrics = await page.evaluate(() => ({
    htmlScrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    viewportWidth: window.innerWidth,
  }))

  expect(metrics.htmlScrollWidth, `${route} html overflow`).toBeLessThanOrEqual(metrics.viewportWidth + 1)
  expect(metrics.bodyScrollWidth, `${route} body overflow`).toBeLessThanOrEqual(metrics.viewportWidth + 1)
}

test('layout has no horizontal overflow across required breakpoints', async ({ page }) => {
  const routes = ['/', '/catalog', '/novel/solo-leveling']

  for (const viewport of viewports) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height })

    for (const route of routes) {
      await assertNoHorizontalOverflow(page, route)
    }
  }
})

test('mobile header and bottom nav do not overlap the content start/end', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const spacing = await page.evaluate(() => {
    const main = document.querySelector('#main-content')
    if (!main) return null

    const style = window.getComputedStyle(main)
    return {
      paddingTop: Number.parseFloat(style.paddingTop || '0'),
      paddingBottom: Number.parseFloat(style.paddingBottom || '0'),
    }
  })

  expect(spacing).not.toBeNull()
  expect(spacing.paddingTop).toBeGreaterThanOrEqual(60)
  expect(spacing.paddingBottom).toBeGreaterThanOrEqual(70)
})

test('mobile navigation links are visible and clickable', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  await expect(page.getByRole('link', { name: 'Каталог' })).toBeVisible()
  await page.getByRole('link', { name: 'Каталог' }).click()
  await expect(page).toHaveURL(/\/catalog/)

  await page.getByRole('link', { name: 'Открыть главную' }).first().click()
  await expect(page).toHaveURL(/\/$/)
})

test('homepage sections fit in mobile layout', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 568 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  await expect(page.getByRole('heading', { name: 'Продолжить чтение', exact: true })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Новые главы сегодня' })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Последние обновления' })).toBeVisible()

  const measurements = await page.evaluate(() => {
    const root = document.querySelector('.home-page__layout')
    const sections = Array.from(document.querySelectorAll('.home-section'))
    if (!root || sections.length < 3) return null

    const get = (el) => ({
      left: el.getBoundingClientRect().left,
      right: el.getBoundingClientRect().right,
    })

    return {
      root: get(root),
      sections: sections.map((section) => get(section)),
      viewport: window.innerWidth,
    }
  })

  expect(measurements).not.toBeNull()
  expect(measurements.root.left, 'root left bound').toBeGreaterThanOrEqual(0)
  expect(measurements.root.right, 'root right bound').toBeLessThanOrEqual(measurements.viewport + 1)
  for (const [index, section] of measurements.sections.entries()) {
    expect(section.left, `section ${index} left bound`).toBeGreaterThanOrEqual(0)
    expect(section.right, `section ${index} right bound`).toBeLessThanOrEqual(measurements.viewport + 1)
  }
})

test('new chapters row scrolls on desktop and mobile', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  await page.waitForSelector('.hero-carousel__viewport', { timeout: 10000 })

  const viewport = page.locator('.hero-carousel__viewport').first()
  await expect(viewport).toBeVisible()

  const desktopScrollBefore = await viewport.evaluate((el) => el.scrollLeft)
  await viewport.evaluate((el) => {
    el.scrollBy({ left: 260 })
  })
  const desktopScrollAfter = await viewport.evaluate((el) => el.scrollLeft)
  expect(desktopScrollAfter).toBeGreaterThan(desktopScrollBefore)

  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  await page.waitForSelector('.hero-carousel__viewport', { timeout: 10000 })
  const mobileViewport = page.locator('.hero-carousel__viewport').first()
  const box = await mobileViewport.boundingBox()
  expect(box).not.toBeNull()

  const mobileScrollBefore = await mobileViewport.evaluate((el) => el.scrollLeft)
  await page.mouse.move(box.x + box.width * 0.7, box.y + box.height * 0.5)
  await page.mouse.down()
  await page.mouse.move(box.x + box.width * 0.25, box.y + box.height * 0.5, { steps: 8 })
  await page.mouse.up()
  await page.waitForTimeout(180)
  const mobileScrollAfter = await mobileViewport.evaluate((el) => el.scrollLeft)
  expect(mobileScrollAfter).toBeGreaterThanOrEqual(mobileScrollBefore)
})
