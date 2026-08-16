"""
Stage 1 — Workflow: deterministic, auditable, boring on purpose.

Task: produce a weekly financial summary doc.
The steps and their ORDER are fixed. No model decides what happens next —
at most, a model fills in the content of one step. This is the right choice
whenever the process itself needs to be provably the same every time
(compliance, finance, anything that gets audited).
"""

from _mock_model import call_model


def query_warehouse() -> dict:
    # step 1: always runs first, always the same query shape
    print("[step 1/3] querying warehouse for this week's order volume + GMV...")
    return {"orders": 482_910, "gmv_usd": 6_120_442, "week_ending": "2026-08-15"}


def summarize(data: dict) -> str:
    # step 2: always runs second. the MODEL fills in content, but the
    # workflow — not the model — decided that summarization happens here.
    print("[step 2/3] summarizing query results...")
    prompt = f"Summarize this week's data for a finance doc: {data}"
    return call_model(prompt)


def write_doc(summary: str) -> str:
    # step 3: always runs third, always writes to the same destination shape
    print("[step 3/3] writing summary to doc...")
    doc = f"# Weekly Financial Summary\n\n{summary}\n"
    return doc


def run() -> str:
    print("=== WORKFLOW: Snowflake query -> summarize -> write doc ===")
    data = query_warehouse()
    summary = summarize(data)
    doc = write_doc(summary)
    print("Done. The sequence above is fixed — rerun this 100 times, you get")
    print("the same 3 steps in the same order every time. That's the feature.")
    return doc


if __name__ == "__main__":
    run()
