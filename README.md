# trinity-dialectic

A single-file dialectical evaluation engine that forces three independent reasoning lenses before any LLM output is finalized.

## Status

Experimental. Maintained by Sage / 0SxD as part of an ongoing research portfolio focused on prompt engineering, agent skills, and LLM evaluation.

## What this is

`trinity.py` is a reference implementation of the Trinity Dialectic: a structured self-evaluation protocol built into the 143_protocol_a operating contract for multi-agent AI systems. It addresses premature commitment in LLM agents by requiring every proposed output to pass three independent gates - Logos (logical rigor), Pathos (creative alignment), and Ethos (practical executability) - before finalization. The fight between Logos and Pathos, arbitrated by Ethos, is the productive mechanism. This is not a pipeline; it is a dialectic grounded in Aristotle's Nicomachean Ethics and phronesis (practical wisdom).

## Approach

- Three evaluation gates fire in sequence; a score below threshold triggers a LOOP_BACK_REVIEW_REPLAN_RETURN cycle rather than suppressing the output
- Trinity of Trinities: each gate applies its own internal three-axis evaluation, yielding a 3x3 grid with a maximum of 15 evaluation tokens
- No external dependencies beyond the Python standard library
- Designed for agentic systems where outputs become inputs to downstream agents and output drift compounds over long task horizons
- Source rooted in `trinity.py`; examples in `examples/`

## Layout

- `trinity.py` - the full dialectical engine (TrinityEngine, DefaultDialecticGate, TrinityOfTrinities)
- `examples/basic_eval.py` - architecture decision walkthrough through all three gates
- `examples/socratic_gate.py` - Socratic variant: surface the better question before answering the stated one
- `_visuals/` - evaluation flow diagram (PNG; EXIF stripped)

## Usage / How to read this

No install required beyond Python 3.x:

```python
from trinity import TrinityEngine, DefaultDialecticGate, ThreatLevel

engine = TrinityEngine(gate=DefaultDialecticGate())
context = {
    "logos_claim": "Use the proven solution.",
    "logos_reasoning": "Three independent benchmarks confirm this approach.",
    "logos_evidence": ["benchmark A", "benchmark B", "benchmark C"],
    "logos_confidence": 0.82,
    "pathos_claim": "The disruptive approach yields 3x gains if it works.",
    "pathos_reasoning": "No one has tried combining these two methods before.",
    "pathos_evidence": ["theoretical basis from paper X"],
    "pathos_confidence": 0.60,
    "threat_level": ThreatLevel.NONE,
    "violations": [],
}
result = engine.run_dialectic(context)
print(result.phase.name)          # VERIFIED
print(result.final_verdict.name)  # LOGOS_WINS
print(result.final_position)      # "Use the proven solution."
```

Start with `examples/basic_eval.py` for a full walkthrough. See also `143-protocol` (link below) for the full operating contract this engine is part of.

## Prior art and citations

- GEPA: Reflective Prompt Evolution, arXiv:2507.19457 - reflective self-evaluation loop that motivates the LOOP_BACK_REVIEW_REPLAN_RETURN cycle
- AGENTS.md spec (Linux Foundation Agentic AI Foundation) - behavioral contract model
- Aristotle, Nicomachean Ethics Books I-II, VI - foundational source for Ethos/Logos/Pathos framing and phronesis; cited verbatim in `trinity.py` module docstring

See also: [143-protocol](https://github.com/0SxD/143-protocol) for the full operating contract.

## License

MIT. Copyright (c) 2026 Sage / 0SxD.

## Notes

This repo is part of an active R&D portfolio. Content may move, change, or be withdrawn. Issues and PRs welcome but reviews are best-effort.
