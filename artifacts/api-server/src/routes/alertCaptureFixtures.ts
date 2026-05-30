import http from "node:http";
import type { AddressInfo } from "node:net";
import express from "express";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";
import type {
  LedgerAlertInvocation,
  LedgerAlertSink,
} from "../lib/ledgerAlerts.js";

/**
 * Shared end-to-end alert-capture test fixtures.
 *
 * The integration suite proves several alert kinds (watchdog stall,
 * task #162; reroll digest, task #200; and future kinds) reach the wire
 * on BOTH the SMTP and webhook transports by spawning the real
 * `kernel.py` `_fire_ledger_alert` path against Node capture servers.
 * The captive SMTP server, captive HTTP webhook server, and the kernel
 * "wire sink" used to be copy-pasted per describe block — this module
 * is the single source of truth so a parser edge case or env-plumbing
 * fix only has to be made once.
 */

// Repo root, four levels up from `artifacts/api-server/src/routes/`.
export const REPO_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
  "..",
  "..",
  "..",
);

export interface WebhookCapture {
  server: http.Server;
  port: number;
  captured: Array<{ headers: Record<string, string>; body: string }>;
  close: () => Promise<void>;
}

export async function startWebhookCapture(): Promise<WebhookCapture> {
  const captured: Array<{
    headers: Record<string, string>;
    body: string;
  }> = [];
  const app = express();
  app.use(express.raw({ type: "*/*", limit: "1mb" }));
  app.post("/alert", (req, res) => {
    captured.push({
      headers: Object.fromEntries(
        Object.entries(req.headers).map(([k, v]) => [
          k,
          Array.isArray(v) ? v.join(",") : String(v ?? ""),
        ]),
      ),
      body: (req.body as Buffer).toString("utf-8"),
    });
    res.status(200).send("ok");
  });
  const server = http.createServer(app);
  await new Promise<void>((resolve) =>
    server.listen(0, "127.0.0.1", resolve),
  );
  const port = (server.address() as AddressInfo).port;
  return {
    server,
    port,
    captured,
    close: () =>
      new Promise<void>((resolve, reject) =>
        server.close((err) => (err ? reject(err) : resolve())),
      ),
  };
}

export interface SmtpCapture {
  port: number;
  messages: Array<{ raw: string; subject: string; body: string }>;
  close: () => Promise<void>;
}

// Minimal RFC-5321 sink: speaks just enough of EHLO / MAIL FROM /
// RCPT TO / DATA / QUIT for `smtplib.SMTP.send_message` (no auth,
// no STARTTLS — `_send_email` skips both when SMTP_USER is unset)
// to complete. Captures the DATA payload plus the parsed Subject
// header and body, decoding quoted-printable so assertions can match
// human-readable substrings even when the SMTP layer soft-wraps them
// across `=\r\n` breaks.
export async function startSmtpCapture(): Promise<SmtpCapture> {
  const net = await import("node:net");
  const messages: Array<{ raw: string; subject: string; body: string }> = [];
  const server = net.createServer((sock) => {
    sock.setEncoding("utf-8");
    let buf = "";
    let inData = false;
    let dataLines: string[] = [];
    const write = (line: string) => sock.write(line + "\r\n");
    write("220 mini.smtp ready");
    sock.on("data", (chunk: string) => {
      buf += chunk;
      let nl: number;
      while ((nl = buf.indexOf("\r\n")) >= 0) {
        const line = buf.slice(0, nl);
        buf = buf.slice(nl + 2);
        if (inData) {
          if (line === ".") {
            const raw = dataLines.join("\r\n");
            const headerEnd = raw.indexOf("\r\n\r\n");
            let subject = "";
            let body = "";
            if (headerEnd >= 0) {
              const headers = raw.slice(0, headerEnd);
              const rawBody = raw.slice(headerEnd + 4);
              // RFC-2822 unfold + find Subject:.
              const unfolded = headers.replace(/\r\n[\t ]+/g, " ");
              let cte = "";
              for (const h of unfolded.split("\r\n")) {
                const ms = /^Subject:\s*(.*)$/i.exec(h);
                if (ms && ms[1] !== undefined) subject = ms[1];
                const mc = /^Content-Transfer-Encoding:\s*(.*)$/i.exec(h);
                if (mc && mc[1] !== undefined) cte = mc[1].toLowerCase();
              }
              // Decode quoted-printable so assertions can match
              // human-readable substrings that the SMTP layer may
              // have soft-wrapped (e.g. "do NOT restore hits.txt"
              // landing across an `=\r\n` soft break).
              body = rawBody;
              if (cte === "quoted-printable") {
                body = body
                  .replace(/=\r\n/g, "")
                  .replace(/=\n/g, "")
                  .replace(/=([0-9A-Fa-f]{2})/g, (_, hex) =>
                    String.fromCharCode(parseInt(hex, 16)),
                  );
              }
            }
            messages.push({ raw, subject, body });
            inData = false;
            dataLines = [];
            write("250 queued");
          } else {
            dataLines.push(line.startsWith("..") ? line.slice(1) : line);
          }
          continue;
        }
        const upper = line.toUpperCase();
        if (upper.startsWith("EHLO") || upper.startsWith("HELO")) {
          write("250 hello");
        } else if (upper.startsWith("MAIL FROM:")) {
          write("250 ok");
        } else if (upper.startsWith("RCPT TO:")) {
          write("250 ok");
        } else if (upper.startsWith("DATA")) {
          write("354 send data");
          inData = true;
          dataLines = [];
        } else if (upper.startsWith("QUIT")) {
          write("221 bye");
          sock.end();
        } else if (upper.startsWith("RSET") || upper.startsWith("NOOP")) {
          write("250 ok");
        } else {
          write("250 ok");
        }
      }
    });
    sock.on("error", () => {
      /* ignore */
    });
  });
  await new Promise<void>((resolve) =>
    server.listen(0, "127.0.0.1", resolve),
  );
  const port = (server.address() as AddressInfo).port;
  return {
    port,
    messages,
    close: () =>
      new Promise<void>((resolve, reject) =>
        server.close((err) => (err ? reject(err) : resolve())),
      ),
  };
}

// Sink that mirrors `createKernelAlertSink` but (a) redirects
// `kernel.ALERTS_LOG` to a per-test tmp file and (b) passes the
// webhook + SMTP env vars into the spawn so the real `_post_webhook` /
// `_send_email` transports run against our capture servers. The python
// program does `_await_alert_dispatch` so the daemon dispatch thread is
// drained before exit.
export function makeWireSink(
  alertsLogPath: string,
  env: Record<string, string>,
): LedgerAlertSink {
  const program = [
    "import json, sys, pathlib",
    `sys.path.insert(0, ${JSON.stringify(REPO_ROOT)})`,
    "import kernel",
    `kernel.ALERTS_LOG = pathlib.Path(${JSON.stringify(alertsLogPath)})`,
    "data = json.load(sys.stdin)",
    "kernel._fire_ledger_alert(data['message'], data['context'])",
    "assert kernel._await_alert_dispatch(15.0), 'alert dispatch did not drain'",
  ].join("\n");
  return (invocation: LedgerAlertInvocation) =>
    new Promise<void>((resolve, reject) => {
      const child = spawn("python3", ["-c", program], {
        stdio: ["pipe", "ignore", "pipe"],
        env: { ...process.env, ...env },
      });
      let stderr = "";
      child.stderr.on("data", (b: Buffer) => {
        stderr += b.toString("utf-8");
      });
      child.on("error", (err) => reject(err));
      child.on("exit", (code) => {
        if (code !== 0) {
          reject(
            new Error(
              `wire sink subprocess exited ${code}; stderr=${stderr}`,
            ),
          );
          return;
        }
        resolve();
      });
      child.stdin.end(
        JSON.stringify({
          message: invocation.message,
          context: invocation.context,
        }),
      );
    });
}
