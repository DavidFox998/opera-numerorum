import { test, expect } from "@playwright/test";
import {
  bootForgedSidecarFixture,
  cleanupForgedSidecarTmpDir,
  createForgedSidecarTmpDir,
  installForgedSidecarForwarders,
  payloadShaFor,
  writeForgedSidecar,
  type FixtureServer,
} from "./helpers/forged-sidecar-fixture.js";

/**
 * Task #222: end-to-end coverage for the per-referee filter on the
 * forged-sidecar "Recent dismissals" panel
 * (`panel-ledger-sidecar-forged-history`).
 *
 * The rebuild-history and re-roll-history panels each carry a referee
 * `<select>` whose selection mirrors into localStorage and survives a
 * reload — pinned by `history-referee-filter-persistence.spec.ts`
 * (task #197). The forged-sidecar dismissals panel gained the same
 * control (filter by `ackedBy`, persisted to
 * `lean-sidecar-forged-history-referee-filter`), but had no equivalent
 * coverage, so a refactor could silently drop it.
 *
 * This spec stands up a realistic two-operator dismissal history
 * (alice dismissed payload-v1, bob dismissed payload-v2) using the
 * shared forged-sidecar fixture, then drives the filter end-to-end:
 *
 *   1. Default state lists both rows ("2 of last 20").
 *   2. Pick "alice" → only her row renders, the count reads "1 of 2",
 *      and the selection is mirrored into localStorage.
 *   3. Reload → the persisted filter is still active (select + row).
 *   4. Click "clear" → both rows return, count is back to "2 of last
 *      20", and the localStorage key is wiped.
 *   5. Reload again → the panel is back to "all".
 *
 * Producing two DISTINCT referee rows mirrors the repeat-tamper flow
 * already exercised by `ledger-sidecar-forged-history-panel.spec.ts`:
 * forge v1 / ack as alice, re-forge with different bytes / ack as bob,
 * then re-forge the same v2 bytes so both ack files survive the final
 * restart and the rotating history log carries both dismissals.
 */

const REBUILD_TOKEN_STORAGE_KEY = "lean-rebuild-token";
const FORGED_HISTORY_FILTER_KEY = "lean-sidecar-forged-history-referee-filter";

const ALICE_TOKEN = "alice-named-token-fixture";
const BOB_TOKEN = "bob-named-token-fixture";
const ALICE_NAME = "alice";
const BOB_NAME = "bob";

const namedTokens = new Map<string, string | null>([
  [ALICE_TOKEN, ALICE_NAME],
  [BOB_TOKEN, BOB_NAME],
]);

test.describe(
  "dashboard: forged-sidecar dismissals referee filter (task #222)",
  () => {
    test("filter by referee narrows the rows, persists across reload, and clearing wipes the persisted value", async ({
      page,
    }) => {
      const { tmpDir, paths } = createForgedSidecarTmpDir(
        "ledger-forged-history-filter-e2e-",
      );
      const { lastOkPath } = paths;

      const markerV1 = "payload-v1-filter";
      const markerV2 = "payload-v2-filter-distinct";
      const shaV1 = payloadShaFor(markerV1);
      const shaV2 = payloadShaFor(markerV2);
      // Distinct bytes → distinct sha, so bob's ack lands a brand-new
      // history row rather than being deduped against alice's.
      expect(shaV1).not.toBe(shaV2);

      // --- Boot 1: forge payload-v1 ---
      writeForgedSidecar(lastOkPath, markerV1);
      let active: FixtureServer = await bootForgedSidecarFixture({
        paths,
        namedTokens,
      });

      try {
        await installForgedSidecarForwarders(page, () => active);

        // Seed alice's token before first render so the ack button
        // appears and the POST resolves to "alice".
        await page.addInitScript(
          ([key, token]) => {
            window.localStorage.setItem(key as string, token as string);
          },
          [REBUILD_TOKEN_STORAGE_KEY, ALICE_TOKEN],
        );

        await page.goto("/");

        const banner = page.locator(
          '[data-testid="panel-ledger-sidecar-forged"]',
        );
        await expect(banner).toBeVisible();

        // --- Ack #1: alice acks payload-v1 ---
        const ackButton = page.locator(
          '[data-testid="button-ack-ledger-sidecar-forged"]',
        );
        await expect(ackButton).toBeEnabled();
        await ackButton.click();
        await expect(banner).toHaveAttribute("data-acknowledged", "true");

        // --- Restart with payload-v2 (different bytes), ack as bob ---
        await active.close();
        writeForgedSidecar(lastOkPath, markerV2);
        active = await bootForgedSidecarFixture({ paths, namedTokens });

        await page.addInitScript(
          ([key, token]) => {
            window.localStorage.setItem(key as string, token as string);
          },
          [REBUILD_TOKEN_STORAGE_KEY, BOB_TOKEN],
        );
        await page.reload();

        await expect(banner).toBeVisible();
        await expect(banner).toHaveAttribute("data-acknowledged", "false");
        await expect(ackButton).toBeEnabled();
        await ackButton.click();
        await expect(banner).toHaveAttribute("data-acknowledged", "true");

        // --- Restart with the SAME v2 bytes so both ack files survive ---
        await active.close();
        writeForgedSidecar(lastOkPath, markerV2);
        active = await bootForgedSidecarFixture({ paths, namedTokens });
        await page.reload();
        await expect(banner).toBeVisible();

        const historyPanel = page.locator(
          '[data-testid="panel-ledger-sidecar-forged-history"]',
        );
        await expect(historyPanel).toBeVisible();

        const select = page.locator(
          '[data-testid="select-ledger-sidecar-forged-history-referee-filter"]',
        );
        const count = page.locator(
          '[data-testid="text-ledger-sidecar-forged-history-count"]',
        );
        const allRows = page.locator(
          '[data-testid^="row-ledger-sidecar-forged-history-"]',
        );

        // --- Default state: both dismissals listed, filter at "all" ---
        await expect(select).toBeVisible();
        await expect(select).toHaveValue("");
        await expect(count).toHaveText("2 of last 20");
        await expect(allRows).toHaveCount(2);
        // The select offers both operators as options.
        await expect(select.locator("option")).toHaveCount(3); // all + alice + bob

        // --- Pick alice → only her row renders ---
        await select.selectOption(ALICE_NAME);
        await expect(select).toHaveValue(ALICE_NAME);
        await expect(count).toHaveText("1 of 2");
        await expect(allRows).toHaveCount(1);
        await expect(
          page.locator(
            '[data-testid="row-ledger-sidecar-forged-history-0"]',
          ),
        ).toHaveAttribute("data-acked-by", ALICE_NAME);

        // The selection is mirrored into localStorage.
        await expect
          .poll(() =>
            page.evaluate(
              (k) => window.localStorage.getItem(k),
              FORGED_HISTORY_FILTER_KEY,
            ),
          )
          .toBe(ALICE_NAME);

        // --- Reload: persisted filter still active ---
        await page.reload();
        await expect(historyPanel).toBeVisible();
        await expect(select).toHaveValue(ALICE_NAME);
        await expect(count).toHaveText("1 of 2");
        await expect(allRows).toHaveCount(1);
        await expect(
          page.locator(
            '[data-testid="row-ledger-sidecar-forged-history-0"]',
          ),
        ).toHaveAttribute("data-acked-by", ALICE_NAME);

        // --- Clear: both rows return, persisted value wiped ---
        await page
          .locator(
            '[data-testid="button-ledger-sidecar-forged-history-clear-filter"]',
          )
          .click();
        await expect(select).toHaveValue("");
        await expect(count).toHaveText("2 of last 20");
        await expect(allRows).toHaveCount(2);
        await expect
          .poll(() =>
            page.evaluate(
              (k) => window.localStorage.getItem(k),
              FORGED_HISTORY_FILTER_KEY,
            ),
          )
          .toBeNull();

        // --- Reload again: back to "all" ---
        await page.reload();
        await expect(historyPanel).toBeVisible();
        await expect(select).toHaveValue("");
        await expect(count).toHaveText("2 of last 20");
        await expect(allRows).toHaveCount(2);
      } finally {
        await active.close();
        cleanupForgedSidecarTmpDir(tmpDir, paths);
      }
    });
  },
);
