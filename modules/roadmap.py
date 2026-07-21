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

    if data_score < 3:
        actions.append(
            {
                "phase": "Days 1–15",
                "action": (
                    "Complete data profiling, ownership confirmation, "
                    "quality assessment, and access approval before "
                    "model development."
                ),
                "reason": "Data readiness scored below 3.0.",
            }
        )

    if governance_score < 3:
        actions.append(
            {
                "phase": "Days 1–15",
                "action": (
                    "Establish AI use case approval, risk review, "
                    "documentation, and escalation processes."
                ),
                "reason": "Governance maturity scored below 3.0.",
            }
        )

    if talent_score < 3:
        actions.append(
            {
                "phase": "Days 1–15",
                "action": (
                    "Confirm required business, data, engineering, security, "
                    "and risk capabilities and address material skill gaps."
                ),
                "reason": "Talent and operating model maturity is limited.",
            }
        )

    if adoption_score < 3:
        actions.append(
            {
                "phase": "Days 16–35",
                "action": (
                    "Conduct user interviews and create a formal change, "
                    "training, and adoption plan."
                ),
                "reason": "Adoption maturity scored below 3.0.",
            }
        )

    if highest_risk_severity in ["Critical", "High"]:
        actions.append(
            {
                "phase": "Days 1–15",
                "action": (
                    "Assign owners and approve mitigations for all critical "
                    "and high risks before pilot authorization."
                ),
                "reason": (
                    f"The assessment contains {highest_risk_severity.lower()} "
                    "risks."
                ),
            }
        )

    if selected_use_case.get("risk", 1) >= 4:
        actions.append(
            {
                "phase": "Days 16–35",
                "action": (
                    "Perform enhanced failure mode testing and define "
                    "mandatory human review checkpoints."
                ),
                "reason": "The selected use case has elevated inherent risk.",
            }
        )

    return actions