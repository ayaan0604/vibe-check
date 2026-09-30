from typing import List
from analyzer import CommentAnalysis
from pydantic import BaseModel
from collections import Counter
from comments import Comment

class AnalysisReport(BaseModel):
    total_comments: int
    intent_distribution: dict[str, float]
    reaction_distribution: dict[str, float]

    sarcasm_rate: float

    vibe: str
    chaos_index : float
    roast_to_hype_ratio : float | None

    comments : List[CommentAnalysis] | None = None

class Aggregator:

    def aggregate(self, analyses : List[CommentAnalysis]) -> AnalysisReport:

        total_comments = len(analyses)
        if total_comments == 0:
            return AnalysisReport(
                total_comments=0,
                intent_distribution={},
                reaction_distribution={},
                sarcasm_rate=0.0,
                vibe="NO DATA",
                chaos_index=0.0,
                roast_to_hype_ratio=None
            )


        #distributions

        intent_counts = Counter(
            analysis.intent
            for analysis in analyses
        )

        reaction_counts = Counter(
            analysis.reaction
            for analysis in analyses
        )

        intent_distribution = {
            intent: (count / total_comments) * 100
            for intent, count in intent_counts.items()
        }

        reaction_distribution = {
            reaction: (count / total_comments) * 100
            for reaction, count in reaction_counts.items()
        }

        #sarcasm
        
        sarcastic_count = sum(
            analysis.sarcastic
            for analysis in analyses
        )

        sarcasm_rate = (
            sarcastic_count / total_comments
        ) * 100

        #vibe

        vibe = self._calculate_vibe(
            intent_distribution
        )

        chaos_index = self._calculate_chaos_index(
            intent_distribution,
            reaction_distribution,
            sarcasm_rate
        )

        roast_count = intent_counts.get("ROAST", 0)
        hype_count = intent_counts.get("HYPE", 0)

        roast_to_hype_ratio = (
            round(roast_count / hype_count, 2)
            if hype_count > 0
            else None
        )

        return AnalysisReport(
            total_comments=total_comments,
            intent_distribution=intent_distribution,
            reaction_distribution=reaction_distribution,
            sarcasm_rate=sarcasm_rate,
            vibe=vibe,
            chaos_index=chaos_index,
            roast_to_hype_ratio=roast_to_hype_ratio,
            comments= analyses
        )

    def _calculate_vibe(self, intent_distribution: dict[str, float]) -> str:

        if not intent_distribution:
            return "NO DATA"

        dominant_intent = max(
            intent_distribution,
            key=intent_distribution.get
        )

        dominant_percentage = intent_distribution[dominant_intent]

        if dominant_intent == "HYPE" and dominant_percentage >= 35:
            return "HYPE"

        if dominant_intent == "ROAST" and dominant_percentage >= 35:
            return "ROASTY"

        if dominant_intent == "JOKE" and dominant_percentage >= 30:
            return "CHAOTIC"

        discussion_rate = (
            intent_distribution.get("WANDER", 0)
            + intent_distribution.get("SUGGESTION", 0)
        )

        if discussion_rate >= 30:
            return "DISCUSSION"

        if dominant_intent == "STORY" and dominant_percentage >= 30:
            return "STORYTIME"

        return "MIXED"

    def _calculate_chaos_index(self, intent_distribution: dict[str, float], reaction_distribution: dict[str, float], sarcasm_rate: float) -> float:

        chaos_index = (
            intent_distribution.get("JOKE", 0) * 0.25
            + intent_distribution.get("ROAST", 0) * 0.25
            + sarcasm_rate * 0.20
            + reaction_distribution.get("LOL", 0) * 0.15
            + reaction_distribution.get("FLABBERGASTED", 0) * 0.15
        )

        return round(chaos_index, 2)