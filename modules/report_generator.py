def generate_deterministic_summary(
    organization_name: str,
    overall_score: float,
    maturity: str,
    gaps: list[tuple[str, float]],
    top_use_cases: list[dict],
    critical_risk_count: int,
) -> dict:
    gap_names = [category for category, _ in gaps]
    use_case_names = [
        use_case["name"]
        for use_case in top_use_cases[:3]
    ]

    current_state = (
        f"{organization_name} received an overall AI readiness score of "
        f"{overall_score:.2f} out of 5, corresponding to the "
        f"{maturity} maturity level."
    )

    risk_statement = (
        f"The initial assessment identified {critical_risk_count} "
        "critical risks requiring executive review."
        if critical_risk_count
        else "No critical risks were identified in the initial assessment."
    )

    return {
        "current_state": current_state,
        "key_gaps": gap_names,
        "priority_use_cases": use_case_names,
        "risk_summary": risk_statement,
        "immediate_actions": [
            "Assign accountable owners for the selected use case.",
            "Confirm success metrics and baseline performance.",
            "Resolve critical data, governance, and risk prerequisites.",
        ],
    }