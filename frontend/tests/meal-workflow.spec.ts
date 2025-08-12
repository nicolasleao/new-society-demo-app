import { test, expect } from '@playwright/test';

test.describe('Meal Management Workflow', () => {
  let username = 'test-user-123'; // Will be overridden with timestamp in beforeEach
  const testMeal = {
    title: 'Test Meal for E2E',
    carbs: '50.5',
    proteins: '25.3',
    fats: '15.7',
    calories: '425'
  };

  test.beforeEach(async ({ page }) => {
    // Start fresh for each test by using a unique username
    const timestamp = Date.now();
    username = `test-user-${timestamp}`;
    
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('should complete full meal workflow: login → create → delete', async ({ page }) => {
    // Step 1: Login as test user
    await test.step('Login with test username', async () => {
      await page.goto('/');
      
      // Verify we're on the login page
      await expect(page.locator('h1')).toContainText('Calory Tracker');
      await expect(page.locator('input[placeholder="Enter your username"]')).toBeVisible();
      
      // Enter username and submit
      await page.fill('input[placeholder="Enter your username"]', username);
      await page.click('button[type="submit"]');
      
      // Verify redirect to dashboard
      await expect(page).toHaveURL('/dashboard');
      await expect(page.locator(`text=Welcome, ${username}`)).toBeVisible();
    });

    // Step 2: Create a new meal
    await test.step('Create a new meal', async () => {
      // Verify meal form is visible
      await expect(page.locator('h2', { hasText: 'Add New Meal' })).toBeVisible();
      
      // Fill out the meal form
      await page.fill('input[id="title"]', testMeal.title);
      await page.fill('input[id="carbs"]', testMeal.carbs);
      await page.fill('input[id="proteins"]', testMeal.proteins);
      await page.fill('input[id="fats"]', testMeal.fats);
      await page.fill('input[id="calories"]', testMeal.calories);
      
      // Submit the form
      await page.click('button[type="submit"]');
      
      // Wait for the meal to appear in the table (indicating successful submission)
      await expect(page.locator('td', { hasText: testMeal.title }).first()).toBeVisible();
      
      // Verify the meal appears in the table
      await expect(page.locator('table')).toBeVisible();
      await expect(page.locator('td', { hasText: testMeal.title }).first()).toBeVisible();
      await expect(page.locator('td', { hasText: testMeal.carbs }).first()).toBeVisible();
      await expect(page.locator('td', { hasText: testMeal.proteins }).first()).toBeVisible();
      await expect(page.locator('td', { hasText: testMeal.fats }).first()).toBeVisible();
      await expect(page.locator('td', { hasText: testMeal.calories }).first()).toBeVisible();
      
      // Verify the stats are updated - use more specific locator
      await expect(page.locator('[data-testid="stats-section"], .bg-red-50 .text-sm.text-gray-600').first()).toBeVisible();
    });

    // Step 3: Delete the meal
    await test.step('Delete the created meal', async () => {
      // Find and click the delete button for our test meal
      const mealRow = page.locator('tr', { has: page.locator('td', { hasText: testMeal.title }) }).first();
      await expect(mealRow).toBeVisible();
      
      const deleteButton = mealRow.locator('button', { hasText: 'Delete' });
      await deleteButton.click();
      
      // Verify confirmation modal appears
      await expect(page.locator('h3', { hasText: 'Delete Meal' })).toBeVisible();
      await expect(page.locator('text=Are you sure you want to delete this meal?')).toBeVisible();
      
      // Confirm deletion
      await page.locator('button', { hasText: 'Delete' }).last().click();
      
      // Verify the meal is removed from the table
      await expect(page.locator('td', { hasText: testMeal.title })).not.toBeVisible();
      
      // Verify we see the "No meals found" message if no other meals exist
      const mealRows = page.locator('tbody tr');
      const rowCount = await mealRows.count();
      
      if (rowCount === 1) {
        // Only the "No meals found" row should exist
        await expect(page.locator('text=No meals found. Add your first meal above!')).toBeVisible();
      }
    });

    // Step 4: Verify logout functionality
    await test.step('Logout and verify redirect', async () => {
      await page.click('button', { hasText: 'Logout' });
      
      // Verify redirect to login page
      await expect(page).toHaveURL('/');
      await expect(page.locator('h1')).toContainText('Calory Tracker');
      await expect(page.locator('input[placeholder="Enter your username"]')).toBeVisible();
    });
  });

  test('should handle meal form validation', async ({ page }) => {
    // Login first
    await page.goto('/');
    await page.fill('input[placeholder="Enter your username"]', username);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');

    await test.step('Verify form requires meal title', async () => {
      // Try to submit empty form
      await page.click('button[type="submit"]');
      
      // Form should not submit without title (required field)
      await expect(page.locator('input[id="title"]')).toBeFocused();
    });

    await test.step('Verify numeric inputs accept valid values', async () => {
      await page.fill('input[id="title"]', 'Validation Test Meal');
      await page.fill('input[id="carbs"]', '10.5');
      await page.fill('input[id="proteins"]', '20.3');
      await page.fill('input[id="fats"]', '5.1');
      await page.fill('input[id="calories"]', '180');
      
      await page.click('button[type="submit"]');
      
      // Wait for the meal to appear in the table (indicating successful submission)
      await expect(page.locator('td', { hasText: 'Validation Test Meal' }).first()).toBeVisible();
      
      // Clean up: delete the meal we just created
      const deleteButton = page.locator('tr', { has: page.locator('td', { hasText: 'Validation Test Meal' }) })
        .locator('button', { hasText: 'Delete' }).first();
      await deleteButton.click();
      await page.locator('button', { hasText: 'Delete' }).last().click();
    });
  });

  test('should display stats correctly', async ({ page }) => {
    // Login first
    await page.goto('/');
    await page.fill('input[placeholder="Enter your username"]', username);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');

    await test.step('Verify stats display components', async () => {
      // Check that stats section is visible (might initially show "No meals logged today")
      await expect(page.locator('h2', { hasText: "Today's Summary" })).toBeVisible();
      
      // Either shows actual stats or no meals message - use try/catch to handle multiple elements
      try {
        const hasStatsData = await page.locator('.bg-red-50 .text-sm.text-gray-600').isVisible();
        expect(hasStatsData).toBeTruthy();
      } catch {
        const hasNoMealsMessage = await page.locator('text=No meals logged today').isVisible();
        expect(hasNoMealsMessage).toBeTruthy();
      }
    });

    await test.step('Verify stats update after adding meal', async () => {
      // Add a meal with known values
      await page.fill('input[id="title"]', 'Stats Test Meal');
      await page.fill('input[id="carbs"]', '30');
      await page.fill('input[id="proteins"]', '20');
      await page.fill('input[id="fats"]', '10');
      await page.fill('input[id="calories"]', '280');
      
      await page.click('button[type="submit"]');
      
      // Wait for the meal to appear in table
      await expect(page.locator('td', { hasText: 'Stats Test Meal' })).toBeVisible();
      
      // The stats should show updated values now - use more specific locators
      await expect(page.locator('.bg-red-50 .text-sm.text-gray-600').first()).toBeVisible();
      await expect(page.locator('.bg-blue-50 .text-sm.text-gray-600').first()).toBeVisible();
      await expect(page.locator('.bg-green-50 .text-sm.text-gray-600').first()).toBeVisible();
      await expect(page.locator('.bg-yellow-50 .text-sm.text-gray-600').first()).toBeVisible();
      
      // Clean up
      const deleteButton = page.locator('tr', { has: page.locator('td', { hasText: 'Stats Test Meal' }) })
        .locator('button', { hasText: 'Delete' }).first();
      await deleteButton.click();
      await page.locator('button', { hasText: 'Delete' }).last().click();
    });
  });

  test('should handle date filter functionality', async ({ page }) => {
    // Login first
    await page.goto('/');
    await page.fill('input[placeholder="Enter your username"]', username);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/dashboard');

    await test.step('Verify date filter options', async () => {
      const dateFilter = page.locator('select');
      await expect(dateFilter).toBeVisible();
      
      // Check default value
      await expect(dateFilter).toHaveValue('today');
      
      // Change to "All time"
      await dateFilter.selectOption('');
      await expect(dateFilter).toHaveValue('');
      
      // Change back to "Today"
      await dateFilter.selectOption('today');
      await expect(dateFilter).toHaveValue('today');
    });
  });
});
