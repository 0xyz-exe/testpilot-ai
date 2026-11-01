import json
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('testpilot.db')
cur = conn.cursor()

print("Seeding rich, realistic test execution & AI diagnosis data...")

# Clear existing
cur.execute("DELETE FROM artifacts")
cur.execute("DELETE FROM test_runs")
cur.execute("DELETE FROM test_cases")
cur.execute("DELETE FROM test_suites")
cur.execute("DELETE FROM projects")
cur.execute("DELETE FROM users")

now = datetime.utcnow()

# 1. Users
cur.execute("""
INSERT INTO users (id, email, password_hash, created_at, updated_at)
VALUES (1, 'secops@testpilot.ai', '$2b$12$e8wS.gWvj0M8cWbFjT4j3eXgLg1jVn2f.HwzU7O6vY7F3c8f8K0sO', ?, ?)
""", (now, now))

# 2. Projects
projects = [
    (1, 1, 'E-Commerce Storefront Platform', json.dumps(["https://staging.storefront.internal", "https://checkout.storefront.internal"]), json.dumps({"parallel_workers": 4, "default_timeout_ms": 30000, "retries": 1}), now, now),
    (2, 1, 'FinTech Auth & Identity Flow', json.dumps(["https://auth.fintech.lan", "https://id.fintech.lan"]), json.dumps({"parallel_workers": 2, "default_timeout_ms": 45000, "retries": 2}), now, now),
    (3, 1, 'Cloud SaaS Multi-Tenant Console', json.dumps(["https://admin.saas.internal"]), json.dumps({"parallel_workers": 2, "default_timeout_ms": 30000, "retries": 0}), now, now),
]
cur.executemany("INSERT INTO projects (id, user_id, name, allowed_urls, settings, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)", projects)

# 3. Test Suites
suites = [
    (1, 1, 'Authentication & Session Suite', 'Full sign-in, MFA challenge, OAuth2 token renewal, and sign-out flows', now, now),
    (2, 1, 'Shopping Cart & Checkout Suite', 'Product variant selection, inventory decrement, promo code, and Stripe payment tender', now, now),
    (3, 2, 'Biometric Passkey & 2FA TOTP', 'WebAuthn hardware key enrollment and time-based OTP step-up verification', now, now),
    (4, 3, 'Tenant RBAC & Audit Trails', 'Role boundary enforcement, workspace switching, and administrative mutation logs', now, now)
]
cur.executemany("INSERT INTO test_suites (id, project_id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", suites)

# 4. Test Cases
test_cases = [
    (
        1, 1, 'Login with valid credentials',
        """import { test, expect } from '@playwright/test';

test('user login with valid credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input#email', 'user@storefront.internal');
  await page.fill('input#password', 'P@ssw0rd2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('.user-avatar')).toBeVisible();
});""",
        json.dumps(["auth", "smoke", "p0", "regression"]),
        'approved', now, now
    ),
    (
        2, 1, 'Login with invalid password (error toast)',
        """import { test, expect } from '@playwright/test';

test('invalid credentials display error toast', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input#email', 'user@storefront.internal');
  await page.fill('input#password', 'WrongPassword!');
  await page.click('button.submit-btn');
  const alert = page.locator('[role=alert]');
  await expect(alert).toBeVisible();
  await expect(alert).toContainText('Invalid email or password');
});""",
        json.dumps(["auth", "negative", "p1"]),
        'approved', now, now
    ),
    (
        3, 2, 'Add multi-variant item to cart',
        """import { test, expect } from '@playwright/test';

test('add variant product to shopping bag', async ({ page }) => {
  await page.goto('/products/wireless-noise-cancelling-headphones');
  await page.click('button[data-color="matte-black"]');
  await page.click('button#add-to-cart');
  await expect(page.locator('#cart-drawer')).toBeVisible();
  await expect(page.locator('.cart-item-count')).toHaveText('1');
});""",
        json.dumps(["cart", "e2e", "p0"]),
        'approved', now, now
    ),
    (
        4, 2, 'Remove product from cart & recalculate tax (FLAKY)',
        """import { test, expect } from '@playwright/test';

test('remove cart item updates subtotal', async ({ page }) => {
  await page.goto('/cart');
  await page.click('.remove-item-btn');
  await page.waitForTimeout(500);
  await expect(page.locator('.cart-empty-message')).toBeVisible();
});""",
        json.dumps(["cart", "flaky", "p1"]),
        'approved', now, now
    ),
    (
        5, 3, 'Biometric passkey authentication step-up',
        """import { test, expect } from '@playwright/test';

test('passkey authentication step-up verification', async ({ page }) => {
  await page.goto('/auth/step-up');
  await page.click('button#verify-passkey');
  await expect(page.locator('.auth-success-badge')).toBeVisible();
});""",
        json.dumps(["security", "passkey", "p0"]),
        'approved', now, now
    )
]
cur.executemany("INSERT INTO test_cases (id, suite_id, title, code, tags, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", test_cases)

# 5. Test Runs
runs = [
    (
        1, 1, 'FAILED', 3240,
        'Timeout 30000ms exceeded waiting for selector "button[type=submit]"\n=========================== logs ===========================\nwaiting for locator("button[type=submit]")\n  locator resolved to hidden element\n  attempted click action timed out after 30000ms',
        'Chromium 130.0.6723.58', '1.48.2', 1,
        now - timedelta(minutes=4), now - timedelta(minutes=4) + timedelta(milliseconds=3240)
    ),
    (
        2, 2, 'PASSED', 1850,
        None,
        'Chromium 130.0.6723.58', '1.48.2', 0,
        now - timedelta(minutes=15), now - timedelta(minutes=15) + timedelta(milliseconds=1850)
    ),
    (
        3, 3, 'PASSED', 2410,
        None,
        'Firefox 131.0.3', '1.48.2', 0,
        now - timedelta(minutes=32), now - timedelta(minutes=32) + timedelta(milliseconds=2410)
    ),
    (
        4, 4, 'FLAKY', 4120,
        'AssertionError: Expected element .cart-empty-message to be visible within 5000ms. DOM Mutation race condition during async recalculation.',
        'WebKit 18.0 (Safari engine)', '1.48.2', 2,
        now - timedelta(hours=1), now - timedelta(hours=1) + timedelta(milliseconds=4120)
    ),
    (
        5, 5, 'PASSED', 2920,
        None,
        'Chromium 130.0.6723.58', '1.48.2', 0,
        now - timedelta(hours=2), now - timedelta(hours=2) + timedelta(milliseconds=2920)
    ),
    (
        6, 1, 'PASSED', 2780,
        None,
        'Chromium 130.0.6723.58', '1.48.2', 0,
        now - timedelta(hours=4), now - timedelta(hours=4) + timedelta(milliseconds=2780)
    )
]
cur.executemany("""
INSERT INTO test_runs (id, test_id, status, duration_ms, error_message, browser_version, playwright_version, retry_count, created_at, completed_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", runs)

# 6. Artifacts
artifacts = [
    (1, 1, 'screenshot', 'artifacts/runs/run_1/failure_selector_timeout.png', 184520, now - timedelta(minutes=4)),
    (2, 1, 'trace', 'artifacts/runs/run_1/playwright_trace.zip', 1420800, now - timedelta(minutes=4)),
    (3, 1, 'console_log', 'artifacts/runs/run_1/browser_console.log', 4512, now - timedelta(minutes=4)),
    (4, 1, 'network_log', 'artifacts/runs/run_1/network_har.json', 89240, now - timedelta(minutes=4)),
    (5, 4, 'screenshot', 'artifacts/runs/run_4/flaky_race_condition.png', 156300, now - timedelta(hours=1)),
]
cur.executemany("INSERT INTO artifacts (id, run_id, type, file_path, file_size, created_at) VALUES (?, ?, ?, ?, ?, ?)", artifacts)

conn.commit()
conn.close()
print("Database seed complete: 1 user, 3 projects, 4 suites, 5 tests, 6 runs, 5 artifacts.")
