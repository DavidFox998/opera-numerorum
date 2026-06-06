#!/usr/bin/env node
/**
 * upload_morning_star_to_drive.js
 * Opera Numerorum — upload (or re-upload) the Morning Star ZIP to Google Drive
 * and patch certificates/invariants.json with the new/current drive_url.
 *
 * Called automatically by make_morning_star_zip.sh after a successful rebuild.
 * Uses the Replit Google Drive connector (conn_google-drive_*).
 *
 * Upload strategy (handles large files):
 *   1. Initiate a resumable upload session via the Replit proxy (tiny metadata-only POST).
 *   2. The response returns a googleapis.com session URL (self-authenticating).
 *   3. PUT the full file directly to that URL — no size limit through proxy.
 *   4. If newly created: set "anyone-can-read" permission (fatal if it fails).
 *   5. Patch certificates/invariants.json with drive_url + drive_file_id.
 *
 * Existing-file reuse: prefer bundle_morning_star.drive_file_id from invariants.json;
 * fall back to parsing drive_url if drive_file_id is absent.
 *
 * Create-new fallback: if PATCH of existing file fails, POST creates a new file in the
 * configured Drive folder (DRIVE_FOLDER_ID below, also recorded in invariants.json
 * under bundle_morning_star.drive_folder_id).
 */

"use strict";

const fs   = require("fs");
const path = require("path");

const CERT_DIR        = path.join(__dirname);
const ZIP_PATH        = path.join(CERT_DIR, "MorningStar_Complete_2026_06_04.zip");
const INVARIANTS      = path.join(CERT_DIR, "invariants.json");
const PROXY_BASE      = "https://connectors.replit.com/api/v2/proxy";
const CONNECTOR_NAME  = "google-drive";
const ZIP_MIME        = "application/zip";
const ZIP_NAME        = "MorningStar_Complete_2026_06_04.zip";

// Stable Drive folder that holds the Morning Star ZIP.
// Determined by querying Drive for the existing file's parents.
const DRIVE_FOLDER_ID = "1vWDb3k6zUI1vOtby5U0AB5ntac-4H_Y1";

async function getProxyHeaders() {
  const { ReplitConnectors } = require("@replit/connectors-sdk");
  const connectors = new ReplitConnectors();
  return await connectors.getProxyHeaders(CONNECTOR_NAME);
}

/**
 * Initiate a resumable upload session via the Replit proxy.
 * Returns the session URI (direct googleapis.com URL, self-authenticating).
 * @param {string|null} fileId  Existing Drive file ID (PATCH) or null (POST/create).
 * @param {object}      authHeaders
 */
async function initiateResumableSession(fileId, authHeaders) {
  const metadata = fileId
    ? JSON.stringify({ name: ZIP_NAME, mimeType: ZIP_MIME })
    : JSON.stringify({ name: ZIP_NAME, mimeType: ZIP_MIME, parents: [DRIVE_FOLDER_ID] });

  const proxyPath = fileId
    ? `/upload/drive/v3/files/${fileId}?uploadType=resumable&fields=id,name,webViewLink`
    : `/upload/drive/v3/files?uploadType=resumable&fields=id,name,webViewLink`;
  const method = fileId ? "PATCH" : "POST";

  const resp = await fetch(PROXY_BASE + proxyPath, {
    method,
    headers: {
      ...authHeaders,
      "Content-Type":          "application/json",
      "X-Upload-Content-Type": ZIP_MIME,
    },
    body: metadata,
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`Failed to initiate resumable session (${resp.status}): ${text.slice(0, 300)}`);
  }

  const sessionUri = resp.headers.get("location") || resp.headers.get("Location");
  if (!sessionUri) {
    throw new Error("No Location header in resumable initiation response");
  }
  return sessionUri;
}

/**
 * Upload file content to the self-authenticating resumable session URI.
 * Returns the completed file metadata { id, name, webViewLink }.
 */
async function uploadToSessionUri(sessionUri, fileBuffer) {
  const resp = await fetch(sessionUri, {
    method:  "PUT",
    headers: {
      "Content-Type":   ZIP_MIME,
      "Content-Length": String(fileBuffer.length),
    },
    body: fileBuffer,
  });

  const text = await resp.text().catch(() => "");
  if (!resp.ok) {
    throw new Error(`Resumable upload PUT failed (${resp.status}): ${text.slice(0, 300)}`);
  }

  let parsed;
  try { parsed = JSON.parse(text); } catch (_) { parsed = {}; }
  return parsed;
}

/**
 * Set file to public reader permission via the proxy.
 * Throws if Drive returns a non-2xx status (permission failure is fatal).
 */
async function setPublicPermission(fileId, authHeaders) {
  const body = JSON.stringify({ role: "reader", type: "anyone" });
  const resp = await fetch(PROXY_BASE + `/drive/v3/files/${fileId}/permissions`, {
    method:  "POST",
    headers: { ...authHeaders, "Content-Type": "application/json" },
    body,
  });
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(
      `Failed to set public permission on ${fileId} (${resp.status}): ${text.slice(0, 200)}`
    );
  }
  return resp.status;
}

/** Extract Drive file ID from a webViewLink or share URL. */
function extractFileIdFromUrl(driveUrl) {
  if (!driveUrl) return null;
  const m = driveUrl.match(/\/file\/d\/([^/?]+)/);
  return m ? m[1] : null;
}

function webViewToShareLink(fileId) {
  return `https://drive.google.com/file/d/${fileId}/view?usp=drivesdk`;
}

async function main() {
  console.log("=== upload_morning_star_to_drive.js ===");

  if (!fs.existsSync(ZIP_PATH)) {
    console.error(`ERROR: ZIP not found at ${ZIP_PATH}`);
    process.exit(1);
  }

  const inv    = JSON.parse(fs.readFileSync(INVARIANTS, "utf8"));
  const bundle = inv["bundle_morning_star"] || {};

  // Prefer drive_file_id field; fall back to parsing drive_url.
  const existingId =
    bundle["drive_file_id"] ||
    extractFileIdFromUrl(bundle["drive_url"] || null);

  console.log(`  ZIP: ${ZIP_PATH}`);
  console.log(`  Drive folder: ${DRIVE_FOLDER_ID}`);
  console.log(`  existing Drive file ID: ${existingId || "(none)"}`);

  const fileBuffer  = fs.readFileSync(ZIP_PATH);
  console.log(`  read ${fileBuffer.length} bytes (${(fileBuffer.length / 1024 / 1024).toFixed(1)} MB)`);

  const authHeaders = await getProxyHeaders();
  let fileMeta      = null;
  let isNew         = false;

  if (existingId) {
    console.log(`  initiating resumable PATCH for existing file ${existingId} ...`);
    try {
      const sessionUri = await initiateResumableSession(existingId, authHeaders);
      console.log("  session URI obtained; uploading ...");
      fileMeta = await uploadToSessionUri(sessionUri, fileBuffer);
      console.log("  PATCH upload complete");
    } catch (err) {
      console.log(`  PATCH failed: ${err.message}`);
      console.log("  falling back to POST (create new file in configured folder) ...");
    }
  }

  if (!fileMeta) {
    console.log(`  initiating resumable POST (new file in folder ${DRIVE_FOLDER_ID}) ...`);
    const sessionUri = await initiateResumableSession(null, authHeaders);
    console.log("  session URI obtained; uploading ...");
    fileMeta = await uploadToSessionUri(sessionUri, fileBuffer);
    isNew    = true;
    console.log(`  POST upload complete; new file ID: ${fileMeta.id}`);
  }

  const fileId = fileMeta.id || existingId;
  if (!fileId) {
    console.error("  ERROR: could not determine Drive file ID from upload response");
    console.error("  response:", JSON.stringify(fileMeta));
    process.exit(1);
  }

  if (isNew) {
    console.log("  setting public reader permission (required for shareable link) ...");
    // Throws if non-2xx — we do not patch invariants unless permission is confirmed.
    const permStatus = await setPublicPermission(fileId, authHeaders);
    console.log(`  permission set (${permStatus})`);
  }

  const driveUrl = fileMeta.webViewLink || webViewToShareLink(fileId);
  console.log(`  Drive URL: ${driveUrl}`);

  // Patch invariants — only reached if upload + permission both succeeded.
  inv["bundle_morning_star"]["drive_url"]       = driveUrl;
  inv["bundle_morning_star"]["drive_file_id"]   = fileId;
  inv["bundle_morning_star"]["drive_folder_id"] = DRIVE_FOLDER_ID;

  fs.writeFileSync(INVARIANTS, JSON.stringify(inv, null, 2) + "\n", "utf8");
  console.log("  invariants.json patched: drive_url, drive_file_id, drive_folder_id");
  console.log("=== done ===");
}

main().catch(err => {
  console.error("FATAL:", err);
  process.exit(1);
});
