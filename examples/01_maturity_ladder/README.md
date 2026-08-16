# Example: The Maturity Ladder

Same underlying goal — "turn data into an answer" — implemented four ways, one per rung of the ladder described in [`docs/01-maturity-ladder.md`](../../docs/01-maturity-ladder.md).

Run them individually or together:

```bash
python3 workflow.py        # Stage 1
python3 single_agent.py    # Stage 2
python3 deep_agent.py      # Stage 3
python3 swarm_sketch.py    # Stage 4 (sketch only — see the file's docstring)
python3 run_all.py         # all four, back to back
```

What to notice reading the output: the workflow's steps never change order no matter what the data looks like. The single agent's *decisions* change based on what it observes, but there's still one agent, one goal. The deep agent adds a second layer — specialists writing to a shared workspace a manager reads from. The swarm sketch has no manager at all, only peers reacting to shared state. Each stage costs more to build and debug than the one before it — the ladder is there to stop you from paying that cost before the task actually needs it.
