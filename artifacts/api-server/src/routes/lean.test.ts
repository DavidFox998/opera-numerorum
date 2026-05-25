import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { __testing } from "./lean.js";

const { checkRebuildAuth, sanitizeRefereeName, getNamedTokens, resetAuthState } =
  __testing;

interface MockReqInit {
  ip?: string;
  authorization?: string;
  refereeName?: string | string[];
}

function makeReq(init: MockReqInit = {}): any {
  return {
    ip: init.ip ?? "10.0.0.1",
    socket: { remoteAddress: init.ip ?? "10.0.0.1" },
    headers: {
      ...(init.authorization !== undefined
        ? { authorization: init.authorization }
        : {}),
      ...(init.refereeName !== undefined
        ? { "x-referee-name": init.refereeName }
        : {}),
    },
    log: {
      warn: vi.fn(),
      info: vi.fn(),
      error: vi.fn(),
    },
  };
}

const ORIGINAL_ENV = { ...process.env };

beforeEach(() => {
  delete process.env["LEAN_REBUILD_TOKEN"];
  delete process.env["LEAN_REBUILD_TOKENS"];
  resetAuthState();
});

afterEach(() => {
  process.env = { ...ORIGINAL_ENV };
  resetAuthState();
});

describe("sanitizeRefereeName", () => {
  it("accepts allowed characters within length limit", () => {
    expect(sanitizeRefereeName("Alice")).toBe("Alice");
    expect(sanitizeRefereeName("alice_2.0-beta")).toBe("alice_2.0-beta");
    expect(sanitizeRefereeName("  spaced  ")).toBe("spaced");
  });

  it("rejects non-string input", () => {
    expect(sanitizeRefereeName(undefined)).toBeNull();
    expect(sanitizeRefereeName(null)).toBeNull();
    expect(sanitizeRefereeName(42)).toBeNull();
    expect(sanitizeRefereeName(["alice"])).toBeNull();
  });

  it("rejects empty / whitespace-only names", () => {
    expect(sanitizeRefereeName("")).toBeNull();
    expect(sanitizeRefereeName("   ")).toBeNull();
  });

  it("rejects names with disallowed characters", () => {
    expect(sanitizeRefereeName("alice@example.com")).toBeNull();
    expect(sanitizeRefereeName("alice/bob")).toBeNull();
    expect(sanitizeRefereeName("<script>")).toBeNull();
    expect(sanitizeRefereeName("alice\nbob")).toBeNull();
  });

  it("rejects names longer than 64 characters", () => {
    expect(sanitizeRefereeName("a".repeat(64))).toBe("a".repeat(64));
    expect(sanitizeRefereeName("a".repeat(65))).toBeNull();
  });
});

describe("getNamedTokens", () => {
  it("returns [] when env is unset or empty", () => {
    expect(getNamedTokens()).toEqual([]);
    process.env["LEAN_REBUILD_TOKENS"] = "";
    expect(getNamedTokens()).toEqual([]);
    process.env["LEAN_REBUILD_TOKENS"] = "   ";
    expect(getNamedTokens()).toEqual([]);
  });

  it("parses well-formed name:token pairs", () => {
    process.env["LEAN_REBUILD_TOKENS"] = "alice:tokA,bob:tokB";
    expect(getNamedTokens()).toEqual([
      { name: "alice", token: "tokA" },
      { name: "bob", token: "tokB" },
    ]);
  });

  it("drops malformed entries silently and keeps the well-formed ones", () => {
    process.env["LEAN_REBUILD_TOKENS"] = [
      "alice:tokA",
      "bareword",
      "nokey:",
      ":nokey",
      "bad@name:tok",
      "  ",
      ("x".repeat(65) + ":tok"),
      "bob:tokB",
    ].join(",");
    expect(getNamedTokens()).toEqual([
      { name: "alice", token: "tokA" },
      { name: "bob", token: "tokB" },
    ]);
  });

  it("allows tokens that themselves contain colons", () => {
    process.env["LEAN_REBUILD_TOKENS"] = "alice:tok:with:colons";
    expect(getNamedTokens()).toEqual([
      { name: "alice", token: "tok:with:colons" },
    ]);
  });
});

describe("checkRebuildAuth", () => {
  describe("when no tokens are configured", () => {
    it("returns 503", () => {
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer anything" }),
      );
      expect(result.ok).toBe(false);
      if (!result.ok) expect(result.status).toBe(503);
    });
  });

  describe("with only LEAN_REBUILD_TOKEN (shared) set", () => {
    beforeEach(() => {
      process.env["LEAN_REBUILD_TOKEN"] = "shared-secret";
    });

    it("rejects requests without an Authorization header (401)", () => {
      const result = checkRebuildAuth(makeReq({}));
      expect(result.ok).toBe(false);
      if (!result.ok) expect(result.status).toBe(401);
    });

    it("rejects requests with a wrong token (401)", () => {
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer nope" }),
      );
      expect(result.ok).toBe(false);
      if (!result.ok) expect(result.status).toBe(401);
    });

    it("accepts the shared token with no X-Referee-Name (anonymous)", () => {
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer shared-secret" }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBeNull();
    });

    it("accepts the shared token and records a valid X-Referee-Name", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: "Alice",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("Alice");
    });

    it("drops a too-long X-Referee-Name and records as anonymous (not rejected)", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: "a".repeat(65),
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBeNull();
    });

    it("drops a bad-character X-Referee-Name and records as anonymous", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: "alice@evil.com",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBeNull();
    });

    it("handles X-Referee-Name sent as an array (first value)", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: ["Alice", "Mallory"],
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("Alice");
    });
  });

  describe("with LEAN_REBUILD_TOKENS (named) set", () => {
    beforeEach(() => {
      process.env["LEAN_REBUILD_TOKENS"] = "alice:tokA,bob:tokB";
    });

    it("attributes a named-token rebuild to the token's name (no header)", () => {
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer tokA" }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("alice");
    });

    it("ignores X-Referee-Name when a named token matches (anti-spoof invariant)", () => {
      // Alice authenticates with her named token but tries to impersonate Bob
      // via the X-Referee-Name header. The header must be ignored.
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer tokA",
          refereeName: "bob",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("alice");
    });

    it("ignores X-Referee-Name even when it is a well-formed unrelated string", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer tokB",
          refereeName: "President Of The Universe",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("bob");
    });

    it("rejects an unknown token even when other named tokens are configured (401)", () => {
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer tokC" }),
      );
      expect(result.ok).toBe(false);
      if (!result.ok) expect(result.status).toBe(401);
    });

    it("rejects when LEAN_REBUILD_TOKENS contains only malformed entries (503)", () => {
      process.env["LEAN_REBUILD_TOKENS"] = "bareword,nokey:,:nokey,bad@name:tok";
      resetAuthState();
      const result = checkRebuildAuth(
        makeReq({ authorization: "Bearer anything" }),
      );
      expect(result.ok).toBe(false);
      if (!result.ok) expect(result.status).toBe(503);
    });
  });

  describe("with both shared and named tokens set", () => {
    beforeEach(() => {
      process.env["LEAN_REBUILD_TOKEN"] = "shared-secret";
      process.env["LEAN_REBUILD_TOKENS"] = "alice:tokA";
    });

    it("prefers the named-token match and ignores X-Referee-Name", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer tokA",
          refereeName: "mallory",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("alice");
    });

    it("falls back to the shared token and honours a valid X-Referee-Name", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: "Carol",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBe("Carol");
    });

    it("falls back to the shared token and records anonymous on a bad name", () => {
      const result = checkRebuildAuth(
        makeReq({
          authorization: "Bearer shared-secret",
          refereeName: "bad/name",
        }),
      );
      expect(result.ok).toBe(true);
      if (result.ok) expect(result.refereeName).toBeNull();
    });
  });

  describe("brute-force lockout", () => {
    beforeEach(() => {
      process.env["LEAN_REBUILD_TOKEN"] = "shared-secret";
    });

    it("locks an IP out after 5 bad attempts (429 on the 6th)", () => {
      for (let i = 0; i < 5; i++) {
        const r = checkRebuildAuth(
          makeReq({ ip: "1.2.3.4", authorization: "Bearer wrong" }),
        );
        expect(r.ok).toBe(false);
        if (!r.ok) expect(r.status).toBe(401);
      }
      const blocked = checkRebuildAuth(
        makeReq({ ip: "1.2.3.4", authorization: "Bearer shared-secret" }),
      );
      expect(blocked.ok).toBe(false);
      if (!blocked.ok) {
        expect(blocked.status).toBe(429);
        expect(blocked.retryAfterSec).toBeGreaterThan(0);
      }
    });

    it("does not lock out a different IP", () => {
      for (let i = 0; i < 5; i++) {
        checkRebuildAuth(
          makeReq({ ip: "1.2.3.4", authorization: "Bearer wrong" }),
        );
      }
      const other = checkRebuildAuth(
        makeReq({ ip: "5.6.7.8", authorization: "Bearer shared-secret" }),
      );
      expect(other.ok).toBe(true);
    });
  });
});
