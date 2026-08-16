"""
A toy "code reviewer" that generates candidate findings on a diff, then
runs each one through a disprove-it pass before deciding whether it's
worth surfacing to a human. The model calls are stubbed (see the comment
on CANDIDATE_FINDINGS) — the point is the CONTROL FLOW around the model,
which is what actually drives precision up in DoorDash's real system.
"""

from dataclasses import dataclass


@dataclass
class Finding:
    file: str
    line: int
    claim: str
    is_actually_true: bool  # ground truth, for this toy example only —
    # a real system doesn't know this in advance, that's the whole problem


# Stand-in for "Lead Scout notices suspicious patterns" — in production this
# is an LLM call over a real diff. Here it's a fixed set so the eval harness
# has something stable to measure against.
CANDIDATE_FINDINGS = [
    Finding("checkout/handler.go", 92, "Removed nil check changes error handling on empty cart", True),
    Finding("checkout/handler.go", 140, "Renamed variable 'total' may break downstream logging", False),
    Finding("payments/adapter.go", 58, "New enum value 'PARTIAL_REFUND' unhandled in adjacent switch statement", True),
    Finding("payments/adapter.go", 12, "Import order changed", False),
    Finding("notifications/sender.go", 77, "Silent catch swallows retry failure, no log emitted", True),
    Finding("notifications/sender.go", 20, "Comment updated, no behavior change claimed incorrectly as a fix", False),
]


def disprove_it_pass(finding: Finding) -> tuple[bool, str]:
    """
    Attempts to falsify the finding before it's allowed to surface.
    Real version: re-reads the diff, traces callers, checks for existing
    handling elsewhere. Toy version: uses the finding's own ground-truth
    flag as a stand-in for "a careful re-check would find this holds up" —
    the mechanism being demonstrated is the GATE, not the falsification
    logic itself, which is exactly the part you'd replace with a real
    model call.
    """
    if finding.is_actually_true:
        return True, "survived disprove-it pass: re-check found the claim holds"
    return False, "disprove-it pass falsified the claim: no behavior change found on closer read"


def review(findings: list[Finding], use_disprove_gate: bool) -> list[Finding]:
    surfaced = []
    for f in findings:
        if not use_disprove_gate:
            surfaced.append(f)
            continue
        survives, reason = disprove_it_pass(f)
        tag = "SURFACE" if survives else "SUPPRESS"
        print(f"  [{tag}] {f.file}:{f.line} — {f.claim}\n           -> {reason}")
        if survives:
            surfaced.append(f)
    return surfaced


if __name__ == "__main__":
    print("=== Reviewing WITHOUT the disprove-it gate (surface everything) ===")
    without_gate = review(CANDIDATE_FINDINGS, use_disprove_gate=False)
    print(f"Surfaced {len(without_gate)}/{len(CANDIDATE_FINDINGS)} findings, no filtering applied.\n")

    print("=== Reviewing WITH the disprove-it gate ===")
    with_gate = review(CANDIDATE_FINDINGS, use_disprove_gate=True)
    print(f"\nSurfaced {len(with_gate)}/{len(CANDIDATE_FINDINGS)} findings after the gate.")
