DEMO_COMPANIES = {
    "Company A: Precision Manufacturer": {
        "org_profile": {
            "company_name": "Apex Precision Components",
            "industry": "Manufacturing",
            "company_size": "500-1000 employees",
            "ai_maturity_target": "Pilot Phase",
            "notes": "High executive backing, fragmented IT infrastructure, limited formal AI governance."
        },
        "readiness_scores": {
            "overall_score": 2.45,
            "maturity_level": "Exploring",
            "category_scores": {
                "Strategy & Executive Alignment": 4.0,
                "Data & Infrastructure": 1.8,
                "Governance & Risk Management": 1.5,
                "Talent & Deployment Capability": 2.5
            },
            "top_gaps": [
                ["Governance & Risk Management", 1.5],
                ["Data & Infrastructure", 1.8]
            ]
        },
        "use_cases": [
            {
                "name": "Predictive Maintenance for Machining Tools",
                "business_owner": "Ops & Maintenance Lead",
                "solution_type": "Predictive Analytics",
                "classification": "Strategic",
                "priority_score": 8.2,
                "recommendation_reason": "High ROI potential on reducing unplanned downtime."
            },
            {
                "name": "Computer-Vision Quality Inspection",
                "business_owner": "Quality Assurance Director",
                "solution_type": "Computer Vision",
                "classification": "Quick Win",
                "priority_score": 7.8,
                "recommendation_reason": "Solves immediate defect-rate inspection bottleneck."
            },
            {
                "name": "Automated Inventory Forecasting",
                "business_owner": "Supply Chain Manager",
                "solution_type": "Demand Forecasting",
                "classification": "Long-Term",
                "priority_score": 5.4,
                "recommendation_reason": "Requires significant data cleanup before scaling."
            }
        ],
        "risk_register": [
            {
                "risk_id": "R01",
                "use_case": "Predictive Maintenance for Machining Tools",
                "category": "Data Quality & Accessibility",
                "severity": "Critical",
                "risk_score": 8.5,
                "mitigation": "Perform sensor telemetry data profiling and consolidate data pipelines.",
                "owner": "Data Lead",
                "status": "Open",
                "review_date": "2026-08-01"
            },
            {
                "risk_id": "R02",
                "use_case": "Computer-Vision Quality Inspection",
                "category": "Model Accuracy & Drift",
                "severity": "Medium",
                "risk_score": 5.0,
                "mitigation": "Establish daily calibration checks and baseline retraining datasets.",
                "owner": "QA Lead",
                "status": "In Progress",
                "review_date": "2026-08-15"
            }
        ]
    },
    "Company B: Regional Bank": {
        "org_profile": {
            "company_name": "Horizon Regional Bank",
            "industry": "Financial Services",
            "company_size": "1000-5000 employees",
            "ai_maturity_target": "Enterprise Scaled",
            "notes": "Strong risk governance, strict compliance requirements, moderate AI engineering capacity."
        },
        "readiness_scores": {
            "overall_score": 3.85,
            "maturity_level": "Scaling",
            "category_scores": {
                "Strategy & Executive Alignment": 4.2,
                "Data & Infrastructure": 3.5,
                "Governance & Risk Management": 4.8,
                "Talent & Deployment Capability": 2.9
            },
            "top_gaps": [
                ["Talent & Deployment Capability", 2.9],
                ["Data & Infrastructure", 3.5]
            ]
        },
        "use_cases": [
            {
                "name": "Customer Support Document Intelligence",
                "business_owner": "Head of Retail Banking",
                "solution_type": "Generative AI / NLP",
                "classification": "Quick Win",
                "priority_score": 8.9,
                "recommendation_reason": "High internal efficiency gains with manageable regulatory risk."
            },
            {
                "name": "Loan Application Fraud Assistant",
                "business_owner": "Risk & Compliance Lead",
                "solution_type": "Machine Learning Classification",
                "classification": "Strategic",
                "priority_score": 8.1,
                "recommendation_reason": "Substantially cuts review cycles; requires explainability controls."
            },
            {
                "name": "Automated Commercial Underwriting Summarizer",
                "business_owner": "Commercial Lending VP",
                "solution_type": "Document Processing",
                "classification": "Strategic",
                "priority_score": 7.4,
                "recommendation_reason": "Speeds up deal flow; human-in-the-loop validation required."
            }
        ],
        "risk_register": [
            {
                "risk_id": "R01",
                "use_case": "Customer Support Document Intelligence",
                "category": "Regulatory & Privacy Leakage",
                "severity": "High",
                "risk_score": 7.2,
                "mitigation": "Implement PII redacting middleware prior to prompt assembly.",
                "owner": "Compliance Lead",
                "status": "In Progress",
                "review_date": "2026-08-01"
            },
            {
                "risk_id": "R02",
                "use_case": "Loan Application Fraud Assistant",
                "category": "Algorithmic Bias & Fair Lending",
                "severity": "Critical",
                "risk_score": 9.0,
                "mitigation": "Conduct independent algorithmic bias audits and model transparency checks.",
                "owner": "Risk Officer",
                "status": "Open",
                "review_date": "2026-08-10"
            }
        ]
    },
    "Company C: Logistics Provider": {
        "org_profile": {
            "company_name": "Vanguard Logistics",
            "industry": "Transportation & Logistics",
            "company_size": "500-1000 employees",
            "ai_maturity_target": "Operational Integration",
            "notes": "Strong operational telemetry, multiple automation opportunities, weak change management."
        },
        "readiness_scores": {
            "overall_score": 3.10,
            "maturity_level": "Developing",
            "category_scores": {
                "Strategy & Executive Alignment": 3.2,
                "Data & Infrastructure": 4.1,
                "Governance & Risk Management": 2.2,
                "Talent & Deployment Capability": 2.9
            },
            "top_gaps": [
                ["Governance & Risk Management", 2.2],
                ["Talent & Deployment Capability", 2.9]
            ]
        },
        "use_cases": [
            {
                "name": "Dynamic Route & Load Optimization",
                "business_owner": "Director of Fleet Operations",
                "solution_type": "Optimization Algorithm",
                "classification": "Quick Win",
                "priority_score": 9.1,
                "recommendation_reason": "Leverages strong existing GPS and fleet data for immediate fuel savings."
            },
            {
                "name": "Automated Exception & Delay Management",
                "business_owner": "Customer Success Manager",
                "solution_type": "Rules Engine + AI Assistant",
                "classification": "Strategic",
                "priority_score": 7.6,
                "recommendation_reason": "Proactively notifies shippers of shipment delays."
            },
            {
                "name": "Warehouse Capacity Forecasting",
                "business_owner": "Warehouse Operations VP",
                "solution_type": "Time Series Forecasting",
                "classification": "Long-Term",
                "priority_score": 6.2,
                "recommendation_reason": "Requires standardized intake telemetry across regional hubs."
            }
        ],
        "risk_register": [
            {
                "risk_id": "R01",
                "use_case": "Dynamic Route & Load Optimization",
                "category": "User Adoption & Change Management",
                "severity": "High",
                "risk_score": 7.0,
                "mitigation": "Conduct driver user-interviews and roll out phased training programs.",
                "owner": "Operations Lead",
                "status": "Open",
                "review_date": "2026-08-01"
            }
        ]
    }
}