import streamlit as st
import json
import os
import pandas as pd
import datetime

# Import backend modules
from modules.report_generator import generate_deterministic_summary
from modules.roadmap import generate_roadmap, generate_conditional_actions
from modules.readiness import calculate_readiness_scores, maturity_level, identify_top_gaps, GAP_RECOMMENDATIONS
from modules.demo_data import DEMO_COMPANIES
from modules.report_generator import (
    generate_deterministic_summary,
    prepare_llm_payload,
    generate_ai_summary,
    create_executive_report
)
from modules.report_generator import (
    generate_deterministic_summary,
    prepare_llm_payload,
    generate_ai_summary
)
from modules.prioritization import (
    calculate_priority_score, 
    classify_use_case, 
    explain_recommendation,
    normalize_name
)
from modules.risk_register import calculate_risk_score, classify_risk

# 1. Page Configuration
st.set_page_config(
    page_title="1AUM Navigator",
    page_icon="🧭",
    layout="wide",
)

# 2. Initialize Session State
def initialize_session_state() -> None:
    defaults = {
        "organization_profile": {},
        "readiness_responses": {},
        "readiness_results": {},
        "use_cases": [],
        "risk_register": [],
        "roadmap": {},
        "executive_summary": {},
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# Helper function to load JSON questions
def load_questions():
    file_path = os.path.join("data", "readiness_questions.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# Helper function to load JSON risk library
def load_risk_library():
    file_path = os.path.join("data", "risk_library.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}
# Map descriptive labels to numeric scores
SCORE_MAP = {
    "1 - Not established": 1,
    "2 - Early stage": 2,
    "3 - Partially established": 3,
    "4 - Mostly established": 4,
    "5 - Mature and repeatable": 5
}

# 3. Sidebar Workflow Indicator
section = st.sidebar.radio(
    "Navigator Workflow",
    [
        "1. Organization Profile",
        "2. Readiness Assessment",
        "3. Use-Case Prioritization",
        "4. Risk Register",
        "5. Roadmap and Report",
    ],
)
# --- STAGE 11: DEMO MODE CONTROLS ---
st.sidebar.write("---")
st.sidebar.subheader("⚡ Demo Mode")
selected_demo = st.sidebar.selectbox("Select Sample Profile", options=list(DEMO_COMPANIES.keys()))

if st.sidebar.button("🚀 Load Demo Organization"):
    demo = DEMO_COMPANIES[selected_demo]
    st.session_state["org_profile"] = demo["org_profile"]
    st.session_state["readiness_results"] = demo["readiness_scores"]
    st.session_state["use_cases"] = demo["use_cases"]
    st.session_state["risk_register"] = demo["risk_register"]
    st.sidebar.success(f"Loaded {selected_demo.split(':')[0]} data!")
    st.rerun()
# 4. Main UI Layout Routing
if section == "1. Organization Profile":
    st.title("1AUM Navigator")
    st.subheader("From AI opportunity to governed execution.")

    st.info(
        "Do not enter confidential, personal, proprietary, or regulated information. "
        "This tool supports planning and does not replace legal, compliance, "
        "cybersecurity, or risk review."
    )

    st.write(
        """
        Assess organizational AI readiness, prioritize AI use cases, 
        identify material risks, and generate a practical 90-day roadmap.
        """
    )
    st.success("Application initialized successfully.")

elif section == "2. Readiness Assessment":
    st.title("AI Readiness Assessment")
    st.write("Evaluate capabilities across the core dimensions:")
    
    questions = load_questions()
    
    if questions:
        # 1. Correctly group questions by category first
        categories = {}
        for q in questions:
            cat = q["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q)
            
        # 2. Now loop through the built categories to display them
        for cat, q_list in categories.items():
            with st.expander(cat, expanded=True):
                for q in q_list:
                    selected_label = st.radio(
                        q["question"],
                        options=list(SCORE_MAP.keys()),
                        key=f"q_{q['id']}"
                    )
                    score_val = SCORE_MAP[selected_label]
                    st.session_state.readiness_responses[q["id"]] = {
                        "category": q["category"],
                        "question_id": q["id"],
                        "score": score_val
                    }
        
        st.write("---")
        
        if st.button("Submit Assessment", type="primary"):
            responses_list = list(st.session_state.readiness_responses.values())
            if responses_list:
                scores_data = calculate_readiness_scores(responses_list)
                st.session_state.readiness_results = scores_data
                st.success("Assessment calculated and saved successfully!")
            else:
                st.error("Please answer the questions before submitting.")
                
        if st.session_state.readiness_results:
            results = st.session_state.readiness_results
            overall_score = results["overall_score"]
            category_scores = results["category_scores"]
            
            percentage_score = round((overall_score / 5) * 100)
            mat_level = maturity_level(overall_score)
            
            st.write("### Assessment Results")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Overall Score", f"{overall_score} / 5")
            col2.metric("Percentage Equivalent", f"{percentage_score}%")
            col3.metric("Maturity Level", mat_level)
            
            st.write("#### Scores by Category")
            df = pd.DataFrame({
                "Category": list(category_scores.keys()),
                "Score": list(category_scores.values())
            })
            st.bar_chart(data=df, x="Category", y="Score")
            
            st.write("#### Top Gaps & Key Recommendations")
            top_gaps = identify_top_gaps(category_scores, number_of_gaps=3)
            
            for gap_cat, gap_score in top_gaps:
                st.warning(f"**{gap_cat}** (Score: {gap_score}/5)")
                rec_text = GAP_RECOMMENDATIONS.get(
                    gap_cat, 
                    "Standardize existing processes, document edge test-cases, and track operational execution metrics."
                )
                st.write(f"👉 *Recommendation:* {rec_text}")
                    
    else:
        st.error("Could not load readiness questions from data folder.")
elif section == "3. Use-Case Prioritization":
    st.title("Use-Case Prioritization")
    st.write("Submit and evaluate your organizational AI initiatives.")

    # --- INTAKE FORM ---
    with st.form("use_case_intake_form", clear_on_submit=True):
        st.write("### Add New AI Use Case")
        
        uc_name = st.text_input("Use-case name")
        business_problem = st.text_area("Business problem")
        business_owner = st.text_input("Business owner or function")
        intended_users = st.text_input("Intended users")
        business_benefit = st.text_area("Expected business benefit")
        required_data = st.text_area("Required data")
        
        solution_type = st.selectbox(
            "AI solution type",
            options=[
                "Predictive analytics",
                "Computer vision",
                "Generative AI",
                "Intelligent automation",
                "Optimization",
                "Natural-language processing",
                "Other"
            ]
        )
        
        regulatory_sensitivity = st.text_input("Regulatory sensitivity")
        implementation_assumptions = st.text_area("Implementation assumptions")
        
        st.write("---")
        st.write("### Dimension Evaluation")
        
        business_impact = st.slider("Business Impact (5 = Favorable/Highest Impact)", min_value=1, max_value=5, value=3)
        strategic_alignment = st.slider("Strategic Alignment (5 = Favorable/Perfect Alignment)", min_value=1, max_value=5, value=3)
        technical_feasibility = st.slider("Technical Feasibility (5 = Favorable/Easiest to Build)", min_value=1, max_value=5, value=3)
        data_readiness_score = st.slider("Data Readiness (5 = Favorable/Highly Ready Data)", min_value=1, max_value=5, value=3)
        risk_score = st.slider("Risk (5 = High Risk, 1 = Low Risk)", min_value=1, max_value=5, value=1)
        
        submit_uc = st.form_submit_button("Add Use Case")
        
        if submit_uc:
            if not uc_name.strip():
                st.error("Please provide a Use-case name.")
            else:
                # Step 33: Prevent Duplicate Names
                existing_names = [normalize_name(u["name"]) for u in st.session_state.use_cases]
                if normalize_name(uc_name) in existing_names:
                    st.error(f"A use case with the name '{uc_name}' already exists.")
                else:
                    scores_dict = {
                        "impact": business_impact,
                        "alignment": strategic_alignment,
                        "feasibility": technical_feasibility,
                        "data_readiness": data_readiness_score,
                        "risk": risk_score
                    }

                    calculated_priority = calculate_priority_score(**scores_dict)
                    classification = classify_use_case(**scores_dict)
                    explanation = explain_recommendation(scores_dict)
                    
                    new_use_case = {
                        "name": uc_name.strip(),
                        "business_problem": business_problem,
                        "business_owner": business_owner,
                        "intended_users": intended_users,
                        "business_benefit": business_benefit,
                        "required_data": required_data,
                        "solution_type": solution_type,
                        "regulatory_sensitivity": regulatory_sensitivity,
                        "implementation_assumptions": implementation_assumptions,
                        "priority_score": calculated_priority,
                        "classification": classification,
                        "explanation": explanation,
                        "scores": {
                            "business_impact": business_impact,
                            "strategic_alignment": strategic_alignment,
                            "technical_feasibility": technical_feasibility,
                            "data_readiness": data_readiness_score,
                            "risk": risk_score
                        }
                    }
                    st.session_state.use_cases.append(new_use_case)
                    st.success(f"Use case '{uc_name}' added and classified as '{classification}'!")

    # --- STEP 32: PORTFOLIO DISPLAY & MANAGEMENT ---
    if st.session_state.use_cases:
        st.write("---")
        st.write("## Use-Case Portfolio Overview")

        # Sort use cases by priority score (descending)
        sorted_cases = sorted(st.session_state.use_cases, key=lambda x: x["priority_score"], reverse=True)

        # 1. Top Three Use Cases
        st.write("### 🏆 Top Recommended Use Cases")
        top_three = sorted_cases[:3]
        col_a, col_b, col_c = st.columns(3)
        cols = [col_a, col_b, col_c]
        for idx, uc in enumerate(top_three):
            with cols[idx]:
                st.metric(
                    label=f"#{idx+1} {uc['name']}",
                    value=f"Score: {uc['priority_score']}",
                    delta=uc['classification']
                )
                st.caption(f"**Owner:** {uc['business_owner'] or 'Unassigned'}")
                st.caption(f"**Rationale:** {uc['explanation']}")

        # 2. Ranked Table
        st.write("### 📊 Ranked Portfolio Table")
        table_data = []
        for uc in sorted_cases:
            table_data.append({
                "Use Case": uc["name"],
                "Priority Score": uc["priority_score"],
                "Classification": uc["classification"],
                "Business Owner": uc["business_owner"],
                "Risk Score": uc["scores"]["risk"],
                "Recommendation Explanation": uc["explanation"],
            })
        df_portfolio = pd.DataFrame(table_data)
        st.dataframe(df_portfolio, use_container_width=True)

        # 3. Impact vs. Feasibility Scatter Chart
        st.write("### 🎯 Impact vs. Feasibility Matrix")
        scatter_data = []
        for uc in st.session_state.use_cases:
            scatter_data.append({
                "Use Case": uc["name"],
                "Business Impact": uc["scores"]["business_impact"],
                "Technical Feasibility": uc["scores"]["technical_feasibility"],
                "Classification": uc["classification"]
            })
        df_scatter = pd.DataFrame(scatter_data)
        st.scatter_chart(
            df_scatter,
            x="Technical Feasibility",
            y="Business Impact",
            color="Classification"
        )

        # 4. Manage & Delete Use Cases
        st.write("### 🛠️ Manage Portfolio Entries")
        for idx, uc in enumerate(st.session_state.use_cases):
            with st.expander(f"{uc['name']} — [{uc['classification']}] (Score: {uc['priority_score']})"):
                st.write(f"**Business Owner/Function:** {uc['business_owner']}")
                st.write(f"**Business Problem:** {uc['business_problem']}")
                st.write(f"**Solution Type:** {uc['solution_type']}")
                st.write(f"**Explanation:** {uc['explanation']}")
                
                if st.button(f"Delete '{uc['name']}'", key=f"del_{idx}"):
                    st.session_state.use_cases.pop(idx)
                    st.rerun()
elif section == "4. Risk Register":
    st.title("Risk Register")
    st.write("Identify, score, and manage material AI risks across logged use cases.")

    st.info(
        "💡 Note: The risks suggested here are generated deterministically based on solution type. "
        "They serve as a foundational starting point and should be thoroughly reviewed, edited, or expanded for your environment."
    )

    risk_lib = load_risk_library()

    # --- STEP 38: GENERATE RISKS FOR LOGGED USE CASES ---
    st.write("### ⚡ Generate Risk Records")
    if st.session_state.use_cases:
        use_case_names = [uc["name"] for uc in st.session_state.use_cases]
        selected_uc_name = st.selectbox("Select Use Case to Assess", options=use_case_names)

        # Find selected use case dict
        selected_uc = next((u for u in st.session_state.use_cases if u["name"] == selected_uc_name), None)

        if selected_uc:
            st.caption(f"**Solution Type:** {selected_uc['solution_type']} | **Owner:** {selected_uc['business_owner'] or 'Unassigned'}")

            if st.button(f"Generate Risk Templates for '{selected_uc_name}'", type="primary"):
                sol_type = selected_uc["solution_type"]
                templates = risk_lib.get(sol_type, risk_lib.get("Other", []))

                added_count = 0
                for tmpl in templates:
                    # Check if this risk already exists for this use case
                    exists = any(
                        r["use_case"] == selected_uc_name and r["source_template"] == tmpl["template_id"]
                        for r in st.session_state.risk_register
                    )
                    if not exists:
                        risk_count = len(st.session_state.risk_register) + 1
                        risk_id = f"RISK-{risk_count:03d}"
                        
                        l_val = tmpl["default_likelihood"]
                        i_val = tmpl["default_impact"]
                        r_score = calculate_risk_score(l_val, i_val)
                        severity = classify_risk(r_score)

                        new_risk = {
                            "risk_id": risk_id,
                            "use_case": selected_uc_name,
                            "category": tmpl["category"],
                            "description": tmpl["description"],
                            "likelihood": l_val,
                            "impact": i_val,
                            "risk_score": r_score,
                            "severity": severity,
                            "mitigation": tmpl["mitigation"],
                            "owner": selected_uc.get("business_owner", ""),
                            "status": "Open",
                            "review_date": str(datetime.date.today() + datetime.timedelta(days=30)),
                            "source_template": tmpl["template_id"],
                        }
                        st.session_state.risk_register.append(new_risk)
                        added_count += 1

                if added_count > 0:
                    st.success(f"Generated {added_count} risk record(s) for '{selected_uc_name}'!")
                    st.rerun()
                else:
                    st.warning("Risk records for this use case have already been generated.")
    else:
        st.warning("No use cases available. Please create at least one use case in '3. Use-Case Prioritization' first.")

    # --- STEP 40: RISK SUMMARY METRICS & AUDIT FLAGS ---
    if st.session_state.risk_register:
        st.write("---")
        st.write("## 📈 Risk Summary Dashboard")

        total_risks = len(st.session_state.risk_register)
        critical_risks = sum(1 for r in st.session_state.risk_register if r["severity"] == "Critical")
        high_risks = sum(1 for r in st.session_state.risk_register if r["severity"] == "High")
        unowned_risks = sum(1 for r in st.session_state.risk_register if not r["owner"].strip())
        unmitigated_risks = sum(1 for r in st.session_state.risk_register if not r["mitigation"].strip())

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Risks", total_risks)
        col2.metric("Critical Risks", critical_risks)
        col3.metric("High Risks", high_risks)
        col4.metric("Unowned Risks", unowned_risks, delta="-Missing Owner" if unowned_risks > 0 else "OK", delta_color="inverse")
        col5.metric("Unmitigated Risks", unmitigated_risks, delta="-Missing Plan" if unmitigated_risks > 0 else "OK", delta_color="inverse")

        # Category Chart
        st.write("### 📊 Risks by Category")
        cat_counts = {}
        for r in st.session_state.risk_register:
            c = r["category"]
            cat_counts[c] = cat_counts.get(c, 0) + 1
        
        df_risk_cat = pd.DataFrame({"Category": list(cat_counts.keys()), "Count": list(cat_counts.values())})
        st.bar_chart(df_risk_cat, x="Category", y="Count")

        # Table View
        st.write("### 📋 Active Risk Register Table")
        df_risk_table = pd.DataFrame(st.session_state.risk_register)
        st.dataframe(
            df_risk_table[["risk_id", "use_case", "category", "severity", "risk_score", "owner", "status", "review_date"]],
            use_container_width=True
        )

        # --- STEP 39: EDITABLE RISK RECORDS ---
        st.write("---")
        st.write("## 🛠️ Edit & Refine Risk Records")
        
        for idx, risk in enumerate(st.session_state.risk_register):
            with st.expander(f"{risk['risk_id']}: {risk['category']} ({risk['use_case']}) — [{risk['severity']} | Score: {risk['risk_score']}]"):
                with st.form(f"edit_risk_form_{risk['risk_id']}"):
                    st.write(f"**Template Ref:** `{risk['source_template']}`")
                    
                    new_desc = st.text_area("Risk Description", value=risk["description"])
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        new_l = st.slider("Likelihood (1-5)", min_value=1, max_value=5, value=int(risk["likelihood"]), key=f"l_{risk['risk_id']}")
                    with c2:
                        new_i = st.slider("Impact (1-5)", min_value=1, max_value=5, value=int(risk["impact"]), key=f"i_{risk['risk_id']}")

                    new_mit = st.text_area("Mitigation Controls", value=risk["mitigation"])
                    
                    c3, c4, c5 = st.columns(3)
                    with c3:
                        new_owner = st.text_input("Risk Owner", value=risk["owner"])
                    with c4:
                        new_status = st.selectbox(
                            "Status",
                            options=["Open", "Mitigation Planned", "In Progress", "Accepted", "Closed"],
                            index=["Open", "Mitigation Planned", "In Progress", "Accepted", "Closed"].index(risk["status"]) if risk["status"] in ["Open", "Mitigation Planned", "In Progress", "Accepted", "Closed"] else 0
                        )
                    with c5:
                        new_date = st.text_input("Review Date (YYYY-MM-DD)", value=risk["review_date"])

                    col_save, col_del = st.columns([1, 4])
                    save_btn = st.form_submit_button("Save Changes")

                    if save_btn:
                        calc_score = calculate_risk_score(new_l, new_i)
                        calc_sev = classify_risk(calc_score)

                        st.session_state.risk_register[idx].update({
                            "description": new_desc,
                            "likelihood": new_l,
                            "impact": new_i,
                            "risk_score": calc_score,
                            "severity": calc_sev,
                            "mitigation": new_mit,
                            "owner": new_owner,
                            "status": new_status,
                            "review_date": new_date,
                        })
                        st.success(f"Updated {risk['risk_id']} successfully!")
                        st.rerun()

                if st.button(f"🗑️ Delete {risk['risk_id']}", key=f"del_risk_{risk['risk_id']}"):
                    st.session_state.risk_register.pop(idx)
                    st.rerun()
# --- STEP 44, 49 & 50: EXECUTIVE SUMMARY WITH LLM & PROVENANCE ---
            st.write("---")
            st.write("## 📄 Executive Summary Report")

            org_name = st.session_state.org_profile.get("company_name", "Organization") if st.session_state.org_profile else "Organization"
            
            # Extract scores & gaps
            if st.session_state.readiness_results:
                ov_score = st.session_state.readiness_results.get("overall_score", 0.0)
                mat_level = st.session_state.readiness_results.get("maturity_level", "Unassessed")
                top_gaps = st.session_state.readiness_results.get("top_gaps", [])
            else:
                ov_score = 0.0
                mat_level = "Unassessed"
                top_gaps = []

            sorted_ucs = sorted(st.session_state.use_cases, key=lambda x: x["priority_score"], reverse=True)
            crit_count = sum(1 for r in st.session_state.risk_register if r["severity"] == "Critical")

            # Prepare sanitized payload for AI
            payload = prepare_llm_payload(
                org_profile=st.session_state.org_profile or {},
                readiness_results=st.session_state.readiness_results or {},
                use_cases=st.session_state.use_cases,
                risk_register=st.session_state.risk_register,
                roadmap_actions=custom_actions
            )

            # STEP 49: Graceful Fallback Execution
            ai_generated = False
            summary_data = None

            try:
                ai_output = generate_ai_summary(payload)
                summary_data = {
                    "current_state": ai_output.current_state,
                    "top_strengths": ai_output.top_strengths,
                    "key_gaps": ai_output.key_gaps,
                    "priority_use_cases": ai_output.priority_use_cases,
                    "immediate_actions": ai_output.immediate_actions,
                    "limitations": ai_output.limitations,
                }
                ai_generated = True
            except Exception:
                # Deterministic fallback if API fails or key missing
                summary_data = generate_deterministic_summary(
                    organization_name=org_name,
                    overall_score=ov_score,
                    maturity=mat_level,
                    gaps=top_gaps,
                    top_use_cases=sorted_ucs,
                    critical_risk_count=crit_count
                )
                st.warning("⚠️ AI-generated narrative is temporarily unavailable. A deterministic summary has been provided.")

            # STEP 50: Render Report with Provenance Labels
            if ai_generated:
                st.caption("🏷️ **Data Provenance:** *Narrative generated with AI (GPT-4o-mini)*")
            else:
                st.caption("🏷️ **Data Provenance:** *Calculated by deterministic scoring*")

            st.write("### 🏢 Current State & Maturity Profile")
            st.write(summary_data["current_state"])

            col_rep1, col_rep2 = st.columns(2)
            with col_rep1:
                st.write("### ⚠️ Key Operational Gaps")
                if summary_data.get("key_gaps"):
                    for gap in summary_data["key_gaps"]:
                        st.write(f"• {gap}")
                else:
                    st.write("• No major category gaps identified below baseline.")

            with col_rep2:
                st.write("### 🏆 Priority AI Use Cases")
                if summary_data.get("priority_use_cases"):
                    for idx, uc_n in enumerate(summary_data["priority_use_cases"]):
                        st.write(f"{idx+1}. {uc_n}")
                else:
                    st.write("• No priority use cases logged.")

            st.write("### 🎯 Immediate Executive Actions")
            if summary_data.get("immediate_actions"):
                for act in summary_data["immediate_actions"]:
                    st.write(f"✓ {act}")

            if summary_data.get("limitations"):
                st.write("### 📌 Assessment Limitations")
                for lim in summary_data["limitations"]:
                    st.write(f"ℹ️ {lim}")
elif section == "5. Roadmap and Report":
    st.title("90-Day Implementation Roadmap & Executive Report")
    st.write("Tailored operational execution path based on organizational readiness and risk posture.")

    if not st.session_state.use_cases:
        st.warning("No use cases available. Please log at least one use case in '3. Use-Case Prioritization' first.")
    else:
        use_case_names = [uc["name"] for uc in st.session_state.use_cases]
        selected_uc_name = st.selectbox("Select Use Case for Roadmap Generation", options=use_case_names)
        
        selected_uc = next((u for u in st.session_state.use_cases if u["name"] == selected_uc_name), None)

        if selected_uc:
            # 1. Base Roadmap
            base_roadmap = generate_roadmap(selected_uc_name)

            # 2. Extract readiness scores if available
            readiness_scores = {}
            if st.session_state.readiness_results:
                readiness_scores = st.session_state.readiness_results.get("category_scores", {})

            # 3. Determine highest risk severity for this use case
            uc_risks = [r for r in st.session_state.risk_register if r["use_case"] == selected_uc_name]
            severities = [r["severity"] for r in uc_risks]
            
            if "Critical" in severities:
                highest_severity = "Critical"
            elif "High" in severities:
                highest_severity = "High"
            elif "Medium" in severities:
                highest_severity = "Medium"
            elif "Low" in severities:
                highest_severity = "Low"
            else:
                highest_severity = "None"

            # 4. Generate conditional customized actions
            custom_actions = generate_conditional_actions(
                readiness_scores=readiness_scores,
                highest_risk_severity=highest_severity,
                selected_use_case=selected_uc
            )

            st.write("---")
            st.write(f"## 🗓️ 90-Day Action Plan: **{selected_uc_name}**")
            st.caption(f"**AI Solution Type:** {selected_uc['solution_type']} | **Owner:** {selected_uc['business_owner'] or 'Unassigned'}")

            # Display Conditional Adjustments first if triggered
            if custom_actions:
                st.write("### 🚨 Tailored Gap-Closure Actions")
                st.info("The following conditional actions were dynamically inserted into your roadmap based on identified readiness gaps and risk flags.")
                
                for idx, act in enumerate(custom_actions):
                    with st.expander(f"⚡ [{act['phase']}] {act['action']}"):
                        st.write(f"**Trigger:** `{act['trigger']}`")
                        st.write(f"**Rationale:** {act['rationale']}")
                        st.write(f"**Suggested Owner:** `{act['suggested_owner']}`")

            # Display 4-Phase Standard Roadmap
            st.write("---")
            st.write("### 🧭 Core 90-Day Milestones")
            
            for phase in base_roadmap["phases"]:
                st.write(f"#### {phase['phase_name']}")
                
                # Check for matching custom actions for this phase
                phase_actions = [a for a in custom_actions if a["phase"] in phase["phase_name"]]
                
                for m in phase["milestones"]:
                    st.write(f"  • {m}")
                    
                if phase_actions:
                    for pa in phase_actions:
                        st.warning(f"  👉 **REQUIRED ADJUSTMENT:** {pa['action']} *(Owner: {pa['suggested_owner']})*")
                st.write("")

           # --- EXECUTIVE SUMMARY REPORT ---
            st.write("---")
            st.write("## 📄 Executive Summary Report")

            org_profile = st.session_state.get("org_profile", {})
            org_name = org_profile.get("company_name", "Organization") if org_profile else "Organization"
            
            readiness_results = st.session_state.get("readiness_results", {})
            if readiness_results:
                ov_score = readiness_results.get("overall_score", 0.0)
                mat_level = readiness_results.get("maturity_level", "Unassessed")
                top_gaps = readiness_results.get("top_gaps", [])
            else:
                ov_score = 0.0
                mat_level = "Unassessed"
                top_gaps = []

            use_cases = st.session_state.get("use_cases", [])
            risk_register = st.session_state.get("risk_register", [])

            sorted_ucs = sorted(use_cases, key=lambda x: x.get("priority_score", 0), reverse=True)
            crit_count = sum(1 for r in risk_register if r.get("severity") == "Critical")

            # Prepare sanitized payload for AI
            payload = prepare_llm_payload(
                org_profile=org_profile,
                readiness_results=readiness_results,
                use_cases=use_cases,
                risk_register=risk_register,
                roadmap_actions=custom_actions
            )

            # Graceful Fallback Execution
            ai_generated = False
            summary_data = None

            try:
                ai_output = generate_ai_summary(payload)
                summary_data = {
                    "current_state": ai_output.current_state,
                    "top_strengths": ai_output.top_strengths,
                    "key_gaps": ai_output.key_gaps,
                    "priority_use_cases": ai_output.priority_use_cases,
                    "immediate_actions": ai_output.immediate_actions,
                    "limitations": ai_output.limitations,
                }
                ai_generated = True
            except Exception:
                summary_data = generate_deterministic_summary(
                    organization_name=org_name,
                    overall_score=ov_score,
                    maturity=mat_level,
                    gaps=top_gaps,
                    top_use_cases=sorted_ucs,
                    critical_risk_count=crit_count
                )
                st.warning("⚠️ AI-generated narrative is temporarily unavailable. A deterministic summary has been provided.")

            # Render Report with Provenance Labels
            if ai_generated:
                st.caption("🏷️ **Data Provenance:** *Narrative generated with AI (GPT-4o-mini)*")
            else:
                st.caption("🏷️ **Data Provenance:** *Calculated by deterministic scoring*")

            st.write("### 🏢 Current State & Maturity Profile")
            st.write(summary_data["current_state"])

            col_rep1, col_rep2 = st.columns(2)
            with col_rep1:
                st.write("### ⚠️ Key Operational Gaps")
                if summary_data.get("key_gaps"):
                    for gap in summary_data["key_gaps"]:
                        st.write(f"• {gap}")
                else:
                    st.write("• No major category gaps identified below baseline.")

            with col_rep2:
                st.write("### 🏆 Priority AI Use Cases")
                if summary_data.get("priority_use_cases"):
                    for idx, uc_n in enumerate(summary_data["priority_use_cases"]):
                        st.write(f"{idx+1}. {uc_n}")
                else:
                    st.write("• No priority use cases logged.")

            st.write("### 🎯 Immediate Executive Actions")
            if summary_data.get("immediate_actions"):
                for act in summary_data["immediate_actions"]:
                    st.write(f"✓ {act}")

            if summary_data.get("limitations"):
                st.write("### 📌 Assessment Limitations")
                for lim in summary_data["limitations"]:
                    st.write(f"ℹ️ {lim}")

            # --- EXPORT DOCX REPORT ---
            st.write("---")
            st.write("### 📥 Export Executive Report")

            report_data_payload = {
                "organization_name": org_name,
                "date": str(datetime.date.today()),
                "executive_summary": summary_data,
                "org_profile": org_profile,
                "readiness_results": readiness_results,
                "top_use_cases": sorted_ucs,
                "risk_register": risk_register,
                "roadmap_actions": custom_actions
            }

            docx_buffer = create_executive_report(report_data_payload)

            st.download_button(
                label="📄 Download Executive Readiness Report (.docx)",
                data=docx_buffer,
                file_name=f"{org_name.replace(' ', '_')}_AI_Readiness_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary"
            )