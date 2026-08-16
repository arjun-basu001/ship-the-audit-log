# The Maturity Ladder: Workflows → Agents → Deep Agents → Swarms

DoorDash frames its own systems on a four-stage ladder. The point of the ladder isn't that swarms are "advanced" and workflows are "basic." It's that each stage trades predictability for flexibility, and you should climb only as far as the task actually requires. Most tasks require less than people want to admit.

## Stage 1 — Workflows: deterministic, auditable, boring on purpose

A fixed pipeline. Step A always runs, then step B, then step C. No model decides the *order* of operations — at most, a model fills in one step (e.g., "summarize this").

Use this when the process is high-stakes, repeatable, and needs to be the same every time: financial reports, compliance checks, anything that gets audited. The value isn't intelligence, it's that step 4 always follows step 3, and you can prove that to someone in a review.

`examples/01_maturity_ladder/workflow.py` shows this: `Snowflake query → summarize → write doc`, hardcoded in that order.

## Stage 2 — Agents: dynamic reasoning over a fixed toolset

A single LLM-driven loop decides *which* tool to call and *when*, based on what it's seen so far (the classic think → act → observe loop). The task is still bounded — one agent, one goal — but the *path* to the goal isn't fixed in advance.

Use this when the right sequence of steps genuinely depends on what you find along the way — exploratory data queries, for instance, where the right follow-up query depends on the first result.

`examples/01_maturity_ladder/single_agent.py` shows a toy version: the agent decides whether it needs a schema lookup before it can write a query, instead of always doing both.

## Stage 3 — Deep Agents: hierarchical decomposition

One "manager" breaks a large task into subtasks and hands them to specialist sub-agents, tracks their progress, and reconciles results — sometimes over hours or days, with a shared workspace so one agent's output is available to another later.

Use this for genuinely long-horizon, multi-part work: a migration, a multi-file refactor, an investigation with several independent threads. The cost is real — more moving parts, more places for errors to compound — so this stage only pays off when the task actually decomposes cleanly.

`examples/01_maturity_ladder/deep_agent.py` shows a minimal manager/specialist split with a shared in-memory "workspace" dict standing in for persistent shared state.

## Stage 4 — Swarms: distributed peer collaboration, no central manager

Multiple agents coordinate through shared state, not a hierarchy. Nobody's "in charge" — control is distributed, closer to how an ant colony finds food than how an org chart runs a project.

Use this rarely, and only where real-time, decentralized coordination is the actual requirement (large-scale logistics is DoorDash's own example). It's the hardest stage to debug, because there's no single decision path to trace — expect to invest heavily in provenance and logging just to understand what happened after the fact.

`examples/01_maturity_ladder/swarm_sketch.py` is deliberately labeled a *sketch*, not a working swarm — building a real one is out of scope for a teaching repo, and pretending otherwise would be the exact kind of overclaiming this repo argues against.

## The actual rule

> Build robust single-agent primitives — reliable schema lookups, reliable retrieval, reliable tool calls — before you attempt multi-agent orchestration. Multi-agent systems don't fix a shaky primitive. They amplify it, faster, and with a worse stack trace.

If you can't get a single agent to reliably call one tool correctly, a swarm of them will not solve that problem. It will hide it in more places.
