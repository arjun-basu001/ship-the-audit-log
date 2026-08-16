"""
Stage 2 — Agent: dynamic reasoning over a fixed toolset.

Task: answer an ad-hoc data question. Unlike the workflow, the RIGHT
SEQUENCE of steps isn't known up front — it depends on what the agent
finds. A think -> act -> observe loop decides, each turn, whether it
has enough information to answer or needs to call another tool.
"""

from _mock_model import call_model

TOOLS = {
    "list_tables": lambda: ["orders", "deliveries", "refunds"],
    "describe_table": lambda t: {
        "orders": ["order_id", "gmv_usd", "created_at", "region"],
        "deliveries": ["order_id", "dasher_id", "delivered_at"],
        "refunds": ["order_id", "amount_usd", "reason"],
    }.get(t, []),
    "run_query": lambda q: {"rows": 482_910, "query": q},
}


def agent_loop(question: str, max_steps: int = 5) -> str:
    print(f"=== AGENT: '{question}' ===")
    observations = []

    for step in range(1, max_steps + 1):
        # the agent decides WHICH tool to call next based on what it's seen —
        # this is the part a fixed workflow can't do, because the workflow
        # author would have to anticipate every possible path in advance
        known_tables = any("tables:" in o for o in observations)
        has_schema = any("schema:" in o for o in observations)

        if not known_tables:
            action = "list_tables"
        elif not has_schema:
            action = "describe_table"
        else:
            action = "run_query"

        print(f"[step {step}] think: need '{action}' next")

        if action == "list_tables":
            result = TOOLS["list_tables"]()
            observations.append(f"tables: {result}")
        elif action == "describe_table":
            result = TOOLS["describe_table"]("orders")
            observations.append(f"schema: {result}")
        else:
            query = call_model(f"Write SQL for: {question}. Schema known: {observations[-1]}")
            result = TOOLS["run_query"](query)
            observations.append(f"result: {result}")
            print(f"[step {step}] observe: {result} -> enough to answer, stopping")
            break

        print(f"[step {step}] observe: {result}")

    answer = call_model(f"Answer '{question}' given: {observations}")
    print(f"\nFinal answer (model-generated from gathered context): {answer}")
    return answer


if __name__ == "__main__":
    agent_loop("How many orders came through last week?")
