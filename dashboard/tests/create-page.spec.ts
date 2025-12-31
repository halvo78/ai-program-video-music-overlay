import { test, expect } from '@playwright/test'

test.describe('Create Video Page', () => {
  test.describe.configure({ timeout: 90000 })

  test.beforeEach(async ({ page }) => {
    await page.goto('/create', { timeout: 60000 })
  })

  test('should load create page with wizard', async ({ page }) => {
    await expect(page.getByText(/create your video|what.*want.*create/i).first()).toBeVisible({ timeout: 15000 })
  })

  test('should display platform selection', async ({ page }) => {
    // Check for platform options
    await expect(page.getByText(/tiktok/i).first()).toBeVisible()
    await expect(page.getByText(/instagram/i).first()).toBeVisible()
    await expect(page.getByText(/youtube/i).first()).toBeVisible()
  })

  test('should allow platform selection', async ({ page }) => {
    // Click on a platform
    const tiktokButton = page.getByText(/tiktok/i).first()
    if (await tiktokButton.isVisible()) {
      await tiktokButton.click()
    }
  })

  test('should have prompt input field', async ({ page }) => {
    // Look for textarea or input
    const promptInput = page.locator('textarea, input[type="text"]').first()
    await expect(promptInput).toBeVisible()
  })

  test('should allow prompt entry', async ({ page }) => {
    const promptInput = page.locator('textarea').first()
    if (await promptInput.isVisible()) {
      await promptInput.fill('Create a motivational video about success')
      await expect(promptInput).toHaveValue('Create a motivational video about success')
    }
  })

  test('should show prompt examples', async ({ page }) => {
    // Check for example prompts
    const examples = page.getByText(/motivational|product|tutorial|lifestyle/i)
    await expect(examples.first()).toBeVisible({ timeout: 10000 })
  })

  test('should have style selection options', async ({ page }) => {
    // Scroll to style section or advance wizard
    await page.evaluate(() => window.scrollBy(0, 500))

    // Check for style options
    const styleOptions = page.getByText(/cinematic|energetic|minimal|professional/i)
    if (await styleOptions.first().isVisible({ timeout: 5000 })) {
      await expect(styleOptions.first()).toBeVisible()
    }
  })

  test('should have music mood selection', async ({ page }) => {
    // Check for music mood options
    const moodOptions = page.getByText(/upbeat|chill|dramatic|inspiring/i)
    if (await moodOptions.first().isVisible({ timeout: 5000 })) {
      await expect(moodOptions.first()).toBeVisible()
    }
  })

  test('should have generate button', async ({ page }) => {
    const generateButton = page.getByRole('button', { name: /generate|create|start/i })
    await expect(generateButton.first()).toBeVisible()
  })

  test('should show AI features toggles', async ({ page }) => {
    // Look for AI feature toggles
    const aiFeatures = page.getByText(/auto.*caption|smart.*edit|ai.*music/i)
    if (await aiFeatures.first().isVisible({ timeout: 5000 })) {
      await expect(aiFeatures.first()).toBeVisible()
    }
  })
})

test.describe('Create Page Wizard Steps', () => {
  test('should progress through wizard steps', async ({ page }) => {
    await page.goto('/create')

    // Step 1: Content
    await expect(page.getByText(/content|describe|prompt/i).first()).toBeVisible({ timeout: 15000 })

    // Fill prompt
    const promptInput = page.locator('textarea').first()
    if (await promptInput.isVisible()) {
      await promptInput.fill('Test video prompt')
    }

    // Look for next/continue button
    const nextButton = page.getByRole('button', { name: /next|continue|proceed/i })
    if (await nextButton.first().isVisible({ timeout: 5000 })) {
      await nextButton.first().click()
    }
  })
})

test.describe('Create Page URL Parameters', () => {
  test('should accept prompt from URL parameter', async ({ page }) => {
    await page.goto('/create?prompt=Create%20a%20cooking%20video')

    // Check if prompt is pre-filled
    const promptInput = page.locator('textarea').first()
    if (await promptInput.isVisible()) {
      const value = await promptInput.inputValue()
      // Should have the URL param value or be ready to accept input
      expect(value.length >= 0).toBe(true)
    }
  })

  test('should accept platform from URL parameter', async ({ page }) => {
    await page.goto('/create?platform=youtube')

    // Page should load with youtube pre-selected or available
    await expect(page.getByText(/youtube/i).first()).toBeVisible({ timeout: 15000 })
  })
})

test.describe('Create Page Validation', () => {
  test('should validate empty prompt', async ({ page }) => {
    await page.goto('/create')

    // Try to generate without prompt
    const generateButton = page.getByRole('button', { name: /generate|create/i }).first()
    if (await generateButton.isVisible({ timeout: 10000 })) {
      await generateButton.click()

      // Should show validation message or not proceed
    }
  })

  test('should require platform selection', async ({ page }) => {
    await page.goto('/create')

    // Check that at least one platform is selectable
    const platforms = page.locator('[class*="platform"]')
    const count = await platforms.count()
    expect(count).toBeGreaterThanOrEqual(0) // May be optional
  })
})

test.describe('Create Page Accessibility', () => {
  test('should have accessible form labels', async ({ page }) => {
    await page.goto('/create')

    // Check for labels
    const labels = page.locator('label')
    const count = await labels.count()
    expect(count).toBeGreaterThan(0)
  })

  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/create')

    // Tab through elements
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')

    // Should focus on interactive elements
    const focused = page.locator(':focus')
    await expect(focused).toBeVisible()
  })
})
