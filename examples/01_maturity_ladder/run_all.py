"""
Runs the same underlying idea — "produce insight from data" — at all four
maturity stages back to back, so the difference in shape is visible in one
run instead of across four separate reads.

Usage: python3 examples/01_maturity_ladder/run_all.py
"""

import workflow
import single_agent
import deep_agent
import swarm_sketch

if __name__ == "__main__":
    workflow.run()
    print()
    single_agent.agent_loop("How many orders came through last week?")
    print()
    deep_agent.manager("why did refunds spike this week")
    print()
    swarm_sketch.sketch_one_tick()
