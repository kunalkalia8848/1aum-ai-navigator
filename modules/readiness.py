from collections import defaultdict
from typing import Any

VALID_MIN_SCORE = 1
VALID_MAX_SCORE = 5

def validate_readiness_responses(
    responses: list[dict[str, Any]],
) -> None:
    if not responses:
        raise ValueError("At least one readiness response is required.")

    for response in responses:
        required_fields = {"category", "question_id", "score"}
        missing_fields = required_fields - response.keys()

        if missing_fields:
            raise ValueError(
                f"Response is missing required fields: {missing_fields}"
            )

        score = response["score"]

        if not isinstance(score, int):
            raise TypeError("Readiness scores must be integers.")

        if not VALID_MIN_SCORE <= score <= VALID_MAX_SCORE:
            raise ValueError("Readiness scores must be between 1 and 5.")

def calculate_readiness_scores(
    responses: list[dict[str, Any]],
) -> dict[str, Any]:
    validate_readiness_responses(responses)

    category_scores: dict[str, list[int]] = defaultdict(list)

    for response in responses:
        category_scores[response["category"]].append(response["score"])

    results = {
        category: round(sum(scores) / len(scores), 2)
        for category, scores in category_scores.items()
    }

    overall_score = round(
        sum(results.values()) / len(results),
        2,
    )

    return {
        "category_scores": results,
        "overall_score": overall_score,
    }

def maturity_level(score: float) -> str:
    if score < 2:
        return "Ad Hoc"
    if score < 3:
        return "Emerging"
    if score < 4:
        return "Developing"
    if score < 4.5:
        return "Established"
    return "Leading"

def identify_top_gaps(
    category_scores: dict[str, float],
    number_of_gaps: int = 3,
) -> list[tuple[str, float]]:
    return sorted(
        category_scores.items(),
        key=lambda item: item[1],
    )[:number_of_gaps]