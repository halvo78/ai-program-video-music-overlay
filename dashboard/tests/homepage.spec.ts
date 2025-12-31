import { test, expect } from '@playwright/test'

test.describe('Taj Chat Homepage', () => {
  test.describe.configure({ timeout: 90000 })

  test('should load the homepage with hero section', async ({ page }) => {
    await page.goto('/')

    // Check for main hero elements
    await expect(page.getByText('Create Videos')).toBeVisible({ timeout: 15000 })
    await expect(page.getByText('Without Limits')).toBeVisible()
  })

  test('should display navigation menu', async ({ page }) => {
    await page.goto('/')

    // Check for navigation items
    await expect(page.locator('nav')).toBeVisible()
    await expect(page.getByText('AI Features').first()).toBeVisible()
    await expect(page.getByText('Platforms').first()).toBeVisible()
  })

  test('should show video gallery section', async ({ page }) => {
    await page.goto('/')

    // Scroll to gallery section
    await page.evaluate(() => window.scrollBy(0, 800))

    // Check for video cards
    const videoCards = page.locator('[class*="video-card"], [class*="card"]')
    await expect(videoCards.first()).toBeVisible({ timeout: 10000 })
  })

  test('should display trust badges', async ({ page }) => {
    await page.goto('/')

    // Check for trust elements
    await expect(page.getByText(/videos created|creators/i).first()).toBeVisible()
  })

  test('should have working CTA buttons', async ({ page }) => {
    await page.goto('/')

    // Check for CTA buttons
    const createButton = page.getByRole('link', { name: /start creating|create|get started/i }).first()
    await expect(createButton).toBeVisible()
  })

  test('should display stats section', async ({ page }) => {
    await page.goto('/')

    // Scroll to stats
    await page.evaluate(() => window.scrollBy(0, 1500))

    // Look for statistics
    await expect(page.getByText(/million|M\+|countries|creators/i).first()).toBeVisible({ timeout: 10000 })
  })

  test('should have footer with links', async ({ page }) => {
    await page.goto('/')

    // Scroll to footer
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))

    await expect(page.locator('footer')).toBeVisible()
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')

    // Should still show main content
    await expect(page.getByText('Create Videos')).toBeVisible({ timeout: 15000 })
  })

  test('should load without console errors', async ({ page }) => {
    const errors: string[] = []
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text())
      }
    })

    await page.goto('/')
    await page.waitForTimeout(2000)

    // Filter out expected development warnings
    const criticalErrors = errors.filter(e =>
      !e.includes('hydration') &&
      !e.includes('Warning') &&
      !e.includes('DevTools')
    )

    expect(criticalErrors.length).toBe(0)
  })
})

test.describe('Navigation Tests', () => {
  test('should navigate to create page from hero CTA', async ({ page }) => {
    await page.goto('/')

    const createLink = page.getByRole('link', { name: /start creating|create your first video/i }).first()
    if (await createLink.isVisible()) {
      await createLink.click()
      await expect(page).toHaveURL(/\/create/, { timeout: 15000 })
    }
  })

  test('should navigate to pricing page', async ({ page }) => {
    await page.goto('/')

    const pricingLink = page.getByRole('link', { name: /pricing/i }).first()
    if (await pricingLink.isVisible()) {
      await pricingLink.click()
      await expect(page).toHaveURL(/\/pricing/, { timeout: 15000 })
    }
  })

  test('should navigate to templates page', async ({ page }) => {
    await page.goto('/')

    const templatesLink = page.getByRole('link', { name: /templates/i }).first()
    if (await templatesLink.isVisible()) {
      await templatesLink.click()
      await expect(page).toHaveURL(/\/templates/, { timeout: 15000 })
    }
  })
})

test.describe('Interaction Tests', () => {
  test('should show auth modal on sign in click', async ({ page }) => {
    await page.goto('/')

    const signInButton = page.getByRole('button', { name: /sign in|log in/i }).first()
    if (await signInButton.isVisible()) {
      await signInButton.click()

      // Modal should appear
      await expect(page.getByText(/welcome back|create your account/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should handle video card interactions', async ({ page }) => {
    await page.goto('/')

    // Find a video card
    const videoCard = page.locator('[class*="video"], [class*="card"]').first()
    if (await videoCard.isVisible()) {
      await videoCard.hover()
      // Should show hover state elements
    }
  })
})

test.describe('Performance Tests', () => {
  test('should load within acceptable time', async ({ page }) => {
    const startTime = Date.now()
    await page.goto('/')
    await page.waitForLoadState('domcontentloaded')
    const loadTime = Date.now() - startTime

    // Should load within 5 seconds
    expect(loadTime).toBeLessThan(5000)
  })

  test('should have correct meta tags', async ({ page }) => {
    await page.goto('/')

    // Check meta tags
    const title = await page.title()
    expect(title).toContain('Taj Chat')

    const description = page.locator('meta[name="description"]')
    await expect(description).toHaveAttribute('content', /.+/)
  })
})
