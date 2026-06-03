import { Link } from "wouter";
import { ArrowLeft, AlertTriangle, ShieldCheck, FileCode } from "lucide-react";
import { Card } from "@/components/ui/card";
import colophonRaw from "@docs/COLOPHON.md?raw";
import h4coreRaw from "@lean/Towers/YM/H4Core.data.json?raw";
import h4boundaryRaw from "@lean/Towers/YM/H4_Boundary.data.json?raw";
import h4timeboundRaw from "@lean/Towers/YM/H4_TimeBound.data.json?raw";
import h4derivationRaw from "@lean/Towers/YM/H4_Derivation.data.json?raw";


const mono = "font-mono text-sm bg-muted px-1.5 py-0.5 border border-border";

interface BuildRow {
  module: string;
  file: string;
  leaf?: string;
  sha: string;
  status: string;
  tone: "locked" | "empirical" | "conjecture";
}

const BUILD_TABLE: BuildRow[] = [
  {
    module: "A",
    file: "H4Core.lean",
    leaf: "H4_Strata_Ztau.lean",
    sha: "aa8c118048652b2aec592ee287479ca01098ec233738fb9b20fdb06b22b1a6ce",
    status: "LOCKED · PROVEN",
    tone: "locked",
  },
  {
    module: "A.1",
    file: "H4_Boundary.lean",
    sha: "05bf60221f712abb97fa5396a5e0eea0a23159218b3fcc07fa06b76b320c871a",
    status: "EMPIRICAL 9/9",
    tone: "empirical",
  },
  {
    module: "E",
    file: "H4_TimeBound.lean",
    sha: "5f172143eceb87d0f00de3bf33f6432e62d83ca4b4b1220b9b022601ae74f8a7",
    status: "EMPIRICAL 6/6",
    tone: "empirical",
  },
  {
    module: "D",
    file: "H4_Derivation.lean",
    sha: "e21ae1ba9990fdb560fd851c56964b4439aefeeab217f5c5fc48ddd50a2ee2b2",
    status: "CONJECTURE",
    tone: "conjecture",
  },
];

const toneClass: Record<BuildRow["tone"], string> = {
  locked:
    "border-green-500/50 bg-green-500/10 text-green-700 dark:text-green-400",
  empirical:
    "border-sky-500/50 bg-sky-500/10 text-sky-700 dark:text-sky-400",
  conjecture:
    "border-amber-500/50 bg-amber-500/10 text-amber-700 dark:text-amber-400",
};

interface DataModule {
  key: string;
  title: string;
  file: string;
  raw: string;
}

const DATA_MODULES: DataModule[] = [
  { key: "A", title: "Module A — H4Core", file: "H4Core.data.json", raw: h4coreRaw },
  {
    key: "A.1",
    title: "Module A.1 — H4 Boundary",
    file: "H4_Boundary.data.json",
    raw: h4boundaryRaw,
  },
  {
    key: "E",
    title: "Module E — H4 TimeBound",
    file: "H4_TimeBound.data.json",
    raw: h4timeboundRaw,
  },
  {
    key: "D",
    title: "Module D — H4 Derivation",
    file: "H4_Derivation.data.json",
    raw: h4derivationRaw,
  },
];

function Section({
  index,
  title,
  subtitle,
  children,
}: {
  index: string;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <Card className="p-6 border-border bg-card">
      <div className="flex items-baseline gap-3 mb-1 border-b border-border pb-3">
        <div className="font-mono text-xs text-primary uppercase tracking-[0.18em]">
          {index}
        </div>
        <h3 className="font-sans font-bold text-lg tracking-tight">{title}</h3>
      </div>
      {subtitle && (
        <p className="font-mono text-[11px] text-muted-foreground uppercase tracking-wider mt-2 mb-4">
          {subtitle}
        </p>
      )}
      <div className="space-y-4">{children}</div>
    </Card>
  );
}

export default function V23Page() {
  return (
    <div className="space-y-8">
      <Link
        href="/"
        className="inline-flex items-center text-xs font-mono text-muted-foreground hover:text-foreground transition-colors"
        data-testid="link-back-dashboard"
      >
        <ArrowLeft className="w-3 h-3 mr-2" /> BACK TO DASHBOARD
      </Link>

      <header className="border-b border-border pb-6">
        <div className="font-mono text-[10px] text-muted-foreground uppercase tracking-[0.18em] mb-2">
          Towers YM v2.3 · /v2.3/ · 2026-06-02
        </div>
        <h2 className="text-3xl font-bold font-sans tracking-tight mb-2">
          H₄ Boundary Protocol — v2.3
        </h2>
        <p className="text-sm font-mono text-muted-foreground">
          FORMAL + EMPIRICAL · AXIOMS 0 · SORRY 0 · MATHLIB OFF · D. FOX · ORCID
          0009-0008-1290-6105
        </p>
      </header>

      {/* Honesty box up front — scope lock */}
      <Card className="p-6 border-amber-500/60 bg-amber-500/5">
        <div className="flex items-center gap-2 font-mono text-[11px] text-amber-700 dark:text-amber-400 uppercase tracking-[0.18em] mb-3 border-b border-amber-500/30 pb-2">
          <AlertTriangle className="w-4 h-4" />
          Read honestly — what v2.3 is and is not
        </div>
        <div className="space-y-3 font-serif text-base leading-relaxed text-foreground/90">
          <p>
            v2.3 is a <strong>mathlib-free, sorry-free, axiom-free</strong> finite
            computation over the real W(H₄) point-stabilizer geometry. Every{" "}
            <span className={mono}>Sym</span> value is computed by the engine in{" "}
            <span className={mono}>H4Core.lean</span>, never hardcoded.
          </p>
          <p>
            The boundary law{" "}
            <span className={mono}>digit_len p ≥ 13 → Sym p = 1</span> is a{" "}
            <strong>CONJECTURE</strong> — recorded as the named open{" "}
            <span className={mono}>Prop</span> <span className={mono}>C13_Law_Open</span>,
            supported by <strong>6/6 empirical samples only</strong>. No theorem
            discharges it; no ∀-law is proven.
          </p>
          <p>
            The proposed <span className={mono}>P5 = 10000000001119</span> has{" "}
            <span className={mono}>digit_len 14</span>, NOT 13 — so its{" "}
            <span className={mono}>digit_len P5 = 13</span> claim is{" "}
            <strong>FALSE</strong>. The genuine 13-digit boundary prime is{" "}
            <span className={mono}>1000000001119</span>. <span className={mono}>3^40</span>{" "}
            carries no temporal meaning; <span className={mono}>10^12 ≪ 3^40</span>{" "}
            by ~7 orders of magnitude.
          </p>
          <p>
            This proves <strong>no</strong> Yang–Mills / mass-gap / Surface-#1
            result, and is keyed to no L-function. It is pure finite geometry,
            surfaced honestly.
          </p>
        </div>
      </Card>

      {/* Page 3: Build Table */}
      <Section
        index="§ 1"
        title="Build Table"
        subtitle="Module · File · SHA-256 (file) · Status"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-border text-left font-mono text-[11px] uppercase tracking-wider text-muted-foreground">
                <th className="py-2 pr-4">Module</th>
                <th className="py-2 pr-4">File</th>
                <th className="py-2 pr-4">SHA-256 (file)</th>
                <th className="py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {BUILD_TABLE.map((row) => (
                <tr
                  key={row.module}
                  className="border-b border-border/60 align-top"
                  data-testid={`build-row-${row.module}`}
                >
                  <td className="py-3 pr-4 font-mono font-bold">{row.module}</td>
                  <td className="py-3 pr-4 font-mono text-xs">
                    {row.file}
                    {row.leaf && (
                      <span className="block text-muted-foreground">
                        + {row.leaf}
                      </span>
                    )}
                  </td>
                  <td className="py-3 pr-4 font-mono text-[10px] break-all max-w-[18rem] text-muted-foreground">
                    {row.sha}
                  </td>
                  <td className="py-3">
                    <span
                      className={`inline-block px-2 py-0.5 border font-mono text-[10px] font-bold uppercase ${toneClass[row.tone]}`}
                    >
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="font-serif text-sm leading-relaxed text-foreground/80 pt-2">
          SHAs above are the <strong>actual file</strong> SHA-256 of each{" "}
          <span className={mono}>.lean</span> source. The BUILD_MANIFEST v2.3
          lists <span className={mono}>A = 48536d9d…ba997</span>, but that is the
          prose milestone <strong>record</strong> hash, NOT a file hash — the real{" "}
          <span className={mono}>H4Core.lean</span> file hash is{" "}
          <span className={mono}>aa8c1180…a6ce</span> (recorded in{" "}
          <span className={mono}>H4Core.data.json</span>). Only Module D's hash is
          pinned explicitly in the manifest, and it matches.
        </p>
      </Section>

      {/* Page 4+: Data */}
      <Section
        index="§ 2"
        title="Data"
        subtitle="data.json from each module · #eval outputs · no prose beyond Lean"
      >
        <div className="space-y-5">
          {DATA_MODULES.map((m) => (
            <div
              key={m.key}
              className="border border-border bg-muted/20"
              data-testid={`data-module-${m.key}`}
            >
              <div className="flex items-center gap-2 px-4 py-2 border-b border-border bg-muted/40">
                <FileCode className="w-3.5 h-3.5 text-muted-foreground" />
                <span className="font-mono text-xs font-bold">{m.title}</span>
                <span className="font-mono text-[10px] text-muted-foreground">
                  · {m.file}
                </span>
              </div>
              <pre className="p-4 overflow-x-auto font-mono text-[11px] leading-relaxed text-foreground/85 whitespace-pre">
                {m.raw}
              </pre>
            </div>
          ))}
        </div>
      </Section>

      {/* Final Page: Colophon */}
      <Section index="§ 3" title="Colophon" subtitle="docs/COLOPHON.md — verbatim">
        <div className="border border-border bg-muted/20">
          <div className="flex items-center gap-2 px-4 py-2 border-b border-border bg-muted/40">
            <ShieldCheck className="w-3.5 h-3.5 text-muted-foreground" />
            <span className="font-mono text-xs font-bold">COLOPHON.md</span>
          </div>
          <pre className="p-4 overflow-x-auto font-mono text-[12px] leading-relaxed text-foreground/90 whitespace-pre-wrap">
            {colophonRaw}
          </pre>
        </div>
      </Section>

      <div className="text-[10px] font-mono text-muted-foreground text-center pt-2">
        © 2026 D. Fox · Entangled Technologies · all computations reproducible
        from SHA-locked Lean · axioms 0 · sorry 0
      </div>
    </div>
  );
}
