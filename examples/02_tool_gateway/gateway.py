"""
A minimal version of the Agent Gateway pattern: agents never hold raw
credentials or call tools directly. Every call goes through this gateway,
which checks scope, logs the attempt (allowed or not), and fails closed.

This is deliberately small enough to read top to bottom. A real gateway adds
auth, rate limiting, and probably a network hop — the SHAPE below is the
part worth understanding first.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuditEntry:
    timestamp: str
    agent: str
    tool: str
    args: dict
    allowed: bool
    reason: str

    def __str__(self) -> str:
        status = "ALLOWED" if self.allowed else "BLOCKED"
        return f"[{self.timestamp}] {status} agent={self.agent} tool={self.tool} args={self.args} reason={self.reason}"


class AgentGateway:
    """
    Agents are registered with a scope: the exact set of tools they're
    allowed to call. Nothing else. No agent gets a credential directly —
    they get a name, and the gateway decides what that name can do.
    """

    def __init__(self):
        self._scopes: dict[str, set[str]] = {}
        self._tools: dict[str, callable] = {}
        self.audit_log: list[AuditEntry] = []

    def register_agent(self, agent_name: str, allowed_tools: set[str]) -> None:
        self._scopes[agent_name] = allowed_tools

    def register_tool(self, tool_name: str, fn: callable) -> None:
        self._tools[tool_name] = fn

    def call(self, agent_name: str, tool_name: str, **kwargs):
        """
        The one and only path from an agent to a tool. This is the trust
        boundary: everything an agent can affect in the real world passes
        through this one function, which is why it's the one function you
        actually need to get right.
        """
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        allowed_tools = self._scopes.get(agent_name, set())

        if tool_name not in allowed_tools:
            # FAIL CLOSED: unknown or out-of-scope requests are rejected,
            # not silently allowed, not allowed-with-a-warning.
            entry = AuditEntry(
                now, agent_name, tool_name, kwargs, False,
                f"'{agent_name}' is not scoped for '{tool_name}' (scope: {sorted(allowed_tools)})",
            )
            self.audit_log.append(entry)
            print(entry)
            raise PermissionError(entry.reason)

        if tool_name not in self._tools:
            entry = AuditEntry(now, agent_name, tool_name, kwargs, False, "tool not registered on gateway")
            self.audit_log.append(entry)
            print(entry)
            raise LookupError(entry.reason)

        entry = AuditEntry(now, agent_name, tool_name, kwargs, True, "within scope")
        self.audit_log.append(entry)
        print(entry)
        return self._tools[tool_name](**kwargs)

    def print_audit_log(self) -> None:
        print("\n--- FULL AUDIT LOG (this is the artifact that matters) ---")
        for entry in self.audit_log:
            print(entry)
