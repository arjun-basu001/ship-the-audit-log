"""
Replays reviewer.py's candidate findings against known ground truth and
reports precision — the same shape of eval DoorDash describes running
against a corpus of real past incidents, small enough here to read in
one sitting.

Run this with and without the gate (see main()) and compare precision.
That comparison is the entire argument of docs/03-precision-over-recall-evals.md,
made numerically instead of rhetorically.

Usage: python3 examples/03_disprove_it_eval/eval_harness.py
"""

from reviewer import CANDIDATE_FINDINGS, review


def precision(surfaced: list) -> float:
    if not surfaced:
        return float("nan")
    true_positives = sum(1 for f in surfaced if f.is_actually_true)
    return true_positives / len(surfaced)


def recall(surfaced: list, all_findings: list) -> float:
    total_true = sum(1 for f in all_findings if f.is_actually_true)
    if total_true == 0:
        return float("nan")
    true_positives = sum(1 for f in surfaced if f.is_actually_true)
    return true_positives / total_true


def report(label: str, surfaced: list, all_findings: list) -> None:
    p = precision(surfaced)
    r = recall(surfaced, all_findings)
    print(f"\n{label}")
    print(f"  surfaced:  {len(surfaced)}/{len(all_findings)}")
    print(f"  precision: {p:.0%}  (of what it surfaced, how much was real —")
    print("               this is the number that determines whether engineers")
    print("               keep reading its output, or learn to ignore it)")
    print(f"  recall:    {r:.0%}  (of what was real, how much it caught)")


def main():
    print("Running the same candidate findings through the reviewer twice:")
    print("once with no quality gate, once with the disprove-it gate.\n")

    print("--- No gate ---")
    no_gate = review(CANDIDATE_FINDINGS, use_disprove_gate=False)
    report("RESULT: no gate", no_gate, CANDIDATE_FINDINGS)

    print("\n--- Disprove-it gate ---")
    with_gate = review(CANDIDATE_FINDINGS, use_disprove_gate=True)
    report("RESULT: disprove-it gate", with_gate, CANDIDATE_FINDINGS)

    print("\n--- Why this matters ---")
    print("In this toy set, recall doesn't move — the gate isn't making the")
    print("system miss real issues, it's filtering out plausible-sounding")
    print("findings that don't survive a second look. Precision jumps from")
    print("50% to 100%. In a real system the gate will occasionally cost you")
    print("some recall too, and that's still usually the right trade: a")
    print("reviewer at 100% recall / 50% precision gets ignored within a week.")
    print("One at 80% recall / 90% precision gets read. DoorDash chose the")
    print("second tradeoff on purpose — a harness like this is how you prove")
    print("it was the right call instead of just asserting it.")


if __name__ == "__main__":
    main()
