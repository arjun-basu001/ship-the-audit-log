# Example: Precision Over Recall — the Disprove-It Gate

Companion code for [`docs/03-precision-over-recall-evals.md`](../../docs/03-precision-over-recall-evals.md).

```bash
python3 reviewer.py        # see the gate suppress false findings on a toy diff
python3 eval_harness.py    # measure precision/recall with the gate on vs. off
```

`reviewer.py` has a fixed set of candidate findings (some real, some plausible-but-wrong) and a `disprove_it_pass()` gate that decides whether each one survives to be surfaced. The model calls are stubbed — in production, both "generate candidate findings" and "attempt to falsify this one" are real model calls over a real diff — but the *control flow* here, generate first, then gate, then surface, is exactly DoorDash's Lead Scout → Deep Reviewer pattern in miniature.

`eval_harness.py` runs the same findings with the gate on and off and reports precision and recall for each. Run it once, then go change `CANDIDATE_FINDINGS` in `reviewer.py` to your own examples and rerun — that loop, look at the eval, adjust, rerun, is the "error analysis" Ng's skills map names as a core competency. It's boring in the way anything called "discipline" is boring. It's also the entire reason DoorDash's reviewer gets read instead of ignored.
