import streamlit as st
import json
import os
import pandas as pd

# Import backend modules
from modules.readiness import calculate_readiness_scores, maturity_level, identify_top_gaps, GAP_RECOMMENDATIONS
from modules.prioritization import (
    calculate_priority_score, 
    classify_use_case, 
    explain_recommendation,
    normalize_name
)

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
    st.write("Identify and analyze material AI risks.")

elif section == "5. Roadmap and Report":
    st.title("Roadmap and Report")
    st.write("Generate your practical 90-day execution plan.")