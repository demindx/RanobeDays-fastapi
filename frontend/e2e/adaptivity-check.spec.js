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

test('form controls stack and fit in mobile layout', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 568 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const measurements = await page.evaluate(() => {
    const input = document.querySelector('.rd-field')
    const select = document.querySelector('.rd-select')
    const tags = document.querySelector('.rd-tag-select')
    if (!input || !select || !tags) return null

    const get = (el) => ({
      width: el.getBoundingClientRect().width,
      left: el.getBoundingClientRect().left,
      right: el.getBoundingClientRect().right,
    })

    return { input: get(input), select: get(select), tags: get(tags), viewport: window.innerWidth }
  })

  expect(measurements).not.toBeNull()
  for (const key of ['input', 'select', 'tags']) {
    expect(measurements[key].left, `${key} left bound`).toBeGreaterThanOrEqual(0)
    expect(measurements[key].right, `${key} right bound`).toBeLessThanOrEqual(measurements.viewport + 1)
  }
})

test('carousel reacts to wheel on desktop and drag on mobile', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  const viewport = page.locator('.hero-carousel__viewport').first()
  await expect(viewport).toBeVisible()

  const desktopTransformBefore = await page.locator('.hero-carousel__track').first().evaluate((el) =>
    window.getComputedStyle(el).transform,
  )
  await viewport.hover()
  await page.mouse.wheel(0, 450)
  await page.waitForTimeout(180)
  const desktopTransformAfter = await page.locator('.hero-carousel__track').first().evaluate((el) =>
    window.getComputedStyle(el).transform,
  )
  expect(desktopTransformAfter).not.toBe(desktopTransformBefore)

  await page.setViewportSize({ width: 390, height: 844 })
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  const mobileViewport = page.locator('.hero-carousel__viewport').first()
  const box = await mobileViewport.boundingBox()
  expect(box).not.toBeNull()

  const mobileTransformBefore = await page.locator('.hero-carousel__track').first().evaluate((el) =>
    window.getComputedStyle(el).transform,
  )
  await page.mouse.move(box.x + box.width * 0.7, box.y + box.height * 0.5)
  await page.mouse.down()
  await page.mouse.move(box.x + box.width * 0.25, box.y + box.height * 0.5, { steps: 8 })
  await page.mouse.up()
  await page.waitForTimeout(180)
  const mobileTransformAfter = await page.locator('.hero-carousel__track').first().evaluate((el) =>
    window.getComputedStyle(el).transform,
  )
  expect(mobileTransformAfter).not.toBe(mobileTransformBefore)
})
