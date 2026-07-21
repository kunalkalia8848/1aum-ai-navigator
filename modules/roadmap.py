def generate_roadmap(use_case_name: str, start_date: str = None) -> dict:
    return {
        "use_case_name": use_case_name,
        "phases": [
            {
                "phase_name": "Days 1–15: Discovery and alignment",
                "timeline": "Days 1–15",
                "milestones": [
                    "Confirm the business objective.",
                    "Assign executive sponsor.",
                    "Define success metrics.",
                    "Map the current workflow.",
                    "Identify required data sources.",
                    "Confirm product ownership.",
                    "Complete the initial AI risk assessment.",
                ],
            },
            {
                "phase_name": "Days 16–35: Prototype and evaluation",
                "timeline": "Days 16–35",
                "milestones": [
                    "Develop a limited prototype.",
                    "Establish the current performance baseline.",
                    "Create an evaluation dataset.",
                    "Test accuracy and failure modes.",
                    "Define human oversight.",
                    "Confirm target architecture.",
                    "Review privacy and security requirements.",
                ],
            },
            {
                "phase_name": "Days 36–60: Pilot",
                "timeline": "Days 36–60",
                "milestones": [
                    "Integrate the solution into a controlled workflow.",
                    "Train pilot users.",
                    "Monitor usage and errors.",
                    "Measure business value.",
                    "Validate controls.",
                    "Collect user feedback.",
                    "Refine the operating process.",
                ],
            },
            {
                "phase_name": "Days 61–90: Production readiness and scale",
                "timeline": "Days 61–90",
                "milestones": [
                    "Complete production-readiness review.",
                    "Finalize controls and accountability.",
                    "Establish monitoring.",
                    "Document support ownership.",
                    "Approve or reject deployment.",
                    "Define the scale roadmap.",
                    "Record lessons learned.",
                ],
            },
        ],
    }


def generate_roadmap(use_case_name: str, start_date: str = None) -> dict:
    return {
        "use_case_name": use_case_name,
        "phases": [
            {
                "phase_name": "Days 1–15: Discovery and alignment",
                "timeline": "Days 1–15",
                "milestones": [
                    "Confirm the business objective.",
                    "Assign executive sponsor.",
                    "Define success metrics.",
                    "Map the current workflow.",
                    "Identify required data sources.",
                    "Confirm product ownership.",
                    "Complete the initial AI risk assessment.",
                ],
            },
            {
                "phase_name": "Days 16–35: Prototype and evaluation",
                "timeline": "Days 16–35",
                "milestones": [
                    "Develop a limited prototype.",
                    "Establish the current performance baseline.",
                    "Create an evaluation dataset.",
                    "Test accuracy and failure modes.",
                    "Define human oversight.",
                    "Confirm target architecture.",
                    "Review privacy and security requirements.",
                ],
            },
            {
                "phase_name": "Days 36–60: Pilot",
                "timeline": "Days 36–60",
                "milestones": [
                    "Integrate the solution into a controlled workflow.",
                    "Train pilot users.",
                    "Monitor usage and errors.",
                    "Measure business value.",
                    "Validate controls.",
                    "Collect user feedback.",
                    "Refine the operating process.",
                ],
            },
            {
                "phase_name": "Days 61–90: Production readiness and scale",
                "timeline": "Days 61–90",
                "milestones": [
                    "Complete production-readiness review.",
                    "Finalize controls and accountability.",
                    "Establish monitoring.",
                    "Document support ownership.",
                    "Approve or reject deployment.",
                    "Define the scale roadmap.",
                    "Record lessons learned.",
                ],
            },
        ],
    }


def generate_conditional_actions(
    readiness_scores: dict[str, float],
    highest_risk_severity: str,
    selected_use_case: dict,
) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []

    data_score = readiness_scores.get("Data Readiness", 0)
    governance_score = readiness_scores.get(
        "Governance, Risk, and Security",
        0,
    )
    talent_score = readiness_scores.get(
        "Talent and Operating Model",
        0,
    )
    adoption_score = readiness_scores.get(
        "Adoption and Change Management",
        0,
    )

    uc_risk = selected_use_case.get("scores", {}).get("risk", 1) if isinstance(selected_use_case.get("scores"), dict) else selected_use_case.get("risk", 1)

    if data_score < 3:
        actions.append(
            {
                "action": "Complete data profiling, ownership confirmation, quality assessment, and access approval before model development.",
                "phase": "Days 1–15",
                "trigger": "Data Readiness < 3.0",
                "rationale": "Insufficient data readiness increases implementation delay risks and model errors.",
                "suggested_owner": "Data Lead / Data Engineering"
            }
        )

    if governance_score < 3:
        actions.append(
            {
                "action": "Establish AI use case approval, risk review, documentation, and escalation processes.",
                "phase": "Days 1–15",
                "trigger": "Governance Maturity < 3.0",
                "rationale": "Immature governance controls increase regulatory and operational compliance exposure.",
                "suggested_owner": "AI Governance / Compliance Officer"
            }
        )

    if talent_score < 3:
        actions.append(
            {
                "action": "Confirm required business, data, engineering, security, and risk capabilities and address material skill gaps.",
                "phase": "Days 1–15",
                "trigger": "Talent & Operating Model < 3.0",
                "rationale": "Skill deficits increase dependency on external vendors and slow adoption.",
                "suggested_owner": "HR / Transformation Lead"
            }
        )

    if adoption_score < 3:
        actions.append(
            {
                "action": "Conduct user interviews and create a formal change, training, and adoption plan.",
                "phase": "Days 16–35",
                "trigger": "Adoption Maturity < 3.0",
                "rationale": "Low organizational change readiness limits downstream business value capture.",
                "suggested_owner": "Change Management / Business Owner"
            }
        )

    if highest_risk_severity in ["Critical", "High"]:
        actions.append(
            {
                "action": "Assign owners and approve mitigations for all critical and high risks before pilot authorization.",
                "phase": "Days 1–15",
                "trigger": f"Risk Severity = {highest_risk_severity}",
                "rationale": f"The presence of {highest_risk_severity.lower()} risks requires mandatory mitigation gates prior to pilot.",
                "suggested_owner": "Risk Lead / Executive Sponsor"
            }
        )

    if uc_risk >= 4:
        actions.append(
            {
                "action": "Perform enhanced failure mode testing and define mandatory human review checkpoints.",
                "phase": "Days 16–35",
                "trigger": f"Inherent Use-Case Risk = {uc_risk}/5",
                "rationale": "Elevated inherent risk demands rigorous validation and explicit human oversight.",
                "suggested_owner": "AI Technical Lead / Quality Assurance"
            }
        )

    return actions