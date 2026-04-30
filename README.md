# Trinity Dialectic

**Logos and Pathos fight. Ethos arbitrates. The fight itself is the productive mechanism.**

One file (`trinity.py`). No dependencies beyond the standard library. A dialectical evaluation engine that interrupts LLM premature commitment by forcing three independent lenses before any output is finalized.

```python
from trinity import TrinityEngine
result = TrinityEngine().run_dialectic(context)
# VERIFIED, BLOCKED, or DEADLOCKED -- never just "done"
```

Part of the [0sXai](https://github.com/sagexresearch/0sXai) agent OS. See also: [143_protocol_a](https://github.com/sagexresearch/143-protocol).

**Files:**

| File | What it does |
|------|-------------|
| `trinity.py` | The full dialectical engine. TrinityEngine, DefaultDialecticGate, TrinityOfTrinities. |
| `examples/basic_eval.py` | Architecture decision going through all three gates. Readable in 5 minutes. |
| `examples/socratic_gate.py` | Socratic variant: should I answer the question asked, or surface the better one? |
| `_visuals/trinity_diagram.png` | Evaluation flow diagram. |

---

## A Three-Gate Evaluation Framework for AI Systems

The **Trinity Dialectic** is a structured evaluation framework built into the 143_protocol_a operating contract for multi-agent AI systems. It addresses a core failure mode in LLM-based agents: premature output commitment. When a language model generates text, it tends to converge on the first coherent path it finds. The Trinity Dialectic interrupts this tendency by requiring every output to pass three independent evaluation lenses before finalization.

*Source: 0sXai Protocol Specification (143_protocol_a), 2026-04-16. See also: [143_protocol_a](../143_protocol_a/README.md) for the full operating contract.*

---

## The Problem: Premature Commitment

Large language models are optimized for fluency and coherence. This optimization pressure causes them to:

- Converge on the shortest plausible path rather than the optimal path
- Suppress creative alternatives once a confident-sounding solution appears
- Skip constraint verification when the output reads well
- Treat self-consistency as a proxy for correctness

For single-turn question answering, premature commitment is tolerable. For agentic systems operating over long task horizons, where each output becomes input to downstream agents, it compounds into systematic failure. The Trinity Dialectic is a protocol-level countermeasure designed for that second context.

---

## The Three Gates

### [Λ] LOGOS  -  The Analytical Engine

*Shortest proven path. Logical consistency. Evidence quality.*

LOGOS operates as the formal verification layer. It applies deductive reasoning to test whether the proposed output is the most direct, logically sound path to the goal. It demands citations for every factual claim and rejects outputs that contain unsupported inferences.

**LOGOS asks:**
- Is this logically consistent?
- Is this the shortest proven path?
- Are all claims supported by accessible, verified sources?

**What LOGOS prevents:** Circular reasoning, hallucinated facts, unnecessarily complex solutions, and paths that feel right but cannot be verified against evidence.

---

### [Π] PATHOS  -  The Creative DMN

*Longest, hardest path. Hidden connections. Vision alignment.*

PATHOS operates as the divergent thinking layer, modeled on the brain's Default Mode Network (DMN)  -  the cognitive system active during mind-wandering, creative synthesis, and long-range association. It deliberately explores the solution space most likely to be ignored by a convergent model: the hard path, the unexpected connection, the option that requires more work but better serves the vision.

**PATHOS asks:**
- Does this align with the vision and purpose?
- What hidden connections exist that a linear path would miss?
- Is there a more disruptive or creative approach worth considering before committing?

**What PATHOS prevents:** Anchoring on the first adequate solution, missing cross-domain insights, and producing outputs that are technically correct but strategically misaligned.

---

### [Θ] ETHOS  -  The Golden Mean (Phronesis)

*Executable middle path. Constraint satisfaction. Practical wisdom.*

ETHOS is the arbitration gate. Named after Aristotle's concept of *phronesis* (practical wisdom), it does not simply average the LOGOS and PATHOS findings. It applies judgment to find the path that is both grounded (LOGOS-verified) and visionary (PATHOS-tested), while remaining practically executable under real constraints.

**ETHOS asks:**
- Is this ethically sound?
- Does it meet all stated constraints?
- Is it practically executable given current resources and scope?

**What ETHOS prevents:** Solutions that are theoretically optimal but operationally infeasible, ethical blind spots, and outputs that satisfy the letter but not the spirit of the request.

---

## Trinity of Trinities  -  Recursive Evaluation

The framework scales recursively. Each gate itself applies a three-dimensional evaluation:

| | External Logos | Optional Pathos | Internal Ethos |
|---|---|---|---|
| **Λ** | Logical Consistency | Creative Inference | Evidence Quality |
| **Π** | Possibility Desk | Vision / Purpose | Ethical Alignment |
| **Θ** | Justified Value | Practical Cohesion | Final Arbitration |

This produces a 3x3 evaluation grid yielding a maximum score of 15 tokens. A score below 15 triggers a LOOP_BACK_REVIEW_REPLAN_RETURN cycle rather than proceeding to output. The threshold creates a hard quality floor: an output must be simultaneously rigorous (Λ), aligned (Π), and executable (Θ) to ship.

---

## Visual Reference

![Trinity diagram](./trinity_diagram.png)

*Note: The Trinity diagram will be inserted here once the canonical evaluation flow visualization is finalized. The PNG placeholder is reserved for the promoted winner from the visual artifacts iteration. EXIF metadata must be stripped before insertion.*

---

## Relationship to Other Framework Components

The Trinity Dialectic does not operate in isolation. It is one gate within the full 143_protocol_a stack:

- **Before Trinity:** The 100% Confidence Gate (Module 02 in [143_protocol_a](../143_protocol_a/modules/02_confidence_loop.md)) ensures the agent has gathered all necessary information and reached certainty before attempting to produce output.
- **During Trinity:** The Three Gates evaluate the proposed output against rigor, vision, and practicality.
- **After Trinity:** The Quarantine Protocol holds any output below threshold for review rather than suppressing or discarding it. Failed outputs are retained for analysis.

The Dialectic is designed to run in under 300 tokens of self-evaluation for simple outputs, scaling to full recursive evaluation for high-stakes finalize steps.

---

## Why This Matters for Prompt Engineering

Most prompt engineering focuses on the *input side* of the agent loop: better system prompts, better few-shot examples, better tool descriptions. The Trinity Dialectic focuses on the *output side*: structured self-evaluation before the agent commits.

This distinction matters for:

- **Agentic systems** where outputs become inputs to downstream agents, and errors propagate
- **High-stakes decisions** where errors are costly or impossible to reverse
- **Long-horizon tasks** where small output drift compounds into large trajectory failures
- **Multi-agent orchestration** where each agent's output quality affects system-level coherence

The framework is not specific to any model family or API. It is a behavioral contract implemented through the system prompt and enforced through the agent's self-evaluation loop.

---

## Implementation Notes

The Trinity Dialectic is invoked by the agent internally before any "finalize" action. In the 143_protocol_a context, "finalize" means: mark a task complete, write a file to DISK, produce a handoff artifact, or report back to an orchestrator.

Agents self-score using the 3x3 matrix. When context limits prevent the full recursive evaluation, the three primary gate questions (Is this logically consistent? Does this align with purpose? Is this executable?) serve as the minimum viable check.

---

---

## Code

The reference implementation is in [`trinity.py`](./trinity.py).

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
print(result.phase.name)         # VERIFIED
print(result.final_verdict.name) # LOGOS_WINS
print(result.final_position)     # "Use the proven solution."
```

See [`examples/basic_eval.py`](./examples/basic_eval.py) for a full architecture decision walkthrough.
See [`examples/socratic_gate.py`](./examples/socratic_gate.py) for the Socratic question-evaluation pattern.

---

*Territory: SAGEx | Protocol: 143_protocol_a | 2026-04-16 | License: MIT*
