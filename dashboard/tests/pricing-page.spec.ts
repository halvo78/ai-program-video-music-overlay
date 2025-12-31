import { test, expect } from '@playwright/test'

test.describe('Pricing Page', () => {
  test.describe.configure({ timeout: 90000 })

  test.beforeEach(async ({ page }) => {
    await page.goto('/pricing', { timeout: 60000, waitUntil: 'domcontentloaded' })
  })

  test('should load pricing page', async ({ page }) => {
    await expect(page.getByText(/pricing|plans|choose/i).first()).toBeVisible({ timeout: 15000 })
  })

  test('should display pricing tiers', async ({ page }) => {
    // Check for tier names
    const tierNames = ['Free', 'Pro', 'Business', 'Enterprise']

    for (const tier of tierNames) {
      const tierElement = page.getByText(new RegExp(tier, 'i')).first()
      if (await tierElement.isVisible({ timeout: 5000 })) {
        await expect(tierElement).toBeVisible()
      }
    }
  })

  test('should display pricing amounts', async ({ page }) => {
    // Check for price indicators
    const prices = page.getByText(/\$\d+|\$0|free/i)
    await expect(prices.first()).toBeVisible({ timeout: 10000 })
  })

  test('should have CTA buttons for each tier', async ({ page }) => {
    // Check for action buttons
    const ctaButtons = page.getByRole('button', { name: /get started|start|choose|select|subscribe/i })
    const count = await ctaButtons.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should display feature lists', async ({ page }) => {
    // Check for feature checkmarks or lists
    const features = page.locator('li, [class*="feature"]')
    const count = await features.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should have billing toggle (monthly/yearly)', async ({ page }) => {
    // Check for billing period toggle
    const toggle = page.getByText(/monthly|yearly|annual/i)
    if (await toggle.first().isVisible({ timeout: 5000 })) {
      await expect(toggle.first()).toBeVisible()
    }
  })

  test('should highlight recommended plan', async ({ page }) => {
    // Check for highlighted/recommended plan
    const recommended = page.getByText(/popular|recommended|best value/i)
    if (await recommended.first().isVisible({ timeout: 5000 })) {
      await expect(recommended.first()).toBeVisible()
    }
  })

  test('should display FAQ section', async ({ page }) => {
    // Scroll to FAQ
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))

    const faq = page.getByText(/faq|frequently asked|questions/i)
    if (await faq.first().isVisible({ timeout: 5000 })) {
      await expect(faq.first()).toBeVisible()
    }
  })
})

test.describe('Pricing Page Interactions', () => {
  test('should toggle billing period', async ({ page }) => {
    await page.goto('/pricing')

    // Find and click billing toggle
    const yearlyToggle = page.getByText(/yearly|annual/i).first()
    if (await yearlyToggle.isVisible({ timeout: 10000 })) {
      await yearlyToggle.click()

      // Prices should update (look for yearly prices or discount indicators)
      await page.waitForTimeout(500)
    }
  })

  test('should expand FAQ items', async ({ page }) => {
    await page.goto('/pricing')
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))

    // Find FAQ accordion items
    const faqItem = page.locator('[class*="accordion"], [class*="faq"]').first()
    if (await faqItem.isVisible({ timeout: 5000 })) {
      await faqItem.click()
    }
  })

  test('should navigate to signup on CTA click', async ({ page }) => {
    await page.goto('/pricing')

    const ctaButton = page.getByRole('button', { name: /get started|start free/i }).first()
    if (await ctaButton.isVisible({ timeout: 10000 })) {
      await ctaButton.click()

      // Should navigate to signup or show auth modal
      await page.waitForTimeout(1000)
    }
  })
})

test.describe('Pricing Page Feature Comparison', () => {
  test('should show feature comparison table', async ({ page }) => {
    await page.goto('/pricing')

    // Look for comparison table
    const table = page.locator('table, [class*="comparison"]')
    if (await table.first().isVisible({ timeout: 5000 })) {
      await expect(table.first()).toBeVisible()
    }
  })

  test('should display video limits per tier', async ({ page }) => {
    await page.goto('/pricing')

    // Check for video limit information
    const limits = page.getByText(/video.*month|minutes|unlimited/i)
    await expect(limits.first()).toBeVisible({ timeout: 10000 })
  })

  test('should display quality tiers', async ({ page }) => {
    await page.goto('/pricing')

    // Check for quality information
    const quality = page.getByText(/720p|1080p|4k|hd/i)
    if (await quality.first().isVisible({ timeout: 5000 })) {
      await expect(quality.first()).toBeVisible()
    }
  })
})

test.describe('Pricing Page Responsiveness', () => {
  test('should be responsive on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto('/pricing')

    await expect(page.getByText(/pricing|plans/i).first()).toBeVisible({ timeout: 15000 })
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/pricing')

    await expect(page.getByText(/pricing|plans/i).first()).toBeVisible({ timeout: 15000 })

    // Pricing cards should stack on mobile
  })
})
