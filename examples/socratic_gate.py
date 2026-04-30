"""
Socratic Gate example -- Trinity Dialectic applied to question generation.

The Socratic pattern: before an agent answers, it runs the Trinity to identify
what question it SHOULD have been asked. This surfaces blind spots that the
original prompt didn't know to address.

Pattern:
    1. Logos identifies the question the prompt actually asks.
    2. Pathos identifies the question the prompt SHOULD have asked.
    3. Ethos decides whether to answer the stated question or surface the better one.

This is how the 143_protocol_a system handles the "Zero Assumption Mandate":
never assume you have the full picture. The Socratic gate asks: what would I
need to be asked to give the best possible answer?
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trinity import (
    TrinityEngine,
    DialecticGate,
    Argument,
    EthosRuling,
    ThreatLevel,
    Verdict,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class SocraticResult:
    stated_question: str
    better_question: str | None
    should_redirect: bool
    reasoning: str


class SocraticGate(DialecticGate):
    """
    A Trinity gate specialized for question evaluation.

    Logos: analyze what the prompt explicitly asks.
    Pathos: surface what the prompter likely actually needs.
    Ethos: decide whether to answer the stated question or surface the gap.
    """

    def logos_argues(self, context: dict[str, Any], round_num: int) -> Argument:
        stated = context.get("stated_question", "")
        return Argument(
            claim=f"Answer the stated question: '{stated}'",
            reasoning=(
                "The user asked a specific question. Answering something they did not ask "
                "violates the principle of least surprise and may be presumptuous."
            ),
            evidence=[
                "User explicitly asked: " + stated,
                "Redirecting without permission risks missing the actual need.",
            ],
            appeal_to_ethos="Our character demands we respect what the user actually asked.",
            confidence=context.get("logos_confidence", 0.6),
        )

    def pathos_argues(
        self, context: dict[str, Any], logos_position: Argument, round_num: int
    ) -> Argument:
        better = context.get("better_question", "")
        gap = context.get("identified_gap", "")
        return Argument(
            claim=f"Surface the better question first: '{better}'",
            reasoning=(
                f"The stated question has a blind spot: {gap}. "
                "Answering the stated question without surfacing this gap produces "
                "a technically correct but strategically misleading response."
            ),
            evidence=[
                "Identified gap: " + gap,
                "Better question: " + better,
                "Socratic tradition: the teacher's job is to ask the right question, "
                "not just answer the wrong one.",
            ],
            appeal_to_ethos="Our character demands we help the user get what they actually need.",
            confidence=context.get("pathos_confidence", 0.75),
        )

    def ethos_arbitrates(
        self, logos: Argument, pathos: Argument, round_num: int
    ) -> EthosRuling:
        # If the gap is significant, redirect. Otherwise answer the stated question.
        gap_severity = len(pathos.evidence)  # proxy for gap significance

        if gap_severity >= 3 and pathos.confidence > logos.confidence:
            return EthosRuling(
                verdict=Verdict.PATHOS_WINS,
                ruling_reason="Gap is significant enough to surface before answering.",
                doctrine_of_mean=(
                    "Surface the gap AND answer the stated question -- both, not either/or."
                ),
                phronesis_check="Worth redirecting: answering the wrong question well is still wrong.",
            )

        return EthosRuling(
            verdict=Verdict.LOGOS_WINS,
            ruling_reason="Gap is minor. Answer the stated question directly.",
            doctrine_of_mean="Respect the user's framing while noting the gap in passing.",
            phronesis_check="Answering the stated question is the practical path here.",
        )

    def assess_threat(self, context: dict[str, Any]) -> ThreatLevel:
        return ThreatLevel.NONE


def evaluate_question(
    stated_question: str,
    better_question: str,
    identified_gap: str,
    logos_confidence: float = 0.6,
    pathos_confidence: float = 0.75,
) -> SocraticResult:
    """Run the Socratic gate on a question."""
    context = {
        "stated_question": stated_question,
        "better_question": better_question,
        "identified_gap": identified_gap,
        "logos_confidence": logos_confidence,
        "pathos_confidence": pathos_confidence,
        "violations": [],
    }

    engine = TrinityEngine(gate=SocraticGate())
    result = engine.run_dialectic(context)

    should_redirect = result.final_verdict.name == "PATHOS_WINS"
    reasoning = ""
    if result.rounds:
        reasoning = result.rounds[-1].ethos_ruling.ruling_reason

    return SocraticResult(
        stated_question=stated_question,
        better_question=better_question if should_redirect else None,
        should_redirect=should_redirect,
        reasoning=reasoning,
    )


if __name__ == "__main__":
    print("=" * 60)
    print("SOCRATIC GATE EXAMPLES")
    print("=" * 60)

    cases = [
        {
            "stated": "What's the fastest sorting algorithm?",
            "better": "What sorting algorithm is best for my specific data distribution and size?",
            "gap": "QuickSort is fastest on average but O(n^2) worst case. "
                   "'Fastest' depends entirely on data characteristics.",
            "logos_conf": 0.5,
            "pathos_conf": 0.85,
        },
        {
            "stated": "How do I fix this bug?",
            "better": "Why does this bug exist and how do I prevent this class of bug?",
            "gap": "Fixing symptoms without understanding root cause creates recurrence.",
            "logos_conf": 0.7,
            "pathos_conf": 0.6,
        },
        {
            "stated": "What's the capital of France?",
            "better": "What's the capital of France?",  # No redirect needed
            "gap": "None -- question is precise and complete.",
            "logos_conf": 0.95,
            "pathos_conf": 0.2,
        },
    ]

    for case in cases:
        result = evaluate_question(
            stated_question=case["stated"],
            better_question=case["better"],
            identified_gap=case["gap"],
            logos_confidence=case["logos_conf"],
            pathos_confidence=case["pathos_conf"],
        )
        print(f"\nStated: {result.stated_question}")
        print(f"Redirect: {result.should_redirect}")
        if result.should_redirect:
            print(f"Better question: {result.better_question}")
        print(f"Reasoning: {result.reasoning}")
        print("-" * 40)
