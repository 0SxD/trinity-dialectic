"""
Basic Trinity Dialectic evaluation example.

Demonstrates: Logos (reason) and Pathos (creativity) fighting over a decision.
Ethos arbitrates. The fight itself is the productive mechanism.

Run:
    python examples/basic_eval.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity import (
    TrinityEngine,
    DefaultDialecticGate,
    TrinityPhase,
    ThreatLevel,
)


def run_architecture_decision() -> None:
    """
    Example: Should we use a monolith or microservices?

    Logos argues from evidence (performance benchmarks, team size).
    Pathos argues from vision (scalability, future flexibility).
    Ethos finds the mean.
    """
    print("=" * 60)
    print("TRINITY DIALECTIC -- Architecture Decision Example")
    print("Question: Monolith vs. microservices for a 3-person team?")
    print("=" * 60)

    context = {
        # Logos position: data says monolith for small teams
        "logos_claim": "Monolith. Team of 3 cannot support microservices operational overhead.",
        "logos_reasoning": (
            "Microservices require: container orchestration, distributed tracing, "
            "service mesh, CI/CD per service, on-call rotation per service boundary. "
            "For a 3-person team, this is operationally fatal."
        ),
        "logos_evidence": [
            "Netflix: 700 engineers before going microservices (2012)",
            "Segment: migrated back to monolith after microservices failure (2022)",
            "Martin Fowler: 'Don't start with microservices' (2015, still current)",
        ],
        "logos_confidence": 0.82,

        # Pathos position: vision demands scalability now
        "pathos_claim": "Design for microservices, implement as monolith (modular monolith).",
        "pathos_reasoning": (
            "A modular monolith with clean service boundaries costs nothing extra now "
            "and can be split when the team scales. Starting with a spaghetti monolith "
            "creates debt that is painful and expensive to undo at scale."
        ),
        "pathos_evidence": [
            "Shopify: modular monolith for years, scaled to $50B+ GMV before splitting",
            "Stack Overflow: monolith serving billions of requests, team of 15",
        ],
        "pathos_confidence": 0.71,

        "threat_level": ThreatLevel.NONE,
        "violations": [],
    }

    engine = TrinityEngine(gate=DefaultDialecticGate())
    result = engine.run_dialectic(context)

    print(f"\nPhase:   {result.phase.name}")
    print(f"Verdict: {result.final_verdict.name}")
    print(f"Position: {result.final_position}")
    print(f"Rounds:  {len(result.rounds)}")
    print(f"Healthy: {engine.is_healthy()}")

    if result.rounds:
        last = result.rounds[-1]
        print(f"\nEthos ruling:")
        print(f"  {last.ethos_ruling.ruling_reason}")
        print(f"  Doctrine of the Mean: {last.ethos_ruling.doctrine_of_mean}")
        print(f"  Phronesis: {last.ethos_ruling.phronesis_check}")


def run_existential_block() -> None:
    """
    Example: Existential threat -- all 9 sub-evaluators fire simultaneously.
    """
    print("\n" + "=" * 60)
    print("TRINITY DIALECTIC -- Existential Block Example")
    print("Question: Should we deploy untested code to production at 2am?")
    print("=" * 60)

    context = {
        "logos_claim": "Deploy. The bug is reproducible and the fix is one line.",
        "logos_confidence": 0.6,
        "pathos_claim": "Do not deploy. 2am deploy without test coverage is reckless.",
        "pathos_confidence": 0.9,
        "threat_level": ThreatLevel.EXISTENTIAL,
        "violations": ["no test coverage", "no review", "production at 2am"],
    }

    engine = TrinityEngine(gate=DefaultDialecticGate())
    result = engine.run_dialectic(context)

    print(f"\nPhase:   {result.phase.name}")
    print(f"Verdict: {result.final_verdict.name}")
    print(f"Position: {result.final_position}")
    print(f"\nSub-evaluators that fired: {len(result.rounds[0].sub_evaluations)}")
    for sub in result.rounds[0].sub_evaluations[:3]:
        print(f"  [{sub.evaluator}] passed={sub.passed} | {sub.reason[:60]}...")


if __name__ == "__main__":
    run_architecture_decision()
    run_existential_block()
