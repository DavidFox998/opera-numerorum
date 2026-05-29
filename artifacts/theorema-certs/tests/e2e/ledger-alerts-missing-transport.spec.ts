import { test, expect, type Route } from "@playwright/test";

/**
 * Task #203: regression coverage for the dashboard crashing when a
 * ledger alert entry is missing one of the two delivery transports.
 *
 * The OpenAPI schema marks both `delivery.webhook` and
 * `delivery.email` as required, but the alert log is read straight
 * off on-disk JSONL written by older versions of the alerting kernel.
 * A legacy entry that ever shipped without one of the two transports
 * used to make the dashboard read `a.delivery.email.status` (and the
 * per-row `alert.delivery.email`) unconditionally, throwing
 * `Cannot read properties of undefined (reading 'status')` and
 * blanking out the whole `panel-ledger-alerts` body.
 *
 * This spec mocks `/api/lean/ledger-alerts*` with three entries that
 * each omit a transport (one missing `email`, one missing `webhook`,
 * one with the whole `delivery` object absent) and asserts the panel
 * still renders: rows are present, the missing transport falls back to
 * a neutral `not_configured` pill, and the present transport is shown
 * verbatim.
 */

const LEDGER_ALERTS_URL = "**/api/lean/ledger-alerts*";

function buildLegacyAlertsResponse() {
  const timestamp = new Date().toISOString();
  const baseFields = {
    acknowledgedAt: null,
    timestamp,
    workflow: "zeta-burst-101-10000",
    recovery: null,
    hitsPath: "data/hits.txt",
    checkpointPath: "data/hits.txt.checkpoint",
    expectedSize: 1024,
    actualSize: 1024,
    expectedSha:
      "0000000000000000000000000000000000000000000000000000000000000000",
    source: "kernel._verify_checkpoint",
    failureMode: "truncation",
  };
  return {
    alerts: [
      {
        ...baseFields,
        id: "legacy-missing-email",
        message: "Legacy entry written before the email transport existed",
        subject: "Legacy missing email transport",
        // delivery present but `email` absent
        delivery: {
          webhook: { status: "ok", error: null },
        },
      },
      {
        ...baseFields,
        id: "legacy-missing-webhook",
        message: "Legacy entry written before the webhook transport existed",
        subject: "Legacy missing webhook transport",
        // delivery present but `webhook` absent
        delivery: {
          email: { status: "failed", error: "smtp connect timeout" },
        },
      },
      {
        ...baseFields,
        id: "legacy-missing-delivery",
        message: "Legacy entry written before delivery tracking existed",
        subject: "Legacy missing delivery object",
        // whole delivery object absent
      },
    ],
    limit: 50,
    totalReturned: 3,
    logPath: "data/ledger-alerts.jsonl",
    logExists: true,
    ackGcDropped: 0,
    rotation: 0,
    availableRotations: [],
  };
}

async function installLedgerAlertsMock(
  page: import("@playwright/test").Page,
) {
  await page.route(LEDGER_ALERTS_URL, async (route: Route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(buildLegacyAlertsResponse()),
    });
  });
}

test.describe("dashboard: ledger alerts with missing delivery transports", () => {
  test("renders the alerts panel without crashing when entries omit a transport", async ({
    page,
  }) => {
    await installLedgerAlertsMock(page);

    await page.goto("/");

    // The panel body must render — before the fix, the unconditional
    // `a.delivery.email.status` deref threw and blanked the whole body.
    const panel = page.locator('[data-testid="panel-ledger-alerts"]');
    await expect(panel).toBeVisible();

    const counter = page.locator('[data-testid="text-ledger-alerts-count"]');
    await expect(counter).toBeVisible();
    await expect(counter).toContainText("3 entries");

    // All three legacy rows must be present.
    await expect(page.locator('[data-testid="row-ledger-alert-0"]')).toBeVisible();
    await expect(page.locator('[data-testid="row-ledger-alert-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="row-ledger-alert-2"]')).toBeVisible();

    // Row 0: webhook present (ok), email missing → neutral fallback.
    await expect(
      page.locator('[data-testid="text-ledger-alert-webhook-0"]'),
    ).toHaveText("webhook: ok");
    const email0 = page.locator('[data-testid="text-ledger-alert-email-0"]');
    await expect(email0).toHaveText("email: not_configured");
    await expect(email0).toHaveAttribute("data-status", "not_configured");

    // Row 1: webhook missing → neutral fallback, email present (failed).
    const webhook1 = page.locator(
      '[data-testid="text-ledger-alert-webhook-1"]',
    );
    await expect(webhook1).toHaveText("webhook: not_configured");
    await expect(webhook1).toHaveAttribute("data-status", "not_configured");
    await expect(
      page.locator('[data-testid="text-ledger-alert-email-1"]'),
    ).toHaveText("email: failed");

    // Row 2: whole delivery object missing → both fall back.
    await expect(
      page.locator('[data-testid="text-ledger-alert-webhook-2"]'),
    ).toHaveText("webhook: not_configured");
    await expect(
      page.locator('[data-testid="text-ledger-alert-email-2"]'),
    ).toHaveText("email: not_configured");
  });
});
