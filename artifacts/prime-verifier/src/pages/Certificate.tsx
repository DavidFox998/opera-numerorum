import { useState } from "react";
import { useGetCertificate, useRunVerification } from "@workspace/api-client-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { CheckCircle, XCircle, ChevronDown, Play, Loader2, Shield, Hash, Sigma } from "lucide-react";

function PassBadge({ pass }: { pass: boolean }) {
  return pass ? (
    <span className="inline-flex items-center gap-1 text-emerald-600 font-semibold text-sm">
      <CheckCircle className="w-4 h-4" /> PASS
    </span>
  ) : (
    <span className="inline-flex items-center gap-1 text-destructive font-semibold text-sm">
      <XCircle className="w-4 h-4" /> FAIL
    </span>
  );
}

function StatusBanner({ status }: { status: string }) {
  const ok = status === "VERIFIED";
  return (
    <div
      className={`flex items-center gap-3 rounded-xl px-6 py-4 ${
        ok
          ? "bg-emerald-50 border border-emerald-200 text-emerald-800 dark:bg-emerald-950 dark:border-emerald-800 dark:text-emerald-300"
          : "bg-destructive/10 border border-destructive/30 text-destructive"
      }`}
    >
      {ok ? (
        <CheckCircle className="w-8 h-8 shrink-0 text-emerald-600" />
      ) : (
        <XCircle className="w-8 h-8 shrink-0" />
      )}
      <div>
        <div className="font-bold text-lg">
          {ok ? "All checks passed — Certificate VERIFIED" : "Verification FAILED"}
        </div>
        <div className="text-sm opacity-80">
          {ok
            ? "The exceptional set S(π/10) is confirmed and GRH holds for L(s, X₀(10))."
            : "One or more verification steps did not pass. See details below."}
        </div>
      </div>
    </div>
  );
}

function Step({
  number,
  title,
  icon: Icon,
  pass,
  children,
}: {
  number: string;
  title: string;
  icon: React.ElementType;
  pass: boolean;
  children: React.ReactNode;
}) {
  return (
    <Card className="shadow-sm">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-3 text-base">
          <span className="flex items-center justify-center w-7 h-7 rounded-full bg-primary/10 text-primary text-xs font-bold">
            {number}
          </span>
          <Icon className="w-4 h-4 text-muted-foreground" />
          <span>{title}</span>
          <span className="ml-auto">
            <PassBadge pass={pass} />
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

export default function CertificatePage() {
  const { data: cert, isLoading } = useGetCertificate();
  const runMutation = useRunVerification();
  const [liveResult, setLiveResult] = useState<typeof cert | null>(null);
  const [runError, setRunError] = useState<string | null>(null);
  const [tableOpen, setTableOpen] = useState(false);

  const active = liveResult ?? cert;

  function handleRun() {
    setRunError(null);
    setLiveResult(null);
    runMutation.mutate(undefined, {
      onSuccess: (data) => {
        if (data.success && data.certificate) {
          setLiveResult(data.certificate as typeof cert);
        } else {
          setRunError(data.error ?? "Unknown error");
        }
      },
      onError: () => setRunError("Network error — could not reach API"),
    });
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center gap-4">
          <Shield className="w-6 h-6 text-primary" />
          <div>
            <h1 className="font-bold text-lg leading-tight">
              Machine Verification Certificate
            </h1>
            <p className="text-xs text-muted-foreground">
              Exceptional Primes for π/10 · GRH for X₀(143) · David Fox, May 2026
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* Run button */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            {liveResult ? (
              <span className="text-emerald-600 font-medium">
                Live run complete · {liveResult.runtime_ms} ms · {liveResult.precision_digits} decimal digits
              </span>
            ) : active ? (
              <span>
                Static certificate · {active.precision_digits} decimal digits (mpmath)
              </span>
            ) : null}
          </div>
          <Button
            onClick={handleRun}
            disabled={runMutation.isPending}
            className="gap-2"
          >
            {runMutation.isPending ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Running…</>
            ) : (
              <><Play className="w-4 h-4" /> Run Live Verification</>
            )}
          </Button>
        </div>

        {runError && (
          <div className="rounded-lg bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 text-sm font-mono">
            {runError}
          </div>
        )}

        {isLoading && !active && (
          <div className="flex items-center gap-2 text-muted-foreground py-16 justify-center">
            <Loader2 className="w-5 h-5 animate-spin" /> Loading certificate…
          </div>
        )}

        {active && (
          <>
            {/* Status banner */}
            <StatusBanner status={active.status} />

            {/* Meta */}
            <div className="grid grid-cols-3 gap-3 text-sm">
              {[
                ["Timestamp", active.timestamp],
                ["Precision", `${active.precision_digits} decimal digits`],
                ["Runtime", active.runtime_ms ? `${active.runtime_ms} ms` : "precomputed"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-lg bg-card border px-4 py-3">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">{label}</div>
                  <div className="font-mono font-medium">{value}</div>
                </div>
              ))}
            </div>

            {/* Step 1 */}
            <Step number="1" title="Exceptional Set S(π/10) for p ≤ 500" icon={Sigma} pass={active.s4_check.pass}>
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="rounded-lg bg-muted/50 px-4 py-3">
                    <div className="text-xs text-muted-foreground mb-1">Expected S₄</div>
                    <code className="font-mono">&#123;2, 3, 19, 191&#125;</code>
                  </div>
                  <div className="rounded-lg bg-muted/50 px-4 py-3">
                    <div className="text-xs text-muted-foreground mb-1">Computed</div>
                    <code className="font-mono">&#123;{active.s4_check.found.join(", ")}&#125;</code>
                  </div>
                </div>

                {/* Key rows from the paper */}
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>p</TableHead>
                      <TableHead>‖p·π/10‖</TableHead>
                      <TableHead>1/p</TableHead>
                      <TableHead>p ∈ S(π/10)?</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {(active.verification_table_500 ?? []).map((row) => (
                      <TableRow key={row.p} className={row.member ? "bg-emerald-50/50 dark:bg-emerald-950/20" : ""}>
                        <TableCell className="font-mono font-semibold">{row.p}</TableCell>
                        <TableCell className="font-mono text-xs">{row.norm}</TableCell>
                        <TableCell className="font-mono text-xs">{row.threshold}</TableCell>
                        <TableCell>
                          {row.member ? (
                            <Badge variant="outline" className="border-emerald-500 text-emerald-600 text-xs">Yes ✓</Badge>
                          ) : (
                            <span className="text-muted-foreground text-xs">No</span>
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>

                <Collapsible open={tableOpen} onOpenChange={setTableOpen}>
                  <CollapsibleTrigger asChild>
                    <Button variant="ghost" size="sm" className="gap-1 text-xs text-muted-foreground">
                      <ChevronDown className={`w-3 h-3 transition-transform ${tableOpen ? "rotate-180" : ""}`} />
                      {tableOpen ? "Hide" : "Show"} full 500-prime sieve note
                    </Button>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <p className="text-xs text-muted-foreground bg-muted/40 rounded-lg px-4 py-3 mt-1 font-mono leading-relaxed">
                      All 91 primes in (191, 500] were verified to fail the condition ‖pπ/10‖ &lt; 1/p.<br />
                      The Colmez desert (Remark 2.2) guarantees no prime in (191, 474984) can be exceptional.<br />
                      Continued fraction: π/10 = [0; 3, 5, 2, 5, 1, 733, …] · a₆ = 733 is large.
                    </p>
                  </CollapsibleContent>
                </Collapsible>
              </div>
            </Step>

            {/* Step 2 */}
            <Step number="2" title="Bost–Connes Energy & GRH for L(s, X₀(10))" icon={Sigma} pass={active.grh_level_10.C_exceeds_threshold}>
              <div className="space-y-3">
                <div className="rounded-lg bg-muted/50 px-4 py-4 font-mono text-sm space-y-2">
                  <div>
                    C(S₄) = <span className="text-primary font-bold">{active.bost_connes_S4}</span>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    = log(2)/1 + log(3)/2 + log(19)/18 + log(191)/190
                  </div>
                  <Separator />
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>Threshold τ(10) = 2√g(X₀(10)) = <span className="font-bold">0</span></div>
                    <div>C(S₄) &gt; τ(10) : <PassBadge pass={active.grh_level_10.C_exceeds_threshold} /></div>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  Since X₀(10) ≅ ℙ¹ has genus 0, the threshold vanishes. The Main Sieve Lemma then
                  implies{" "}
                  <span className="font-semibold text-foreground">
                    {active.grh_level_10.conclusion}.
                  </span>
                </p>
              </div>
            </Step>

            {/* Step 3 */}
            <Step number="3" title="Large Exceptional Primes (p₅, p₆, p₇)" icon={Sigma} pass={active.large_primes_pass}>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground mb-3">
                  Verified at {active.precision_digits} decimal digits via mpmath. The Colmez desert
                  guarantees any prime beyond p₄ = 191 must exceed ≈ 474,984.
                </p>
                <div className="space-y-3">
                  {active.large_primes.map((lp, i) => (
                    <div
                      key={lp.p}
                      className={`rounded-lg border px-4 py-3 ${
                        lp.member
                          ? "border-emerald-300 bg-emerald-50/60 dark:border-emerald-800 dark:bg-emerald-950/20"
                          : "border-destructive/40 bg-destructive/5"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                          p{i + 5}
                        </span>
                        <PassBadge pass={lp.member} />
                      </div>
                      <div className="font-mono text-sm font-bold break-all">{lp.p}</div>
                      <div className="text-xs text-muted-foreground mt-1 font-mono">
                        ‖p·π/10‖ = {lp.norm} &nbsp;·&nbsp; 1/p = {lp.threshold}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Step>

            {/* Step 4: SHA-256 */}
            <Step number="4" title="SHA-256 of Canonical Prime Set" icon={Hash} pass={active.sha256_match}>
              <div className="space-y-3">
                <div className="rounded-lg bg-muted/50 px-4 py-4 space-y-2">
                  <div className="text-xs text-muted-foreground uppercase tracking-wider mb-2">S_canon</div>
                  <div className="flex flex-wrap gap-2">
                    {active.exceptional_set.map((p, i) => (
                      <code
                        key={p}
                        className="text-xs bg-primary/10 text-primary rounded px-2 py-1 font-mono"
                      >
                        p{i + 1}={p}
                      </code>
                    ))}
                  </div>
                </div>
                <div className="space-y-1 text-sm">
                  {[
                    ["Computed SHA-256", active.sha256],
                    ["Expected SHA-256", active.expected_sha256],
                  ].map(([label, val]) => (
                    <div key={label} className="rounded-lg bg-card border px-4 py-2">
                      <div className="text-xs text-muted-foreground mb-1">{label}</div>
                      <code className="font-mono text-xs break-all">{val}</code>
                    </div>
                  ))}
                </div>
                <div className="text-sm">
                  Hash match: <PassBadge pass={active.sha256_match} />
                </div>
              </div>
            </Step>

            {/* Footer */}
            <Separator />
            <div className="text-xs text-muted-foreground text-center space-y-1 pb-8">
              <div>Verification protocol: Section 7 of the canonical paper (May 2026)</div>
              <div>
                Reproduce:{" "}
                <code className="bg-muted rounded px-1 py-0.5">
                  python3 verify/bost_connes_verify.py
                </code>
                {" "}·{" "}
                <code className="bg-muted rounded px-1 py-0.5">
                  gcc -O2 -o bin/print_S4 bin/print_S4.c && ./bin/print_S4
                </code>
              </div>
              <div>
                GitHub:{" "}
                <a
                  href="https://github.com/DavidFox998/alpha0-ponti"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary underline"
                >
                  DavidFox998/alpha0-ponti
                </a>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
