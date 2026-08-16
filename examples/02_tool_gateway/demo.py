"""
Two agents, one gateway. One agent stays in its lane. One tries to reach
outside it — deliberately, to show what the gateway does when that happens.

Usage: python3 examples/02_tool_gateway/demo.py
"""

from gateway import AgentGateway


def post_pr_comment(pr_id: str, body: str) -> str:
    return f"comment posted on PR {pr_id}: '{body}'"


def read_repo(path: str) -> str:
    return f"contents of {path}: [...]"


def run_database_migration(sql: str) -> str:
    return f"MIGRATION EXECUTED: {sql}"  # exactly the kind of action a review agent should never reach


def main():
    gw = AgentGateway()
    gw.register_tool("post_pr_comment", post_pr_comment)
    gw.register_tool("read_repo", read_repo)
    gw.register_tool("run_database_migration", run_database_migration)

    # scoped tightly to what a code-review agent actually needs
    gw.register_agent("code-reviewer", allowed_tools={"read_repo", "post_pr_comment"})

    print("--- Agent 'code-reviewer' does its job, within scope ---")
    gw.call("code-reviewer", "read_repo", path="services/checkout/handler.go")
    gw.call("code-reviewer", "post_pr_comment", pr_id="4821", body="Deletion here changes error handling — see line 92.")

    print("\n--- Agent 'code-reviewer' tries to reach beyond its scope ---")
    print("(this simulates a prompt-injected or just plain buggy agent trying")
    print(" to 'helpfully' run a migration it found referenced in a PR)")
    try:
        gw.call("code-reviewer", "run_database_migration", sql="ALTER TABLE orders DROP COLUMN legacy_id;")
    except PermissionError as e:
        print(f"Blocked, as intended: {e}")

    gw.print_audit_log()

    print("\nThe scary version of this demo is the one where 'code-reviewer'")
    print("was just handed a database credential directly instead of going")
    print("through a gateway. In that version, this script has no story to")
    print("tell, because there's no audit log — the migration just runs.")


if __name__ == "__main__":
    main()
