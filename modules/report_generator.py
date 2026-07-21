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
def prepare_llm_payload(
    org_profile: dict,
    readiness_results: dict,
    use_cases: list[dict],
    risk_register: list[dict],
    roadmap_actions: list[dict]
) -> dict:
    """
    Sanitizes and aggregates structured data for LLM narrative generation.
    Strictly excludes PII, individual names, and confidential free text.
    """
    # 1. Industry & Size Category Only (Excludes explicit company/person names)
    sanitized_org = {
        "industry": org_profile.get("industry", "Unspecified"),
        "company_size": org_profile.get("company_size", "Unspecified"),
        "ai_maturity_target": org_profile.get("ai_maturity_target", "Unspecified")
    }

    # 2. Aggregated Readiness Metrics
    sanitized_readiness = {
        "overall_score": readiness_results.get("overall_score", 0.0),
        "maturity_level": readiness_results.get("maturity_level", "Unassessed"),
        "category_scores": readiness_results.get("category_scores", {}),
        "top_gaps": [cat for cat, _ in readiness_results.get("top_gaps", [])]
    }

    # 3. High-level Use Case Metadata (Excludes custom free-text assumptions)
    sorted_ucs = sorted(use_cases, key=lambda x: x.get("priority_score", 0), reverse=True)[:3]
    sanitized_use_cases = [
        {
            "name": uc.get("name"),
            "solution_type": uc.get("solution_type"),
            "classification": uc.get("classification"),
            "priority_score": uc.get("priority_score")
        }
        for uc in sorted_ucs
    ]

    # 4. Aggregate Risk Profile (Counts only, no individual risk owners or PII)
    critical_count = sum(1 for r in risk_register if r.get("severity") == "Critical")
    high_count = sum(1 for r in risk_register if r.get("severity") == "High")
    med_count = sum(1 for r in risk_register if r.get("severity") == "Medium")
    low_count = sum(1 for r in risk_register if r.get("severity") == "Low")

    sanitized_risks = {
        "total_risks": len(risk_register),
        "critical_count": critical_count,
        "high_count": high_count,
        "medium_count": med_count,
        "low_count": low_count
    }

    # 5. High-level Roadmap Action Items (Excludes assigned owner names)
    sanitized_roadmap = [
        {
            "phase": act.get("phase"),
            "trigger": act.get("trigger"),
            "action": act.get("action")
        }
        for act in roadmap_actions
    ]

    return {
        "organization": sanitized_org,
        "readiness": sanitized_readiness,
        "priority_use_cases": sanitized_use_cases,
        "risk_summary": sanitized_risks,
        "key_roadmap_adjustments": sanitized_roadmap
    }