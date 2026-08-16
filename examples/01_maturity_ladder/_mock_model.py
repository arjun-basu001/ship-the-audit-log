"""
A stand-in for a real model call, shared by every script in this folder.

Swap `call_model()` for a real SDK call (OpenAI, Anthropic, whatever you run)
and everything else in this folder works unchanged — that's the point of the
pattern. The architecture around the model doesn't care which model it is.
"""

import random


def call_model(prompt: str, options: list[str] | None = None) -> str:
    """
    # swap for a real model call, e.g.:
    # return anthropic_client.messages.create(...).content[0].text

    Here, it just does something plausible-but-deterministic-enough for a
    demo: if given options, picks one with a slight bias toward the first;
    otherwise returns a canned "summary" of the prompt.
    """
    if options:
        weights = [3] + [1] * (len(options) - 1)
        return random.choices(options, weights=weights, k=1)[0]
    return f"[summary of {len(prompt)} chars of input, produced by a real model in prod]"
