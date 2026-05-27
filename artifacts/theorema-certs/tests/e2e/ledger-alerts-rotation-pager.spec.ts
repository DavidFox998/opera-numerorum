import { test, expect, type Route, type Page } from "@playwright/test";

/**
 * Task #136: end-to-end coverage for the rotated-archive pager added by
 * task #120 to the Recent ledger alerts panel.
 *
 * The pager lets operators switch between the live alert log
 * (`data/ledger-alerts.jsonl`) and rotated archives (`.1`, `.2`, …).
 * The backend half (the `rotation` query param + `availableRotations`
 * response field on `GET /api/lean/ledger-alerts`) is covered by
 * `artifacts/api-server/src/routes/lean.integration.test.ts`, but the
 * dashboard click-through is not exercised end-to-end. A regression in
 * the pager wiring (e.g. the .1 button stops sending `rotation=1`, or
 * the read-only hint stops appearing, or the Dismiss button keeps
 * rendering in archive mode) would ship silently.
 *
 * Selectors under test (artifacts/theorema-certs/src/pages/dashboard.tsx):
 *   - panel-ledger-alerts-rotations
 *   - btn-ledger-alerts-rotation-0           (live)
 *   - btn-ledger-alerts-rotation-1 / -2      (archives)
 *   - text-ledger-alerts-rotation-hint
 *   - button-dismiss-ledger-alert-<i>
 */

const LEDGER_ALERTS_URL = "**/api/lean/ledger-alerts*";
const REFEREE_TOKEN_URL = "**/api/lean/referee-token*";

interface RotationFixture {
  index: number;
  size: number;
  mtime: string;
}

interface AlertsFixture {
  rotation: number;
  alertId: string;
  workflow: string;
  message: string;
  availableRotations: RotationFixture[];
}

function buildAlertsResponse(fx: AlertsFixture) {
  return {
    alerts: [
      {
        id: fx.alertId,
        acknowledgedAt: null,
        timestamp: new Date("2026-05-27T12:00:00Z").toISOString(),
        workflow: fx.workflow,
        message: fx.message,
        failureMode: "live_prefix_sha_mismatch",
        recovery: null,
        hitsPath: "data/hits.txt",
        checkpointPath: "data/hits.txt.checkpoint",
        expectedSize: 1024,
        actualSize: 1024,
        expectedSha:
          "0000000000000000000000000000000000000000000000000000000000000000",
        source: "kernel._verify_checkpoint",
        delivery: {
          webhook: { status: "ok", error: null, inflight: 0, cap: 8 },
          email: { status: "ok", error: null, inflight: 0, cap: 8 },
        },
      },
    ],
    limit: 50,
    totalReturned: 1,
    logPath:
      fx.rotation === 0
        ? "data/ledger-alerts.jsonl"
        : `data/ledger-alerts.jsonl.${fx.rotation}`,
    logExists: true,
    ackGcDropped: 0,
    rotation: fx.rotation,
    availableRotations: fx.availableRotations,
  };
}

const AVAILABLE_ROTATIONS: RotationFixture[] = [
  { index: 1, size: 4096, mtime: "2026-05-26T12:00:00Z" },
  { index: 2, size: 2048, mtime: "2026-05-25T12:00:00Z" },
];

function fixtureForRotation(rotation: number): AlertsFixture {
  if (rotation === 0) {
    return {
      rotation: 0,
      alertId: "live-alert-id",
      workflow: "zeta-burst-live",
      message: "Live alert — checkpoint sha mismatch on the live log",
      availableRotations: AVAILABLE_ROTATIONS,
    };
  }
  return {
    rotation,
    alertId: `archive-${rotation}-alert-id`,
    workflow: `zeta-archive-${rotation}`,
    message: `Archived alert from rotation .${rotation} — checkpoint sha mismatch`,
    availableRotations: AVAILABLE_ROTATIONS,
  };
}

async function installAlertsRouter(page: Page): Promise<void> {
  await page.route(LEDGER_ALERTS_URL, async (route: Route) => {
    const url = new URL(route.request().url());
    const rotationParam = url.searchParams.get("rotation") ?? "0";
    const rotation = Number.parseInt(rotationParam, 10) || 0;
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(buildAlertsResponse(fixtureForRotation(rotation))),
    });
  });
}

async function installRefereeTokenMock(page: Page): Promise<void> {
  // The Dismiss button only renders when `rebuildToken` is truthy in the
  // dashboard state. The dashboard reads it from localStorage via the
  // referee-token panel; we set it directly so the live view actually
  // shows the Dismiss button (and we can prove the archive view hides it).
  await page.addInitScript(() => {
    window.localStorage.setItem("lean-rebuild-token", "test-token");
    window.localStorage.setItem("lean-rebuild-referee-name", "playwright");
  });
  await page.route(REFEREE_TOKEN_URL, async (route: Route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ ok: true }),
    });
  });
}

test.describe("dashboard: ledger alerts rotated-archive pager", () => {
  test("switching between live and rotated archives swaps entries, hides Dismiss, and shows the read-only hint", async ({
    page,
  }) => {
    await installRefereeTokenMock(page);
    await installAlertsRouter(page);
    await page.goto("/");

    const panel = page.locator('[data-testid="panel-ledger-alerts"]');
    await expect(panel).toBeVisible();

    // --- Live (rotation=0) state ---
    const pager = page.locator(
      '[data-testid="panel-ledger-alerts-rotations"]',
    );
    await expect(pager).toBeVisible();

    const liveButton = page.locator(
      '[data-testid="btn-ledger-alerts-rotation-0"]',
    );
    const rot1Button = page.locator(
      '[data-testid="btn-ledger-alerts-rotation-1"]',
    );
    const rot2Button = page.locator(
      '[data-testid="btn-ledger-alerts-rotation-2"]',
    );
    await expect(liveButton).toBeVisible();
    await expect(rot1Button).toBeVisible();
    await expect(rot2Button).toBeVisible();

    const message = page.locator('[data-testid="text-ledger-alert-message-0"]');
    await expect(message).toContainText("Live alert");

    // In live mode the hint advertises how many archives are available,
    // and the Dismiss button is visible (we set a referee token above).
    const hint = page.locator(
      '[data-testid="text-ledger-alerts-rotation-hint"]',
    );
    await expect(hint).toContainText("2 rotated archives available");
    await expect(hint).not.toContainText("read-only archive");

    const dismiss = page.locator(
      '[data-testid="button-dismiss-ledger-alert-0"]',
    );
    await expect(dismiss).toBeVisible();

    // --- Click .1: archive mode ---
    await rot1Button.click();
    await expect(message).toContainText("Archived alert from rotation .1");
    await expect(hint).toContainText("read-only archive");
    await expect(hint).toContainText("acknowledgements are disabled");
    await expect(dismiss).toHaveCount(0);

    // --- Click .2: still archive mode, swaps to the other fixture ---
    await rot2Button.click();
    await expect(message).toContainText("Archived alert from rotation .2");
    await expect(hint).toContainText("read-only archive");
    await expect(dismiss).toHaveCount(0);

    // --- Click live: back to live entries, Dismiss returns ---
    await liveButton.click();
    await expect(message).toContainText("Live alert");
    await expect(hint).toContainText("2 rotated archives available");
    await expect(hint).not.toContainText("read-only archive");
    await expect(dismiss).toBeVisible();
  });
});
