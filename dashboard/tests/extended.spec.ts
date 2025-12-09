import { test, expect } from '@playwright/test'

test.describe('Taj Chat Deep Flows', () => {
  test.describe.configure({ timeout: 120000 })

  test('studio page shows key panels and tracks', async ({ page }) => {
    await page.goto('/studio', { timeout: 60000, waitUntil: 'domcontentloaded' })

    await expect(page.getByRole('button', { name: 'Assets', exact: true }).first()).toBeVisible()
    await expect(page.getByRole('button', { name: 'Effects', exact: true }).first()).toBeVisible()
    await expect(page.getByRole('button', { name: 'Text', exact: true }).first()).toBeVisible()
    await expect(page.getByRole('button', { name: 'AI', exact: true }).first()).toBeVisible()

    await expect(page.getByText('Video', { exact: true }).last()).toBeVisible()
    await expect(page.getByText('Music', { exact: true }).last()).toBeVisible()
    await expect(page.getByText('Voice', { exact: true }).last()).toBeVisible()
  })

  test('commissioning page shows hero and stats', async ({ page }) => {
    await page.goto('/commissioning', { timeout: 60000, waitUntil: 'domcontentloaded' })

    await expect(page.getByRole('heading', { name: 'Commissioning', exact: true }).first()).toBeVisible()
    await expect(page.getByText('System Commissioning')).toBeVisible()
    const runFull = page.getByText('Run Full Commission', { exact: true }).first()
    await runFull.scrollIntoViewIfNeeded()
    await expect(runFull).toBeVisible({ timeout: 15000 })
    await expect(page.getByText('Export Report', { exact: true })).toBeVisible()
  })

  test('templates page shows filters and cards', async ({ page }) => {
    await page.goto('/templates', { timeout: 60000, waitUntil: 'domcontentloaded' })

    await expect(page.getByRole('heading', { name: 'Templates', exact: true }).first()).toBeVisible()
    const allTemplates = page.getByText('All Templates', { exact: true }).first()
    await allTemplates.scrollIntoViewIfNeeded()
    await expect(allTemplates).toBeVisible({ timeout: 10000 })
    await expect(page.getByRole('button', { name: /Trending/i }).first()).toBeVisible()
    await expect(page.getByText('New', { exact: true })).toBeVisible()
  })
})

