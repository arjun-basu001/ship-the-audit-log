"""
Stage 3 — Deep Agent: hierarchical decomposition.

Task: investigate "why did refunds spike this week" — too broad for one
agent to just answer, so a manager breaks it into subtasks, hands them to
specialists, and reconciles the results. A shared "workspace" stands in for
the persistent shared memory DoorDash describes — artifacts one agent
produces are visible to the others, including ones that run later.
"""

from _mock_model import call_model

workspace: dict[str, str] = {}  # stand-in for a persistent shared memory layer


def specialist_data(subtask: str) -> None:
    print(f"  [specialist: data] investigating '{subtask}'")
    workspace["data_findings"] = call_model(
        f"Pull the numbers relevant to: {subtask}",
        options=[
            "Refund rate up 2.3x in the Midwest region specifically.",
            "Refund rate roughly flat nationally.",
        ],
    )
    print(f"  [specialist: data] wrote to workspace: {workspace['data_findings']}")


def specialist_ops(subtask: str) -> None:
    print(f"  [specialist: ops] investigating '{subtask}', reading workspace so far")
    prior = workspace.get("data_findings", "no prior findings")
    workspace["ops_findings"] = call_model(
        f"Given {prior}, check for an operational cause of: {subtask}",
        options=[
            "A regional dasher shortage caused late deliveries -> refunds.",
            "No operational anomaly found.",
        ],
    )
    print(f"  [specialist: ops] wrote to workspace: {workspace['ops_findings']}")


def reflection_agent() -> str:
    print("  [reflection] checking whether findings actually explain the spike")
    verdict = call_model(
        f"Do these findings sufficiently explain the spike? {workspace}",
        options=["Yes, sufficient.", "No, needs another pass."],
    )
    print(f"  [reflection] verdict: {verdict}")
    return verdict


def manager(goal: str) -> str:
    print(f"=== DEEP AGENT: manager decomposing '{goal}' ===")
    subtasks = ["find where the spike is concentrated", "find what caused it there"]
    print(f"[manager] decomposed into subtasks: {subtasks}")

    specialist_data(subtasks[0])
    specialist_ops(subtasks[1])
    verdict = reflection_agent()

    if verdict.startswith("No"):
        print("[manager] reflection agent flagged this as insufficient — in a")
        print("          real system, the manager would re-dispatch here.")

    report = call_model(f"Write final report from: {workspace}")
    print(f"\n[manager] final report (drawing on both specialists' workspace entries):\n{report}")
    return report


if __name__ == "__main__":
    manager("why did refunds spike this week")
