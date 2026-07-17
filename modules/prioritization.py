from typing import Final

MIN_SCORE: Final = 1
MAX_SCORE: Final = 5

def validate_dimension_score(name: str, score: int) -> None:
    if not isinstance(score, int):
        raise TypeError(f"{name} must be an integer.")

    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(f"{name} must be between 1 and 5.")

def calculate_priority_score(
    impact: int,
    alignment: int,
    feasibility: int,
    data_readiness: int,
    risk: int,
) -> float:
    dimensions = {
        "impact": impact,
        "alignment": alignment,
        "feasibility": feasibility,
        "data_readiness": data_readiness,
        "risk": risk,
    }

    for name, value in dimensions.items():
        validate_dimension_score(name, value)

    inverse_risk = 6 - risk

    score = (
        impact * 0.30
        + alignment * 0.20
        + feasibility * 0.20
        + data_readiness * 0.20
        + inverse_risk * 0.10
    )

    return round(score, 2)