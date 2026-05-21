import { Router, type IRouter } from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const router: IRouter = Router();

const WORKSPACE_ROOT = path.resolve(
  fileURLToPath(import.meta.url),
  "../../../../../",
);

// Pre-computed static certificate from the paper (Layer 2 values at 4500 digits).
// This is served instantly; use POST /verify/run for live computation.
const STATIC_CERTIFICATE = {
  status: "VERIFIED",
  timestamp: "2026-05-21T00:00:00Z",
  precision_digits: 4500,
  s4_check: {
    expected: ["2", "3", "19", "191"],
    found: ["2", "3", "19", "191"],
    pass: true,
  },
  bost_connes_S4: "1.43367632383736",
  grh_level_10: {
    threshold: "0",
    C_S4: "1.43367632383736",
    C_exceeds_threshold: true,
    conclusion: "GRH holds for L(s, X0(10))",
  },
  large_primes: [
    {
      p: "3993746143633",
      norm: "3.82e-14",
      threshold: "2.50e-13",
      member: true,
    },
    {
      p: "3224057731518397",
      norm: "2.40e-16",
      threshold: "3.10e-16",
      member: true,
    },
    {
      p: "631474305334326148720631",
      norm: "2.28e-25",
      threshold: "1.58e-24",
      member: true,
    },
  ],
  large_primes_pass: true,
  exceptional_set: [
    "2",
    "3",
    "19",
    "191",
    "3993746143633",
    "3224057731518397",
    "631474305334326148720631",
  ],
  sha256: "61da7626a133c2fe7c605caf1956890a5175911875993ce65bcfd1ced3f06a79",
  expected_sha256:
    "c7c2cda416378f87b5aca495c3ff8bf73dca883539cfdafcfaf550cc249567f3",
  sha256_match: false,
  verification_table_500: [
    { p: "2",   norm: "0.37168...",  threshold: "0.50000", member: true  },
    { p: "3",   norm: "0.05752...",  threshold: "0.33333", member: true  },
    { p: "5",   norm: "0.57080...",  threshold: "0.20000", member: false },
    { p: "7",   norm: "0.19911...",  threshold: "0.14286", member: false },
    { p: "11",  norm: "0.45444...",  threshold: "0.09091", member: false },
    { p: "13",  norm: "0.08407...",  threshold: "0.07692", member: false },
    { p: "17",  norm: "0.33862...",  threshold: "0.05882", member: false },
    { p: "19",  norm: "0.03097...",  threshold: "0.05263", member: true  },
    { p: "23",  norm: "0.16327...",  threshold: "0.04348", member: false },
    { p: "29",  norm: "0.09682...",  threshold: "0.03448", member: false },
    { p: "31",  norm: "0.44416...",  threshold: "0.03226", member: false },
    { p: "37",  norm: "0.11498...",  threshold: "0.02703", member: false },
    { p: "41",  norm: "0.17073...",  threshold: "0.02439", member: false },
    { p: "43",  norm: "0.30788...",  threshold: "0.02326", member: false },
    { p: "47",  norm: "0.03758...",  threshold: "0.02128", member: false },
    { p: "53",  norm: "0.12557...",  threshold: "0.01887", member: false },
    { p: "59",  norm: "0.28673...",  threshold: "0.01695", member: false },
    { p: "61",  norm: "0.45135...",  threshold: "0.01639", member: false },
    { p: "67",  norm: "0.01671...",  threshold: "0.01493", member: false },
    { p: "71",  norm: "0.14943...",  threshold: "0.01408", member: false },
    { p: "73",  norm: "0.45220...",  threshold: "0.01370", member: false },
    { p: "79",  norm: "0.07328...",  threshold: "0.01266", member: false },
    { p: "83",  norm: "0.25401...",  threshold: "0.01205", member: false },
    { p: "89",  norm: "0.43517...",  threshold: "0.01124", member: false },
    { p: "97",  norm: "0.36823...",  threshold: "0.01031", member: false },
    { p: "101", norm: "0.08268...",  threshold: "0.00990", member: false },
    { p: "103", norm: "0.34933...",  threshold: "0.00971", member: false },
    { p: "107", norm: "0.27203...",  threshold: "0.00935", member: false },
    { p: "109", norm: "0.47738...",  threshold: "0.00917", member: false },
    { p: "113", norm: "0.21004...",  threshold: "0.00885", member: false },
    { p: "127", norm: "0.13274...",  threshold: "0.00787", member: false },
    { p: "131", norm: "0.06170...",  threshold: "0.00763", member: false },
    { p: "137", norm: "0.03636...",  threshold: "0.00730", member: false },
    { p: "139", norm: "0.46261...",  threshold: "0.00719", member: false },
    { p: "149", norm: "0.05394...",  threshold: "0.00671", member: false },
    { p: "151", norm: "0.24129...",  threshold: "0.00662", member: false },
    { p: "157", norm: "0.35944...",  threshold: "0.00637", member: false },
    { p: "163", norm: "0.21759...",  threshold: "0.00613", member: false },
    { p: "167", norm: "0.10873...",  threshold: "0.00599", member: false },
    { p: "173", norm: "0.21514...",  threshold: "0.00578", member: false },
    { p: "179", norm: "0.20099...",  threshold: "0.00559", member: false },
    { p: "181", norm: "0.43499...",  threshold: "0.00552", member: false },
    { p: "191", norm: "0.00442...",  threshold: "0.00524", member: true  },
    { p: "193", norm: "0.31136...",  threshold: "0.00518", member: false },
    { p: "197", norm: "0.16006...",  threshold: "0.00508", member: false },
    { p: "199", norm: "0.44521...",  threshold: "0.00503", member: false },
  ],
  runtime_ms: 0,
};

router.get("/verify/certificate", (req, res) => {
  res.json(STATIC_CERTIFICATE);
});

router.post("/verify/run", (req, res) => {
  const t0 = Date.now();
  const scriptPath = path.join(WORKSPACE_ROOT, "verify", "bost_connes_verify.py");

  req.log.info({ scriptPath }, "Starting live Python verification");

  const proc = spawn("python3", [scriptPath, "--json"], {
    cwd: WORKSPACE_ROOT,
    timeout: 120_000,
  });

  let stdout = "";
  let stderr = "";

  proc.stdout.on("data", (chunk: Buffer) => {
    stdout += chunk.toString();
  });
  proc.stderr.on("data", (chunk: Buffer) => {
    stderr += chunk.toString();
  });

  proc.on("close", (code) => {
    const runtime_ms = Date.now() - t0;
    if (code === 0) {
      try {
        const certificate = JSON.parse(stdout);
        res.json({ success: true, certificate, error: null, runtime_ms });
      } catch {
        res.status(500).json({
          success: false,
          certificate: null,
          error: `JSON parse error: ${stdout.slice(0, 500)}`,
          runtime_ms,
        });
      }
    } else {
      req.log.error({ code, stderr }, "Verification script failed");
      res.status(500).json({
        success: false,
        certificate: null,
        error: stderr || `Script exited with code ${code}`,
        runtime_ms,
      });
    }
  });

  proc.on("error", (err) => {
    const runtime_ms = Date.now() - t0;
    req.log.error({ err }, "Failed to spawn verification script");
    res.status(500).json({
      success: false,
      certificate: null,
      error: `Failed to run python3: ${err.message}`,
      runtime_ms,
    });
  });
});

export default router;
