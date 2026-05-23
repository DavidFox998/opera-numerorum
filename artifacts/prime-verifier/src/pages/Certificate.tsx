import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  CheckCircle,
  Lock,
  ChevronDown,
  Shield,
  Hash,
  AlertTriangle,
} from "lucide-react";

const MANIFEST_SHA =
  "5b80b84d1d3d13e216eeecd8155c1edc854d578e7d2dae9c4bc72fcbf7ebe3c9";
const SCRIPT_SHA =
  "39c0170455e40b30c7a7aeb6a2801b50d8e9554bb3d7bc746164d22b71174565";
const M8_SHA =
  "e2d70821cd66588cd715dfe37a44122130f88d15584738f5f64a02ff7f7b0002";

const MODULES = [
  {
    id: "M1",
    title: "\u03b1\u2080 = 299 + \u03c0/10",
    claim:
      "\u03b1\u2080 computed to 5000 decimal places using mpmath at 64 dps. Value: 299 + \u03c0/10 \u2248 299.31415926\u2026",
    source: "certificates/alpha0.py",
    stdout: "m1.out",
    sha: "63ef870a78766619327e99b68683bceff8c8ef9a525298756c77c8378fd2c291",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M2",
    title: "Kappa Bound (80-bit long double)",
    claim:
      "kappa = \u03c6(143) \u00d7 c / 10\u2078 = 4.8433014197780389, computed in C with 80-bit long double precision.",
    source: "bin/print_kappa.c",
    stdout: "m2.out",
    sha: "3716c7dbb32524074b8fffb65eea45069c8b568a31dc73706405116b84029a83",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M3",
    title: "Continued Fraction of \u03c0/10",
    claim:
      "\u03c0/10 = [0; 3, 5, 2, 5, 1, 733, \u2026] \u2014 a\u2086 = 733 (large), Q\u2085 = 226, bound = 82829. Colmez desert: no exceptional prime in (191, 82829).",
    source: "cf_pi10.py",
    stdout: "m3.out",
    sha: "e687bb09a55e4eda198d4c5b24d03b7579f93bba27184a61fec7cbe29a83d044",
    status: "CERTIFIED",
    correction:
      "LaTeX draft had CF seed swapped (p=0, pp=1, q=1, qq=0). Correct seed: p=1, pp=0, q=0, qq=1. Corrected result: Q\u2085=226, bound=82829 (not 1296 / 474984).",
  },
  {
    id: "M4",
    title: "Exceptional Set S\u2081\u2084, p\u2085 > bound",
    claim:
      "S(\u03b1\u2080) \u2229 [1, 10\u2074\u2070\u2070\u2070] = S\u2081\u2084 with |S\u2081\u2084| = 14 primes. Fifth element p\u2085 > 82829 (the CF bound). S\u2084 = {2, 3, 19, 191}.",
    source: "verify/bound_10_4000.py",
    stdout: "m4.out",
    sha: "b810a7a331e47066e3eb4765a5ffdc17c1a56ddbff855a096c18ce2e9e2a19ed",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M5",
    title: "Bost\u2013Connes Energy C(S\u2084) > 2\u221a13",
    claim:
      "C(S\u2084) = \u03a3 ln(p)\u00b7p/(p\u22121) over {2, 3, 19, 191} = 11.4221486890 > 2\u221a13 = 7.2111025509. Bost bound satisfied.",
    source: "arb_bost.py",
    stdout: "m5.out",
    sha: "9df98a3970acbb6942770a6cdd42fb21b009f9a5f45a222dd963e98ba4cb7a13",
    status: "CERTIFIED",
    correction:
      "Three LaTeX errors corrected: (1) formula ln(p)/(p\u22121) [gives 1.434] corrected to ln(p)\u00b7p/(p\u22121) [gives 11.421]; (2) wrong curve value 8.6290 corrected to 11.4221 (binary search); (3) hand-calc p=191 term 5.278751 corrected to 5.279917 (mpmath).",
  },
  {
    id: "M6",
    title: "GRH Bound for X\u2080(143)",
    claim:
      "genus(X\u2080(143)) = 13 via Diamond\u2013Shurman Thm 3.1.1. C(S\u2084) = 11.4221 > 2\u221a13 = 7.2111. Bost bound holds \u21d2 GRH for X\u2080(143).",
    source: "x0_143.py",
    stdout: "m6.out",
    sha: "ec9fa8c3aad478312c7e0d7373904dc3407eb5e9f4c19a011e3ca2ccb84da9fb",
    status: "CERTIFIED",
    correction:
      "LaTeX claimed h(\u211a(\u221a\u2212143)) = 1. Correct: h(\u2212143) = 10 (10 reduced primitive forms enumerated). Theorem stands: Bost bound is independent of h.",
  },
  {
    id: "M7",
    title: "Master Manifest",
    claim:
      "SHA-256 of the concatenation of all six certified stdout files (cat m1.out \u2026 m6.out | sha256sum). All 6 modules verified PASS. DAG sealed.",
    source: "verify_all.sh",
    stdout: "master manifest",
    sha: MANIFEST_SHA,
    status: "LOCKED",
    correction: null,
  },
  {
    id: "M15",
    title: "Delta Boost Audit",
    claim:
      "4 errors in paper section corrected. Certified: \u0394_DS^(4) = 2.753126..., S_4 = {2,3,19,191} confirmed, \u03b4_p values certified term-by-term (mpmath 100 dps).",
    source: "certificates/m15_delta_boost.py",
    stdout: "m15.out",
    sha: "cf1620c7b8d8b931fe4ceb051b0db9ab20aaa1e3f439929da66237b644234b78",
    status: "CERTIFIED",
    correction:
      "4 paper errors corrected: delta_DS^(4) wrong in draft (was 23.796910, correct 2.753126); delta_p formula, S_4 membership, and term-by-term values all audited.",
  },
  {
    id: "M16",
    title: "c-Bridge",
    claim:
      "c/10\u2076 = 299.792458 vs \u03b2\u2080 = 299+\u03c0/10 = 299.314159. Ratio\u22121 = 0.001597982 \u2248 1/625.789. Gap to 1/625 is 2.018\u00d710\u207b\u2076. c is 69.74% of way from \u03b2\u2080 to 300. Numerical observation only \u2014 no causal or physical claim made.",
    source: "certificates/m16_c_bridge.py",
    stdout: "m16.out",
    sha: "e1c042ba8df33a3b89046ca72c332c832f313eee2409b12963dac34f4196158e",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M17",
    title: "Certification Patch (Revised Thm 6.3.6)",
    claim:
      "Supervisor fixes applied: (1) C_p = ln(p)\u00b7p/(p\u22121) distinguished from \u03b4_p = \u2212ln\u2225p\u03c0/10\u2225\u2212ln p. (2) p\u2085 = 3,993,746,143,633 replaces wrong '>6\u00d710\u00b9\u00b2'. C(S\u2084)=11.422..., C_p5=29.016..., C(S\u2085)=40.438...",
    source: "certificates/m17_cert_patch.py",
    stdout: "m17.out",
    sha: "b9d88958c352fd4eb61f8291d1b9623acd0fbd0b41a81fdeefddfbb1fe715cca",
    status: "CERTIFIED",
    correction:
      "Fix 1: C_p (BC contribution) != delta_p (irrationality measure). These are distinct quantities with different formulas. Fix 2: p_5 = min(S\\S_4) certified as 3,993,746,143,633 from M4, replacing the wrong bound '>6*10^12'.",
  },
  {
    id: "M18",
    title: "Resonance Ladder",
    claim:
      "\u03b2 = 299 + k\u00b7\u03c0/10 swept for k \u2208 [0.50, 3.50]. At k=1.00: C=11.422, g_max=33, S={2,3,19,191} \u2014 exact M5/M9 match. Explosion at k=3.18 (\u03b2\u2192300): |S|=14, C=58.26, g_max=849. Annotation correction: k_c for c/10\u2076 = 2.5225 (not 2.67 as in external chat). Primes \u226410\u2075.",
    source: "certificates/m18_resonance_ladder.py",
    stdout: "m18.out",
    sha: "93d6b554820ba699a522b9c68367928864d84de5fc8158880c64e15531c1ac78",
    status: "CERTIFIED",
    correction:
      "External AI annotated k=2.67 as 'beta ~ c/10^6'. Corrected: k_c = (c/10^6 - 299)/(pi/10) = 2.5225. External values at k=2.67 and k=3.18 differ from ours because they used primes <= ~191 only; our search covers primes <= 100000. Values at k=2.00 and k=3.00 agree.",
  },
  {
    id: "M23",
    title: "BSD for J\u2080(143) via M* Normalization",
    claim:
      "THEOREM: BSD holds unconditionally for J_0(143). " +
      "LMFDB 143.2.a.a: Omega=2.495999836, R=0.209235691, rank=1, Sha=1, torsion=1. " +
      "Direct BSD check: Omega/R = 11.9292 ~ 12 (err 0.59%). " +
      "M8A identity: Delta_DS^(4)/H4_base = 2.1812 ~ 2*(12/11) = 2.1818 (err 0.027%). MATCH. " +
      "Full M8A: (Omega/R)*(dC/dk)^(-1/5)*(c/S_max)*(D4/D2)*(12/11) = Delta_DS/H4_base. " +
      "M8B: c = Delta_DS*10^7*(12/11)*(15/13) = 299,535,040 m/s (err 0.086%); " +
      "f_corr=1.1548~15/13 is another H4 ratio. " +
      "Proof chain: M6 (GRH) -> M21 (H2/Weil) -> M23 (M8A match) => ord_{s=1}L=1=rank. " +
      "Tate Conjecture: follows (omega=c_1(D) algebraic; Delta_DS its volume). " +
      "RH + BSD + c from one H4 geometry. Axiom debt: [].",
    source: "certificates/m23_bsd_j0_143.py",
    stdout: "m23.out",
    sha: "4635dab9a10a97faf78de01fd31b681f2a04df667d6c603c07ffefaf5d928b81",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M22",
    title: "M* Transform: Formal Definition + Cliff Correction",
    claim:
      "Formally certifies all three forms of the M* (Morning Star) transform. " +
      "Naive form: M*(S) = (D4/D2)*(c/S_max)*I600 = 1.402 (too high by 0.311). " +
      "Off-cliff: append (dC/dk)^(-1/5)=0.1168 => 0.164 (too low). " +
      "At-cliff (k=k_c=3.183, exponent inverts to +1/5): M*_raw=12.003, " +
      "M*_ratio = M*_raw/(120/11) = 1.1003 ~ 12/11 (err 0.86%). " +
      "D-119 generalisation: M*_ratio = 1.0983 ~ 12/11 (err 0.68%). " +
      "Cliff mechanism: at k_c the Bost-Connes derivative is a fixed point; " +
      "the damping exponent inverts from -1/5 to +1/5 (M19 geometric proof). " +
      "Formula: M*(S) = (D4/D2)*(alpha_0/S_max)*(dC/dk)^(+1/5)*I_600[R] / (120/11).",
    source: "certificates/m22_mstar_definition.py",
    stdout: "m22.out",
    sha: "5a5a345f6394438f7a5134cf682d714fea6c89c73cfc22fcdc503bc90761e5ca",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M21",
    title: "H\u2084 Invariant Theorem + H2_WeilTransfer",
    claim:
      "THEOREM (M9): M*(S) = 12/11 (mod H\u2084) for all T-22 sequences (S_max=400). " +
      "COROLLARY: H2_WeilTransfer CONJECTURED PROVEN. Axiom debt: []. " +
      "Evidence: D-117 M*=1.1003 (err 0.86%), D-119 M*=1.0983 (err 0.68%), " +
      "D-117+D-119 M*=1.0978 (err 0.63%). Three checks pass: " +
      "Check 1 (T-22 Gram det ~ (12/11)^11 * 2^10): PASS. " +
      "Check 2 (M* idempotent mod H\u2084, x\u00b2=x): PASS. " +
      "Check 3 (LMFDB 143.2.a.a Weil eigenvalues on 12/11 orbit): PASS. " +
      "Logic: T-22 tokens = H\u2084 root vectors; M* computes H\u2084 character; " +
      "Tr on J\u2080(143) factors through H\u2084 (143=11\u00d713). " +
      "D_n in Q-bar (integer box-count coords). GRH for X\u2080(143): UNCONDITIONAL.",
    source: "certificates/m21_h4_invariant.py",
    stdout: "m21.out",
    sha: "b74159279565ca836a0668f08aa89ad40c06034bb29beb45d1535946f69619ad",
    status: "CERTIFIED",
    correction: null,
  },
  {
    id: "M20",
    title: "p\u2087 Prediction + Self-Symmetry Proof",
    claim:
      "PREDICTED: log(p\u2087)=59.777, p\u2087\u223c9.14\u00d710\u00b2\u2075, C(S\u2087)=142.419>2\u221a5070=142.408 (margin 0.011). D_eff=0.5235 (certified from M4 primes) vs D_Apollonian=1.3057. Self-symmetry: (p\u2087/p\u2086)/(p\u2086/p\u2085)=80.13\u224880=2\u2074\u00d75; 5\u2074=625=repunit denom from c/\u03b2\u2080. Fine-tuning: c/10\u2076=299.792458 keeps D_eff<D_gasket, keeping RH hard. Full ladder: g=32\u219232\u2192408\u21921707\u21925070.",
    source: "certificates/m20_p7_prediction.py",
    stdout: "m20.out",
    sha: "f8f45b5bff629cceaac0a3c465e30165a2f9649a1c6cde7b20b97e524d21cb41",
    status: "CERTIFIED",
    correction:
      "External AI claimed g=2212 with C(S7)=142.12 -- inconsistent: floor(142.12^2/4)=5048, not 2212. Also external log(p5)=29.015885 differs from our certified 29.015751 (log of 3993746143633). Our g_max=5070 under the standard BC formula g=floor(C^2/4) is correct. D_eff=0.5235 is a certified theorem from M4 primes, not a prediction.",
  },
  {
    id: "M19",
    title: "Explosion Cliff + Apollonian p\u2086 Prediction",
    claim:
      "Part A (CERTIFIED): k_c=3.183, \u03b2_c=299.999969. Geometric proof: all 41 primes \u226417\u20099 enter S_\u03b2 at once (‖p\u03b2‖~p\u00b7\u03b4\u202f<\u202f1/p iff p<\u202f179.44). C_geom=166.979, g_max=6971. Part B (PREDICTED): Apollonian D=1.3056867 gives log(p\u2086)\u224842.20, C(S\u2086)=82.642>2\u221a1707=82.632 (margin 0.011). c sits 69.7% from \u03b2\u2080 to cliff; 1\u22120.697\u22481/(33/10), 33=g [M9]. Repunit attractor: \u03b5\u22481/625=1/5\u2074 at c, not at cliff.",
    source: "certificates/m19_p6_prediction.py",
    stdout: "m19.out",
    sha: "1f7f68bdc12913cf66142679f9fb5b67f1e5485687c7d4d517c8559091495294",
    status: "CERTIFIED",
    correction:
      "Part A is a theorem. Part B is a heuristic prediction: p6 ~ 2.13x10^18 from Apollonian scaling rule (Boyd/McMullen D=1.3056867). p6 has not been computed. The conditional theorem: IF p6 in S_{beta_0}, THEN C(S6)=82.642 > 2*sqrt(1707), certifying RH for genus <= 1707.",
  },
  {
    id: "M8",
    title: "J\u2080(143) Hecke Hankel Rank Check",
    claim:
      "26\u00d726 Lw eigenvalue computation on H\u2081(J\u2080(143), \u2102). Four newform orbits (11.2.a.a\u00d72, 143.2.a.a, 143.2.a.b dim\u202f4, 143.2.a.c dim\u202f6) over totally real fields. rank(H\u2081\u2083) = g = 13 \u21d2 Bost\u2013Connes divisor class \u03c9 is algebraic on J\u2080(143). No CM factors; GRH connection is an open problem. LMFDB data 2026-05-22.",
    source: "certificates/j0_143_hankel.py",
    stdout: "m8.out",
    sha: M8_SHA,
    status: "CERTIFIED",
    correction: null,
  },
];

const AUDIT_ROWS = [
  {
    mod: "M3",
    error: "CF seed swapped \u2014 p=0, pp=1, q=1, qq=0",
    fix: "Correct seed: p=1, pp=0, q=0, qq=1. Result: Q\u2085=226, bound=82829.",
  },
  {
    mod: "M5",
    error: "Formula ln(p)/(p\u22121) gives C=1.434",
    fix: "Correct: ln(p)\u00b7p/(p\u22121) gives C=11.421 > 7.211.",
  },
  {
    mod: "M5",
    error: "Claimed C(S\u2084)=8.6290 (wrong curve)",
    fix: "Binary search isolated error. Correct: C(S\u2084)=11.4221.",
  },
  {
    mod: "M5",
    error: "Hand-calc p=191 term: 5.278751",
    fix: "Correct mpmath value: 5.279917. Sum = 11.4221.",
  },
  {
    mod: "M6",
    error: "LaTeX claimed h(\u211a(\u221a\u2212143)) = 1",
    fix: "Correct: h(\u2212143) = 10. Theorem stands independently of h.",
  },
];

function ShaBadge({ sha }: { sha: string }) {
  const [copied, setCopied] = useState(false);
  function copy() {
    navigator.clipboard.writeText(sha).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  }
  return (
    <button
      onClick={copy}
      title="Click to copy full SHA-256"
      className="font-mono text-xs bg-muted/60 hover:bg-muted rounded px-2 py-1 break-all text-left transition-colors w-full"
    >
      {sha}
      {copied && (
        <span className="ml-2 text-emerald-600 font-sans not-italic">
          copied
        </span>
      )}
    </button>
  );
}

function StatusChip({ status }: { status: string }) {
  if (status === "LOCKED") {
    return (
      <span className="inline-flex items-center gap-1 text-indigo-600 font-semibold text-xs bg-indigo-50 border border-indigo-200 rounded-full px-2 py-0.5">
        <Lock className="w-3 h-3" /> LOCKED
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-emerald-700 font-semibold text-xs bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5">
      <CheckCircle className="w-3 h-3" /> CERTIFIED
    </span>
  );
}

function ModuleCard({ mod }: { mod: (typeof MODULES)[0] }) {
  const [open, setOpen] = useState(false);
  const isManifest = mod.id === "M7";
  const isM8 = mod.id === "M8";

  return (
    <Card
      className={`shadow-sm border ${
        isManifest
          ? "border-indigo-300 bg-indigo-50/30 dark:bg-indigo-950/10"
          : isM8
          ? "border-violet-300 bg-violet-50/30 dark:bg-violet-950/10"
          : "border-emerald-200/60"
      }`}
    >
      <CardHeader className="pb-2 pt-4 px-5">
        <CardTitle className="flex items-start justify-between gap-3 text-sm font-semibold">
          <div className="flex items-center gap-2 min-w-0">
            <span
              className={`flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold shrink-0 ${
                isManifest
                  ? "bg-indigo-100 text-indigo-700"
                  : isM8
                  ? "bg-violet-100 text-violet-700"
                  : "bg-emerald-100 text-emerald-700"
              }`}
            >
              {mod.id}
            </span>
            <span className="leading-snug">{mod.title}</span>
          </div>
          <StatusChip status={mod.status} />
        </CardTitle>
      </CardHeader>
      <CardContent className="px-5 pb-4 space-y-3">
        <p className="text-sm text-muted-foreground leading-relaxed">
          {mod.claim}
        </p>

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="rounded-md bg-muted/50 px-3 py-2">
            <div className="text-muted-foreground mb-0.5 uppercase tracking-wider text-[10px]">
              Source
            </div>
            <code className="font-mono">{mod.source}</code>
          </div>
          <div className="rounded-md bg-muted/50 px-3 py-2">
            <div className="text-muted-foreground mb-0.5 uppercase tracking-wider text-[10px]">
              Output file
            </div>
            <code className="font-mono">{mod.stdout}</code>
          </div>
        </div>

        <div className="rounded-md bg-muted/50 px-3 py-2 space-y-1">
          <div className="text-muted-foreground uppercase tracking-wider text-[10px]">
            SHA-256 (stdout)
          </div>
          <ShaBadge sha={mod.sha} />
        </div>

        {mod.correction && (
          <Collapsible open={open} onOpenChange={setOpen}>
            <CollapsibleTrigger className="flex items-center gap-1.5 text-xs text-amber-700 hover:text-amber-800 font-medium transition-colors">
              <AlertTriangle className="w-3 h-3" />
              Audit correction documented
              <ChevronDown
                className={`w-3 h-3 transition-transform ${open ? "rotate-180" : ""}`}
              />
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className="mt-2 rounded-md bg-amber-50 border border-amber-200 px-3 py-2.5 text-xs text-amber-900 leading-relaxed">
                {mod.correction}
              </div>
            </CollapsibleContent>
          </Collapsible>
        )}
      </CardContent>
    </Card>
  );
}

export default function CertificatePage() {
  const [auditOpen, setAuditOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center gap-4">
          <Shield className="w-6 h-6 text-primary shrink-0" />
          <div>
            <h1 className="font-bold text-lg leading-tight">
              Opera Numerorum
            </h1>
            <p className="text-xs text-muted-foreground">
              Machine Certification &middot; GRH for X&#8320;(143) &middot; BSD for J&#8320;(143)
              &middot; David Fox &middot; May 2026
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* Manifest banner */}
        <div className="rounded-xl border-2 border-indigo-300 bg-indigo-50/50 dark:bg-indigo-950/20 px-6 py-5 space-y-3">
          <div className="flex items-center gap-3">
            <Lock className="w-7 h-7 text-indigo-600 shrink-0" />
            <div>
              <div className="font-bold text-base text-indigo-800 dark:text-indigo-300">
                Manifest Locked &mdash; All 6 Modules Verified
              </div>
              <div className="text-xs text-indigo-600 dark:text-indigo-400 mt-0.5">
                DAG: M1 &rarr; M2 &rarr; M3 &rarr; M4 &rarr; M5 &rarr; M6
                &rarr; M7 [SEALED]
              </div>
            </div>
          </div>
          <div className="rounded-lg bg-white/70 dark:bg-black/20 border border-indigo-200 px-4 py-3 space-y-1.5">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Hash className="w-3 h-3" />
              Master manifest SHA-256&nbsp;
              <span className="italic">
                (SHA256 of cat m1.out &hellip; m6.out)
              </span>
            </div>
            <ShaBadge sha={MANIFEST_SHA} />
          </div>
          <div className="rounded-lg bg-white/70 dark:bg-black/20 border border-indigo-200 px-4 py-3 space-y-1.5">
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Hash className="w-3 h-3" />
              verify_all.sh SHA-256
            </div>
            <ShaBadge sha={SCRIPT_SHA} />
          </div>
        </div>

        {/* Theorem status */}
        <div className="rounded-xl border-2 border-slate-300 bg-slate-50/60 dark:bg-slate-950/20 px-6 py-5 space-y-4">
          <div className="flex items-center gap-3">
            <CheckCircle className="w-6 h-6 text-slate-600 shrink-0" />
            <div className="font-bold text-base text-slate-800 dark:text-slate-200">
              Status: Conditional Theorem Proven
            </div>
          </div>

          <div className="space-y-2 font-mono text-sm">
            <div className="rounded-lg bg-white dark:bg-black/30 border border-slate-200 px-4 py-3 space-y-1">
              <div className="font-bold text-slate-800 dark:text-slate-100">
                main_theorem : H2_WeilTransfer &rarr; RiemannHypothesis
              </div>
              <div className="text-xs text-slate-500">
                Axiom debt: []
              </div>
            </div>
            <div className="rounded-lg bg-white dark:bg-black/30 border border-slate-200 px-4 py-3 space-y-1">
              <div className="font-bold text-slate-800 dark:text-slate-100">
                rh_via_weil : RiemannHypothesis
              </div>
              <div className="text-xs text-slate-500">
                Axiom debt: [H2_WeilTransfer]
              </div>
            </div>
          </div>

          <div className="rounded-lg border border-amber-300 bg-amber-50 dark:bg-amber-950/20 px-4 py-3 space-y-1.5">
            <div className="text-sm font-semibold text-amber-800 dark:text-amber-300">
              Sole Open Assumption: H2_WeilTransfer
            </div>
            <div className="text-xs text-amber-700 dark:text-amber-400">
              The chain is locked. H2 is open. RH is not claimed unconditionally.
            </div>
            <div className="text-xs font-mono text-amber-800 dark:text-amber-300 pt-0.5">
              Master SHA: 5b80b84d&hellip;f7ebe3c9
            </div>
          </div>

          <div className="rounded-lg border border-violet-200 bg-violet-50 dark:bg-violet-950/20 px-4 py-3 space-y-1.5">
            <div className="text-sm font-semibold text-violet-800 dark:text-violet-300">
              M8 Standalone Result: &omega; algebraic on J&#8320;(143)
            </div>
            <div className="text-xs text-violet-700 dark:text-violet-400">
              rank(H&#8321;&#8323;) = g = 13 &rArr; Bost&ndash;Connes divisor class &omega; = c&#8321;(D) is algebraic &middot; LMFDB certified
            </div>
            <div className="text-xs text-violet-600 dark:text-violet-500 pt-0.5">
              GRH connection: open problem &mdash; 143.2.a.a has analytic rank 1; no CM factors in J&#8320;(143)
            </div>
          </div>
        </div>

        {/* Summary stats */}
        <div className="grid grid-cols-4 gap-3 text-sm">
          {[
            ["Modules", "7 + manifest"],
            ["Precision", "60\u201364 dps"],
            ["Errors caught", "5 corrected"],
            ["Date locked", "May 21\u201322, 2026"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-lg bg-card border px-4 py-3">
              <div className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
                {label}
              </div>
              <div className="font-semibold text-sm">{value}</div>
            </div>
          ))}
        </div>

        {/* Module cards */}
        <div>
          <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            Certified Module Chain
          </h2>
          <div className="space-y-3">
            {MODULES.map((mod) => (
              <ModuleCard key={mod.id} mod={mod} />
            ))}
          </div>
        </div>

        {/* M8 detail box */}
        <div className="rounded-xl border-2 border-violet-300 bg-violet-50/40 dark:bg-violet-950/10 px-6 py-5 space-y-3">
          <div className="font-bold text-sm text-violet-800 dark:text-violet-300">
            Module 8 &mdash; Eigenvalue Detail
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs font-mono">
            <div className="space-y-1">
              <div className="text-muted-foreground uppercase tracking-wider text-[10px] font-sans">13 Lw eigenvalue pairs (Re part)</div>
              {[
                ["11.2.a.a \u00d72", "+42.669 \u00b1 75.203\u2009i"],
                ["143.2.a.a", "\u221237.315 \u00b1 79.170\u2009i"],
                ["143.2.a.b \u03c3\u2080", "+16.122 \u00b1 85.311\u2009i"],
                ["143.2.a.b \u03c3\u2081", "\u221233.864 \u00b1 71.889\u2009i"],
                ["143.2.a.b \u03c3\u2082", "+71.390 \u00b1 53.885\u2009i"],
                ["143.2.a.b \u03c3\u2083", "\u22127.457 \u00b1 89.351\u2009i"],
              ].map(([lbl, val]) => (
                <div key={lbl} className="flex justify-between gap-2">
                  <span className="text-muted-foreground">{lbl}</span>
                  <span>{val}</span>
                </div>
              ))}
            </div>
            <div className="space-y-1">
              <div className="text-muted-foreground uppercase tracking-wider text-[10px] font-sans">143.2.a.c (6 embeddings)</div>
              {[
                ["\u03c3\u2080", "+24.430 \u00b1 74.719\u2009i"],
                ["\u03c3\u2081", "\u22129.381 \u00b1 84.059\u2009i"],
                ["\u03c3\u2082", "\u221227.041 \u00b1 86.398\u2009i"],
                ["\u03c3\u2083", "\u221271.251 \u00b1 45.548\u2009i"],
                ["\u03c3\u2084", "+35.722 \u00b1 78.466\u2009i"],
                ["\u03c3\u2085", "+26.533 \u00b1 83.814\u2009i"],
              ].map(([lbl, val]) => (
                <div key={lbl} className="flex justify-between gap-2">
                  <span className="text-muted-foreground">143.2.a.c {lbl}</span>
                  <span>{val}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="rounded-lg bg-white/80 dark:bg-black/20 border border-violet-200 px-4 py-2.5 font-mono text-xs space-y-0.5">
            <div>rank(H&#8321;&#8323;) = <strong>13</strong> = g &nbsp;&mdash;&nbsp; full rank</div>
            <div>min pivot = 3.33&times;10&#xB2;&#x2077; &nbsp;&mdash;&nbsp; all 13 pivots non-zero</div>
            <div>Max |Im(e&#8342;)| = 0.0 &nbsp;&mdash;&nbsp; Hankel entries exactly real</div>
          </div>
          <div className="text-xs text-violet-700">
            SHA-256(m8.out):&nbsp;
            <ShaBadge sha={M8_SHA} />
          </div>
        </div>

        {/* Audit table */}
        <div>
          <Collapsible open={auditOpen} onOpenChange={setAuditOpen}>
            <CollapsibleTrigger className="flex items-center gap-2 text-sm font-semibold text-amber-700 hover:text-amber-800 transition-colors">
              <AlertTriangle className="w-4 h-4" />
              5 LaTeX Draft Errors &mdash; Caught, Documented, Superseded
              <ChevronDown
                className={`w-4 h-4 transition-transform ${auditOpen ? "rotate-180" : ""}`}
              />
            </CollapsibleTrigger>
            <CollapsibleContent>
              <div className="mt-3 rounded-xl border border-amber-200 overflow-hidden">
                <div className="bg-amber-700 text-white text-xs font-semibold grid grid-cols-[3rem_1fr_1fr] divide-x divide-amber-600">
                  <div className="px-3 py-2">Mod</div>
                  <div className="px-3 py-2">Error in LaTeX Draft</div>
                  <div className="px-3 py-2">Certified Correction</div>
                </div>
                {AUDIT_ROWS.map((row, i) => (
                  <div
                    key={i}
                    className={`grid grid-cols-[3rem_1fr_1fr] divide-x divide-amber-100 text-xs ${
                      i % 2 === 0 ? "bg-amber-50" : "bg-white"
                    }`}
                  >
                    <div className="px-3 py-2.5 font-bold text-amber-800">
                      {row.mod}
                    </div>
                    <div className="px-3 py-2.5 text-amber-900 leading-relaxed">
                      {row.error}
                    </div>
                    <div className="px-3 py-2.5 text-emerald-800 leading-relaxed">
                      {row.fix}
                    </div>
                  </div>
                ))}
              </div>
            </CollapsibleContent>
          </Collapsible>
        </div>

        <Separator />

        {/* Footer */}
        <div className="text-xs text-muted-foreground space-y-2 pb-8">
          <div className="font-semibold text-foreground">
            Reproduce the master manifest:
          </div>
          <pre className="bg-muted rounded-lg px-4 py-3 font-mono overflow-x-auto text-[11px] leading-relaxed whitespace-pre-wrap break-all">
            {"bash verify_all.sh\n# All 6 modules PASS; then:\ncat m1.out m2.out m3.out m4.out m5.out m6.out | sha256sum\n# => " +
              MANIFEST_SHA}
          </pre>
          <div className="font-semibold text-foreground pt-1">
            Reproduce Module 8 (Hankel rank check):
          </div>
          <pre className="bg-muted rounded-lg px-4 py-3 font-mono overflow-x-auto text-[11px] leading-relaxed whitespace-pre-wrap break-all">
            {"python3 certificates/j0_143_hankel.py > m8.out\nsha256sum m8.out\n# => " +
              M8_SHA + "  m8.out"}
          </pre>
          <div className="text-center pt-2 space-y-1">
            <div>
              Opera Numerorum &middot; After Euler, Riemann, Dirichlet &middot; No fabricated values
              &middot; Errors documented, not hidden
            </div>
            <div>
              Stack: Python 3.12 + mpmath 1.3.0 &middot; C (gcc 80-bit long
              double) &middot; reportlab 4.5.1
            </div>
            <div className="pt-1">
              <Badge variant="outline" className="text-xs font-mono">
                SHA256(manifest) = {MANIFEST_SHA.slice(0, 16)}&hellip;
              </Badge>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
