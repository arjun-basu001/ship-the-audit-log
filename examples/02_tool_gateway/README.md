# Example: The Trust Boundary / Agent Gateway

Companion code for [`docs/02-trust-boundary-pattern.md`](../../docs/02-trust-boundary-pattern.md).

```bash
python3 demo.py
```

`gateway.py` is the pattern: agents are registered with a scope (the exact tools they're allowed to call), every call is logged whether allowed or blocked, and anything outside scope fails closed rather than failing open.

`demo.py` runs a `code-reviewer` agent doing its actual job (read a repo, post a PR comment) and then, deliberately, trying to run a database migration it has no business touching — to show what the gateway does when an agent reaches past its scope, whether from a bug, a bad prompt, or an injected instruction in something it read. Read the printed audit log at the end; that log, not the model's output, is the actual safety artifact.
