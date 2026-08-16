"""
Stage 4 — Swarm: distributed peer collaboration, no central manager.

This file is deliberately a SKETCH, not a working swarm. A real swarm needs
real distributed infrastructure (message buses, consensus, failure handling
across machines) that doesn't belong in a single-file teaching example —
and faking that here would be exactly the kind of overclaiming this repo
argues against. Read this for the *shape* of the idea, not as something to
run in production.

Task (sketched): a fleet of delivery-routing peers coordinating in real time,
each reacting to local conditions, with no single agent deciding the global
plan. DoorDash's own comparison is apt: closer to an ant colony finding food
than an org chart running a project.
"""

from dataclasses import dataclass, field


@dataclass
class Peer:
    name: str
    local_state: dict = field(default_factory=dict)

    def observe(self, shared_board: dict) -> None:
        # a peer reads shared state — not a manager's instructions — to decide
        # its next move. no peer has a global view; each acts on what it sees.
        nearby_load = shared_board.get(self.name, 0)
        self.local_state["load"] = nearby_load

    def act(self, shared_board: dict) -> None:
        # peers coordinate by WRITING to shared state, which other peers will
        # read on their next turn. this is the "decentralized protocol" part —
        # there's no message to a manager, only a change other peers can see.
        if self.local_state.get("load", 0) > 5:
            shared_board[self.name] = max(0, shared_board.get(self.name, 0) - 1)
            print(f"  [{self.name}] load high, shed one unit of work to shared board")
        else:
            print(f"  [{self.name}] load manageable, no action")


def sketch_one_tick() -> None:
    print("=== SWARM (sketch only — not a runnable production pattern) ===")
    shared_board = {"peer-a": 8, "peer-b": 2, "peer-c": 6}
    peers = [Peer(name) for name in shared_board]

    for p in peers:
        p.observe(shared_board)
    for p in peers:
        p.act(shared_board)

    print(f"\nShared board after one tick: {shared_board}")
    print("Notice: no peer above ever called another peer directly, and no")
    print("central process decided who does what. That property is also why")
    print("swarms are the hardest stage to debug after the fact — there's no")
    print("single decision path to trace, only a sequence of shared-state edits.")
    print("This is why DoorDash treats provenance/logging as non-negotiable")
    print("infrastructure BEFORE reaching for this stage, not after.")


if __name__ == "__main__":
    sketch_one_tick()
