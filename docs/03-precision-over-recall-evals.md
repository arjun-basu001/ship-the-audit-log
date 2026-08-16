# Precision Over Recall: The "Disprove-It Pass"

"Volume without unit-cost and quality gates is a vanity trap." That's DoorDash's own language describing their agent platform, and it's the single most useful sentence in this whole repo. It's worth sitting with, because it cuts against almost every "look how many tasks our agent completed" metric currently getting posted on LinkedIn.

Throughput is easy to demo and easy to fake — an agent that flags 40 issues per PR looks impressive for about a week, until engineers learn to ignore all 40 because 35 of them aren't real. At that point the agent has a 0% effective acceptance rate no matter how many things it technically caught. Volume without a quality gate isn't progress. It's noise with better production values.

## The pattern: split noticing from verifying

DoorDash's code reviewer went through three iterations before this clicked:

- **V1**: specialist agents (security, tests, performance) working independently. Good at mechanical bugs, blind to anything crossing a specialty's boundary.
- **V2**: two generalist reviewers reading the whole diff. Better at cross-cutting issues, but attention spread thin — everything got a shallow pass, nothing got a deep one.
- **V3 (shipped)**: a **Lead Scout** that's allowed to notice suspicious patterns without proving them — a deletion that looks like it changes behavior, an enum handled in three places but updated in two, an error silently swallowed. Then **Deep Reviewers** investigate only the scout's leads, in depth. Then, only for findings that survive review, a **Fixer** agent proposes the change.

In their words: *"Splitting noticing from verifying let us go deeper on the things that matter without spreading attention thin across the things that don't."*

## The gate: disprove it before you post it

Before a finding reaches a human, the system runs a "disprove-it pass" — it actively tries to falsify its own claim. Is this actually a behavior change, or does a caller already handle the null case elsewhere? Is this enum actually referenced anywhere the new value matters? If the system can talk itself out of the finding, it doesn't post it.

This one design choice is why DoorDash's acceptance rate on high/critical findings sits at 60.2%, up from 46% with the commercial tool they replaced. The bar isn't "could this maybe be a problem." It's "did this survive an attempt to prove it isn't one."

## Why this generalizes past code review

Any agent whose job is to *flag* something — a compliance check, a fraud signal, a data-quality alert, a support-ticket triage — has the same failure mode: it's cheap to generate candidates and expensive to be wrong about them, and the cost of being wrong isn't paid by the agent, it's paid by the human who now distrusts everything it says. Precision over recall, enforced by an explicit falsification step, is the fix in every one of those cases, not just this one.

## Where this shows up in the repo

`examples/03_disprove_it_eval/reviewer.py` generates candidate findings on a toy diff, then runs each one through a disprove-it check before deciding whether to surface it. `examples/03_disprove_it_eval/eval_harness.py` replays a small fixture set of known true/false findings and reports precision — the same shape of eval DoorDash describes running against a corpus of real past incidents, just small enough to read in one sitting.

Run the harness with the disprove-it gate on and off. The precision difference is the entire argument of this document, made numerically instead of rhetorically.
