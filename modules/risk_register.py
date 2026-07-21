def calculate_risk_score(likelihood: int, impact: int) -> int:
    for name, score in {
        "likelihood": likelihood,
        "impact": impact,
    }.items():
        if not isinstance(score, int):
            raise TypeError(f"{name} must be an integer.")

        if not 1 <= score <= 5:
            raise ValueError(f"{name} must be between 1 and 5.")

    return likelihood * impact


def classify_risk(score: int) -> str:
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Medium"
    return "Low"