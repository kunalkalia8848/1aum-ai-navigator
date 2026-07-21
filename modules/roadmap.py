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