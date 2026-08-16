# Ng's Four Pillars, Mapped to a System That Already Shipped

Andrew Ng's "AI Engineering Skills Map" (built from 10,000+ job postings, expert interviews, and industry survey data) names four pillars as the essential competencies for 2026. Read cold, they sound like reasonable abstractions. Read next to DoorDash's public engineering writeups, they read like a description of a system that already exists — which is usually the sign a framework is right: it's describing something real, not inventing something aspirational.

## 1. Building and deploying AI applications

Ng's framing: mastery of LLMs, context engineering, RAG, and agentic workflows, paired with real evaluation practice and error-analysis loops — because AI systems, unlike traditional software, produce variable output, and "it worked when I tried it" isn't a deployment strategy.

DoorDash's version: an eval corpus built from real past incidents and known review misses, replayed every time a prompt, retrieval strategy, or model choice changes. Not a one-time benchmark — a continuously growing regression suite for a system whose failure mode is "confidently wrong," not "crashes."

## 2. Software engineering fundamentals

Ng's framing: understanding tradeoffs — cost, scalability, reliability, speed, security, privacy — well enough to give a coding agent real constraints instead of vibes.

DoorDash's version: the Agent Gateway (see `docs/02-trust-boundary-pattern.md`). Scoped access, audit logging, and fail-closed defaults, decided as an architecture choice before the agent shipped — not bolted on after an incident made it necessary. This is the pillar least visible in agent demos and most responsible for whether a system survives contact with production.

## 3. Using coding agents

Ng's framing: context management, balancing planning against execution, closing the loop with verification, and knowing when to intervene versus when to let the agent run.

DoorDash's version: the Lead Scout / Deep Reviewer / Fixer split (see `docs/03-precision-over-recall-evals.md`). The Fixer — the one agent actually allowed to touch code — only acts after a finding survives scouting, deep review, *and* a disprove-it pass. That's "knowing when to intervene" as a concrete architecture decision, not a vague best practice.

## 4. Shaping the build

Ng's framing: engineers increasingly decide the spec, not just implement it — product intuition, business judgment, knowing when to prototype fast versus build deliberately.

DoorDash's version: "volume without unit-cost and quality gates is a vanity trap" is, underneath the engineering language, a product decision. Someone chose to optimize for acceptance rate and cost-per-review instead of tasks-completed, and that choice shaped every technical decision downstream of it. The architecture didn't produce that judgment. The judgment produced the architecture.

## The actual takeaway

None of DoorDash's four moves required a better model. Same LLMs everyone else has access to. The difference is entirely in the three unglamorous layers Ng's map insists on: the software engineering fundamentals underneath the agent, the evaluation discipline around it, and the product judgment about what "good" even means before anyone wrote a line of orchestration code.

If your team is spending its energy on making the agent more autonomous and none of it on these three things, you don't have a worse model problem. You have a missing-pillars problem.
