import { test, expect } from '@playwright/test'

test.describe('Taj Chat Dashboard', () => {
  test.describe.configure({ timeout: 90000 })
  test('should load the dashboard page', async ({ page }) => {
    await page.goto('/')

    // Check for main elements
    await expect(page.locator('text=Taj Chat')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Create Video' }).first()).toBeVisible()
  })

  test('should navigate to create page', async ({ page }) => {
    await page.goto('/', { timeout: 60000 })

    // Click on Create Video button
    const createLink = page.locator('a[href="/create"]').first()
    await createLink.click({ timeout: 15000 })
    await expect(page).toHaveURL(/\/create$/, { timeout: 15000 })
    await expect(page.getByRole('heading', { name: 'Create Your Video' })).toBeVisible()
  })

  test('should navigate to agents page', async ({ page }) => {
    await page.goto('/agents', { timeout: 60000 })

    // Check for agents
    await expect(page.getByRole('heading', { name: 'AI Agents' })).toBeVisible()
    await expect(page.locator('text=Content Analysis Agent')).toBeVisible()
    await expect(page.locator('text=Video Generation Agent')).toBeVisible()
  })

  test('should navigate to gallery page', async ({ page }) => {
    await page.goto('/gallery', { timeout: 60000, waitUntil: 'domcontentloaded' })

    // Check for gallery elements
    await expect(page.getByRole('heading', { name: 'Gallery' })).toBeVisible()
  })

  test('should navigate to social page', async ({ page }) => {
    await page.goto('/social', { timeout: 60000, waitUntil: 'domcontentloaded' })

    // Check for social hub elements
    await expect(page.getByRole('heading', { name: 'Social Hub' })).toBeVisible()
    await expect(page.locator('text=Connected Platforms')).toBeVisible()
  })

  test('should navigate to analytics page', async ({ page }) => {
    await page.goto('/analytics', { timeout: 60000, waitUntil: 'domcontentloaded' })

    // Check for analytics elements
    await expect(page.getByRole('heading', { name: 'Analytics' })).toBeVisible()
    await expect(page.getByText('Total Views')).toBeVisible()
  })

  test('should navigate to settings page', async ({ page }) => {
    await page.goto('/settings', { timeout: 60000, waitUntil: 'domcontentloaded' })

    // Check for settings elements
    await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible()
    await expect(page.locator('text=API Keys')).toBeVisible()
  })

  test('should show system status in sidebar', async ({ page }) => {
    await page.goto('/')

    // Check for system status
    await expect(page.locator('text=System Online')).toBeVisible()
    await expect(page.locator('text=10 Agents Ready')).toBeVisible()
  })

  test('should allow selecting platforms in create page', async ({ page }) => {
    await page.goto('/create')

    // Check platform buttons exist
    await expect(page.locator('text=TikTok')).toBeVisible()
    await expect(page.locator('text=Instagram Reels')).toBeVisible()
    await expect(page.locator('text=YouTube Shorts')).toBeVisible()
    await expect(page.locator('text=Twitter/X')).toBeVisible()
  })

  test('should allow selecting workflow mode in create page', async ({ page }) => {
    await page.goto('/create')

    // Check workflow mode buttons exist
    await expect(page.locator('text=Hybrid')).toBeVisible()
    await expect(page.locator('text=Sequential')).toBeVisible()
    await expect(page.locator('text=Parallel')).toBeVisible()
  })
})
