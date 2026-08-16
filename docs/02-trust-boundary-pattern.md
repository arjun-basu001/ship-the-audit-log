# The Trust Boundary Pattern

An agent with unscoped access to your systems isn't an employee. It's an intern with root, no manager, and a to-do list it wrote itself. Nobody would hand a new hire that on day one — full prod credentials, no audit trail, "figure it out." Somehow it's the default setup for a lot of "autonomous" agent demos, because in a demo, nothing the agent touches actually matters.

In production, it matters. DoorDash's answer was an **Agent Gateway**: a control plane the agent talks to instead of talking to your systems directly.

## What the gateway actually does

1. **Scopes access per agent, per task.** A code-review agent gets read access to a repo and write access to PR comments. It does not get a database credential just because a database credential exists somewhere in the environment.
2. **Routes every tool call through one auditable choke point.** DoorDash's version sits in front of 200+ MCP servers — the agent doesn't hold credentials for any of them directly.
3. **Logs every call with provenance.** Not "the agent did something," but *which* agent, *which* tool, *which* arguments, *what* it got back. When something goes wrong, you can trace it. Without this, "why did the agent do that" is a question you can't actually answer, just speculate about.
4. **Fails closed.** A tool call outside an agent's scope is rejected and logged — not silently ignored, not allowed with a warning. Rejected, and someone can see that it was attempted.

## Why this isn't optional once an agent has real autonomy

The moment an agent's action isn't reviewed by a human before it executes — a Fixer agent pushing a code change, a report-writer emailing a doc, a swarm coordinating logistics — the gateway *is* your safety system. There is no other one. "The model is well-behaved" is not a control. It's a hope.

This is also, not coincidentally, a software engineering fundamentals problem before it's an AI problem: least privilege, audit logging, and fail-closed defaults are the same three things you'd want on any service account, agent or not. The novelty of "AI agent" doesn't exempt it from access control. If anything it raises the stakes, because the thing making the request can be talked into requesting something it shouldn't via a bad prompt or a poisoned document, in a way a human service account can't be.

## Where this shows up in the repo

`examples/02_tool_gateway/gateway.py` implements a minimal version: scopes, an audit log, and a fail-closed check. `examples/02_tool_gateway/demo.py` runs two agents against it — one requesting a tool inside its scope (allowed, logged) and one requesting a tool outside its scope (blocked, logged, and you can see exactly why).

Run it and read the audit log it prints. That log is the entire point. An agent you can't audit after the fact isn't an agent you can trust before the fact, no matter how good its outputs looked in testing.
