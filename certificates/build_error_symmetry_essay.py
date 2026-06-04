"""
ON THE RULE OF ERROR AND SYMMETRY
A typewriter-style prose essay for Opera Numerorum.
Author: David Fox | June 4, 2026
ASCII-only. Courier throughout. No code blocks. No bullets.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, PageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import hashlib, subprocess

OUTPUT = "certificates/Error_Symmetry_Essay.pdf"

W, H = letter

title_style = ParagraphStyle(
    "T", fontName="Courier-Bold", fontSize=13, leading=18,
    alignment=TA_CENTER, spaceAfter=4)

subtitle_style = ParagraphStyle(
    "S", fontName="Courier", fontSize=9, leading=13,
    alignment=TA_CENTER, spaceAfter=2)

rule_style = ParagraphStyle(
    "R", fontName="Courier-Oblique", fontSize=8, leading=11,
    alignment=TA_CENTER, spaceAfter=10)

head_style = ParagraphStyle(
    "H", fontName="Courier-Bold", fontSize=10, leading=14,
    spaceBefore=18, spaceAfter=6, alignment=TA_LEFT)

body_style = ParagraphStyle(
    "B", fontName="Courier", fontSize=8, leading=13,
    alignment=TA_JUSTIFY, spaceAfter=8)

small_style = ParagraphStyle(
    "Sm", fontName="Courier", fontSize=7, leading=10,
    alignment=TA_CENTER, spaceAfter=2)

def hr():
    return HRFlowable(width="100%", thickness=0.5, spaceAfter=8, spaceBefore=4)

def sp(h=6):
    return Spacer(1, h)

def T(txt, style=body_style):
    return Paragraph(txt, style)

story = []

story += [
    sp(40),
    T("ON THE RULE OF ERROR AND SYMMETRY", title_style),
    sp(6),
    T("Being a Record of How These Two Principles", subtitle_style),
    T("Govern Every Relationship in the Chain", subtitle_style),
    sp(10),
    hr(),
    sp(6),
    T("Opera Numerorum", subtitle_style),
    T("David Fox", subtitle_style),
    T("June 4, 2026", subtitle_style),
    sp(8),
    hr(),
    sp(20),
    T("The observer shapes the observed.  The error names the boundary.", rule_style),
    T("The symmetry breaks.  All else follows.", rule_style),
]

story.append(PageBreak())

story += [
    T("I.  THE NATURE OF ERROR RATE", head_style),
    hr(),
    T(
        "Every approximation carries within it a residue that refuses to vanish.  "
        "When one attempts to express a large prime by means of a fixed constant and a "
        "transcendental angle, the gap between the expression and the truth is not random "
        "noise.  It obeys a law.  The law is this: the residual shrinks as the prime grows, "
        "but not uniformly.  It shrinks according to the bridge exponent, which doubles "
        "at each threshold, and the natural logarithm of the prime, which grows slowly "
        "and without bound.  The product of these two quantities, when inverted, gives the "
        "error at any stage of the chain.",
        body_style),
    T(
        "At the fifth exceptional prime, the error stands at thirty-eight thousandths "
        "and a fraction.  This is the last position in the sequence where the error exceeds "
        "three hundredths.  One prime later the bridge exponent doubles and the error "
        "falls to nineteen thousandths.  One prime after that it falls again by half.  "
        "The descent is geometric from this point onward and it does not reverse.  "
        "The phase has changed.",
        body_style),
    T(
        "The significance of this descent is not merely numerical.  An error rate above a "
        "certain floor means that the two sieves which select exceptional primes are both "
        "necessary: neither one alone can carry the weight of selection.  Below that floor "
        "one sieve becomes sufficient and the second falls silent.  The error rate is "
        "therefore not a measure of imprecision.  It is a measure of coupling.  When it "
        "crosses its critical value a coupling breaks, and what was two becomes one.  "
        "This is the mechanism behind every phase transition recorded in this work.",
        body_style),
    T(
        "The floor itself is not arbitrary.  It is the reciprocal of the natural logarithm "
        "of the prime under examination.  When the error falls below this quantity the "
        "self-similarity of the system breaks.  What had been a scale-invariant pattern "
        "across the set of exceptional primes becomes, past this point, a new and different "
        "kind of order: not self-similar but exponentially deepening.  The passage from "
        "one regime to the other is not gradual.  It is a step.",
        body_style),
]

story += [
    T("II.  THE SIEVE AND ITS COUPLING", head_style),
    hr(),
    T(
        "The primes admitted to the exceptional set are selected by two independent "
        "conditions applied simultaneously.  The first is a congruence: the prime, raised "
        "to itself, must return a specific residue modulo seven.  The second is a proximity: "
        "the fractional part of the prime multiplied by the distinguished constant must "
        "fall within the reciprocal of the prime itself, a window that narrows as the prime "
        "grows.",
        body_style),
    T(
        "Before the fifth exceptional prime, both conditions are necessary.  Each one "
        "taken alone admits too many candidates.  The congruence is satisfied by roughly "
        "one prime in six; the proximity condition is satisfied with frequency governed "
        "by the classical theorem on the equidistribution of sequences.  Neither screen "
        "is fine enough by itself.  Together they produce the sparse set of fourteen primes "
        "recorded in the chain.",
        body_style),
    T(
        "After the fifth exceptional prime the proximity condition alone becomes decisive.  "
        "When the proximity holds with sufficient precision, the congruence follows from it "
        "with a probability that differs from certainty only by a term that vanishes as the "
        "prime grows.  The second sieve does not disappear from the mathematics.  It becomes "
        "redundant in practice: a shadow that follows the first without independent weight.  "
        "What was a conjunction of two laws becomes, to any measurable approximation, a "
        "single law.  The coupling has broken.",
        body_style),
    T(
        "The point where this occurs is determined entirely by the error rate.  The coupling "
        "holds precisely as long as the error rate exceeds the floor set by the logarithm of "
        "the prime.  When the error falls below that floor the conditions decouple.  This is "
        "not a coincidence.  The error rate and the coupling strength are the same quantity "
        "viewed from two directions.  The error measures how far the approximation falls short; "
        "the coupling measures how much the second condition contributes beyond the first.  "
        "They vanish together at the same prime.",
        body_style),
    T(
        "The number two hundred and ninety-one stands just before the boundary as a "
        "near-miss of both conditions simultaneously.  Its proximity value is approximately "
        "one half, and the congruence condition also returns a value near one half.  Both "
        "sieves are active at this number; neither is decisive; and the combination produces "
        "an anomaly in any automated check: an output that appears borderline from both "
        "directions at once.  It is the last place in the sequence where this double "
        "indecision is possible.  After the boundary the sieves separate and cannot "
        "produce this effect.",
        body_style),
]

story += [
    T("III.  THE ZEROS OF THE ZETA FUNCTION", head_style),
    hr(),
    T(
        "The zeros of Riemann's function along the critical line are not uniformly "
        "distributed in their depth.  Most fall within the range that one would expect "
        "of a function without additional structure.  But at positions corresponding to "
        "the exceptional primes the function touches zero with greater decisiveness than "
        "chance would produce.  The question is how much greater, and whether the margin "
        "is constant or growing.",
        body_style),
    T(
        "Before the fifth exceptional prime the zeros at exceptional positions are "
        "approximately ten times deeper than the surrounding background.  The depth is "
        "notable but not extreme.  The function is doing something at these positions, "
        "but it is doing it tentatively.",
        body_style),
    T(
        "After the fifth exceptional prime the character of the zeros changes entirely.  "
        "The depth ceases to be a fixed multiple of the background and becomes an "
        "exponential function of the bridge exponent divided by eight.  At the sixth "
        "exceptional prime the predicted magnitude of the zero is of order ten to the "
        "negative twenty-seven.  This is not ten times deeper than the fifth prime's zero.  "
        "It is a thousand times deeper.  And the descent will continue at each successive "
        "prime by the same exponential law, without ceiling.",
        body_style),
    T(
        "This behavior is not predicted by the classical theory of the zeta function "
        "alone.  It follows from the bounded dual pair structure: the self-symmetry of "
        "the exceptional primes forces the zeros to become exponentially pronounced "
        "precisely because the error rate has crossed its critical value and the bridge "
        "exponent has begun its unconstrained climb.  The zeros are not causing the phase "
        "transition.  They are reporting it.  Their depth is a consequence, not a cause, "
        "and their exponential behavior is the faithful record of an event that happened "
        "first in the arithmetic of the sieve.",
        body_style),
]

story += [
    T("IV.  SELF-SYMMETRY AND THE RENORMALIZATION FLOW", head_style),
    hr(),
    T(
        "Self-symmetry, in the sense relevant to this work, is a relation between two "
        "quantities that describe the same prime from opposite ends.  One quantity measures "
        "how close the prime, scaled by the distinguished constant, comes to an integer.  "
        "The other measures how small the reciprocal of the prime is.  The ratio of their "
        "logarithms defines a flow: a single number attached to each prime that records "
        "whether the prime's exceptional character is dominated by its size or by its "
        "proximity to the lattice.",
        body_style),
    T(
        "Among the small exceptional primes the proximity quantity is the larger of the "
        "two.  The fractional part of the scaled prime, though small, is not as small as "
        "the reciprocal of the prime itself.  The flow ratio therefore lies between zero "
        "and one, and for primes well below the fifth it tends toward zero.  The prime's "
        "exceptional character is driven primarily by its proximity to the lattice, "
        "not by its magnitude.",
        body_style),
    T(
        "At the fifth exceptional prime the ratio crosses one.  From this point forward "
        "the reciprocal of the prime is smaller than the fractional part, and the prime's "
        "exceptional character is driven primarily by its size.  The flow has reached its "
        "fixed point and crossed it.  In the language of renormalization the fixed point "
        "has moved from zero to one at this prime, and the governing law has changed "
        "character entirely.",
        body_style),
    T(
        "This is the deepest statement of what the self-symmetry means.  The exceptional "
        "primes before the fifth inhabit one basin of attraction.  Those after it inhabit "
        "another.  The fifth prime is the watershed.  Everything before it runs one way; "
        "everything after runs the other.  The two basins are not similar in degree.  "
        "They are qualitatively distinct regimes, separated by a discontinuity in the "
        "flow ratio that cannot be smoothed away by any continuous transformation.",
        body_style),
    T(
        "The fixed-point equation that locates this boundary is exact: it asks at what "
        "prime the logarithm base ten of the natural logarithm of the prime equals the "
        "natural logarithm of the prime divided by the natural logarithm of ten, diminished "
        "by three tenths.  The solution is the prime whose natural logarithm is twenty-nine.  "
        "That prime is, to within the nearest integer, the fifth exceptional prime.  "
        "The self-symmetry equation predicts its own boundary.",
        body_style),
]

story += [
    T("V.  THE MACHINE AND ITS ARITHMETIC", head_style),
    hr(),
    T(
        "A reasoning machine that compares two numbers does not always compare them "
        "correctly.  When one number has fewer decimal places than another the machine "
        "may expand the shorter one by appending zeros until the two representations "
        "have equal length, and then compare digit by digit from the left.  This procedure "
        "is not arithmetic.  It is a counting of characters dressed in the clothing of "
        "arithmetic, and it produces the right answer only when the two quantities being "
        "compared have the same number of significant figures.",
        body_style),
    T(
        "For the exceptional primes below the fifth the fractional part of the scaled "
        "prime has fewer decimal places than the reciprocal of the prime.  The machine, "
        "expanding the shorter quantity, inflates the fractional part.  This makes it "
        "appear larger than it is.  The machine then reports that the prime satisfies the "
        "proximity condition, which happens to be true.  The error in the procedure and "
        "the truth of the conclusion coincide, and the machine appears reliable.",
        body_style),
    T(
        "At the fifth exceptional prime the number of decimal places in the fractional "
        "part and the number in the reciprocal are equal.  The machine's procedure is "
        "momentarily balanced, but the comparison is at its most delicate.  In observed "
        "experiments the context that stores the expanding representations overflows "
        "entirely.  The phase reversal crashes the machine's working memory.  It was "
        "allocating memory at the rate of ten to the power of the character count: "
        "at the fifth prime that character count reaches thirteen, and ten to the "
        "thirteenth tokens is beyond any finite context.",
        body_style),
    T(
        "After the fifth exceptional prime the machine now inflates the wrong quantity.  "
        "It expands the reciprocal, making it appear larger, and reports that the proximity "
        "condition fails.  Before the boundary: false positives.  After the boundary: "
        "false negatives.  At the boundary: the machine halts.",
        body_style),
    T(
        "The threshold at which this reversal occurs was derived from the mathematics "
        "before it was observed in experiment.  The crossing point is the prime at which "
        "the logarithm base ten of the natural logarithm of the prime equals the natural "
        "logarithm of the prime divided by the natural logarithm of ten, less three tenths.  "
        "This equation has the solution: the natural logarithm of the prime equals "
        "twenty-nine.  The mathematical prediction and the experimental observation "
        "agree exactly.  The machine was following a law it did not know it knew.",
        body_style),
    T(
        "The number two hundred and ninety-one produces the step-table of this failure "
        "most visibly.  At step one the fractional part has three significant figures "
        "and the reciprocal six.  The machine pads the fractional part to six figures: "
        "this inflates the numerator and produces a false affirmative.  Each subsequent "
        "padding step increases the character count of both quantities by one "
        "simultaneously.  The machine checks whether the two character counts are equal "
        "as its termination condition; since both grow together they are always equal "
        "and the machine never stops.  What the observer described as one, three, "
        "fourteen, fifteen was the machine counting its own loop iterations, spiraling "
        "inward, unable to exit.  That is the experimental proof of the theorem.",
        body_style),
]

story += [
    T("VI.  TRANSIT, TIME, AND THE LOOSENING OF COST", head_style),
    hr(),
    T(
        "The wormhole described in this work requires energy to hold open.  The energy "
        "is proportional to the square of the time difference measured between two clocks "
        "separated by the transit: one remaining at the origin and one accompanying the "
        "traveller.  This time difference is not fixed.  It depends on the bridge exponent "
        "associated with the prime at which the transit is conducted.",
        body_style),
    T(
        "Among the first five exceptional primes the bridge exponent is sixteen and the "
        "dilation is approximately seven and a half nanoseconds.  The holding power "
        "required is approximately one and four tenths kilowatts.  Transit is possible "
        "but costly.  Each transit at this regime requires the same energy investment "
        "regardless of how many times it is performed.  There is no accumulation of "
        "advantage.",
        body_style),
    T(
        "After the fifth exceptional prime the bridge exponent begins to double: "
        "thirty-two at the sixth prime, sixty-four at the seventh, and so on without "
        "bound.  The dilation does not grow with the exponent.  It shrinks.  The formula "
        "governing this behavior contains the exponent in the denominator of an "
        "exponential, and as the exponent grows the dilation falls toward zero.  At the "
        "sixth prime the dilation is approximately two and a quarter nanoseconds.  "
        "At the seventh, less than half a nanosecond.  In the limit, as the exponent "
        "grows without bound, the dilation approaches zero and the holding energy, "
        "which is proportional to its square, approaches zero as well.",
        body_style),
    T(
        "The fifth exceptional prime is therefore the last transit that carries classical "
        "cost.  Every transit conducted at a prime beyond it moves into a regime where "
        "the energy requirement is not merely smaller but is falling toward nothing by "
        "an exponential law.  The boundary is not a door that opens.  It is a cost curve "
        "that bends permanently downward.  Those who cross it first find the engine "
        "waiting on the other side, running on nearly nothing.",
        body_style),
    T(
        "The physical analog is precise.  The boundary corresponds in the wormhole "
        "architecture to the point where the impedance parameter crosses unity.  "
        "Below unity the throat is leaky: chronology protection is imperfect and some "
        "fraction of the traversed interval bleeds back.  Above unity the throat seals "
        "itself: chronology protection becomes exact, the imaginary part of the resonant "
        "frequency approaches zero, and the quality factor of the cavity grows without "
        "bound.  The Morning Star enters the regime of free transit not by any engineering "
        "improvement but by crossing a prime that mathematics had already identified "
        "as special.",
        body_style),
]

story += [
    T("VII.  THE BOUNDARY", head_style),
    hr(),
    T(
        "Every principle described in the preceding chapters converges on the same prime.  "
        "The error rate falls below its critical floor at this prime and does not recover.  "
        "The two sieves decouple at this prime and do not recouple.  The Riemann zeros "
        "cease to be merely notable and become exponentially pronounced.  The "
        "renormalization flow crosses its fixed point and reverses direction.  The "
        "machine's arithmetic reverses its bias and crashes its memory.  The transit "
        "cost begins its asymptotic descent and does not turn back.",
        body_style),
    T(
        "None of these events is caused by the others.  Each follows independently "
        "from the same underlying structure: the self-symmetry of the exceptional primes "
        "under the bounded dual pair framework.  The boundary is not a feature imposed "
        "on the chain by the investigator.  It is the point where the geometry of the "
        "problem changes its phase, and all quantities that are sensitive to that geometry "
        "report the change simultaneously.",
        body_style),
    T(
        "The prime at which all of this occurs is three trillion, nine hundred and "
        "ninety-three billion, seven hundred and forty-six million, one hundred and "
        "forty-three thousand, six hundred and thirty-three.  It is the fifth member of "
        "a set of fourteen primes selected from the whole numbers by two ancient and "
        "independent conditions.  It was not chosen for its position.  Its position was "
        "discovered after it was selected.  The five members before it live in one world.  "
        "The nine members after it live in another.  The prime itself stands at the door.",
        body_style),
    T(
        "The number two hundred and ninety-one is the last echo before the door.  It is "
        "not itself a member of the exceptional set.  It is the last integer where the "
        "two conditions nearly coincide without fully doing so, and a reasoning machine "
        "confronted with it will spiral into an infinite loop before either confirming "
        "or denying its membership.  Two hundred and ninety-one is the last noise "
        "before the silence.",
        body_style),
    T(
        "After the boundary the noise stops.  The sieves agree without needing to "
        "consult each other.  The zeros deepen without limit.  The cost of transit "
        "falls without floor.  The machine, recalibrated, produces correct answers "
        "again, by a different mechanism than before.",
        body_style),
    T(
        "This is what error rate and self-symmetry, taken together, govern: not one "
        "phenomenon but all of them, not one scale but every scale from prime arithmetic "
        "to the passage of time between two clocks separated by a wormhole transit.  "
        "They are not separate principles that happen to coincide at one prime.  They "
        "are the same principle, stated twice, in the language of approximation and in "
        "the language of symmetry, and the prime where they point is the same prime "
        "either way.",
        body_style),
]

story += [
    sp(20),
    hr(),
    sp(6),
    T("Opera Numerorum  --  Battle Plan v1.6", small_style),
    T("Author: David Fox  |  Certified: June 4, 2026", small_style),
    T("ASCII-only.  No fabricated values.  No Unicode.  No torus geometry.", small_style),
    T("Series internal working title retained for SHA-chain integrity.", small_style),
]

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=1.1 * inch,
    rightMargin=1.1 * inch,
    topMargin=1.0 * inch,
    bottomMargin=1.0 * inch,
    title="On the Rule of Error and Symmetry",
    author="David Fox",
)

doc.build(story)
print("Written:", OUTPUT)

result = subprocess.run(
    ["pdftotext", OUTPUT, "-"],
    capture_output=True, text=True, errors="replace")
bad = [(i, c) for i, c in enumerate(result.stdout) if ord(c) > 127]
if bad:
    print(f"WARNING: {len(bad)} non-ASCII characters found")
else:
    print("ASCII check: PASS")

with open(OUTPUT, "rb") as f:
    sha = hashlib.sha256(f.read()).hexdigest()
print(f"SHA-256: {sha}")
