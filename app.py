import streamlit as st
import json
import os
import pandas as pd

# Import the scoring functions and the new recommendations map
from modules.readiness import calculate_readiness_scores, maturity_level, identify_top_gaps, GAP_RECOMMENDATIONS

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
        # Group questions by category
        categories = {}
        for q in questions:
            cat = q["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q)
            
        # Display questions dynamically
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
        
        # Submit button to calculate and display metrics
        if st.button("Submit Assessment", type="primary"):
            responses_list = list(st.session_state.readiness_responses.values())
            
            if responses_list:
                scores_data = calculate_readiness_scores(responses_list)
                st.session_state.readiness_results = scores_data
                st.success("Assessment calculated and saved successfully!")
            else:
                st.error("Please answer the questions before submitting.")
                
        # Display Results Section if they exist in state (persists across navigation)
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
                # Fetch explicit deterministic recommendation if defined, otherwise use a fallback
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

    # Step 27 Form Intake Fields
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
        st.write("### Step 28: Prioritization Scoring (1-5 Scale)")
        
        # 1-5 Scoring Inputs with explicit directions
        business_impact = st.slider("Business Impact (5 = Favorable/Highest Impact)", min_value=1, max_value=5, value=3)
        strategic_alignment = st.slider("Strategic Alignment (5 = Favorable/Perfect Alignment)", min_value=1, max_value=5, value=3)
        technical_feasibility = st.slider("Technical Feasibility (5 = Favorable/Easiest to Build)", min_value=1, max_value=5, value=3)
        data_readiness_score = st.slider("Data Readiness (5 = Favorable/Highly Ready Data)", min_value=1, max_value=5, value=3)
        risk_score = st.slider("Risk (5 = High Risk, 1 = Low Risk)", min_value=1, max_value=5, value=1)
        
        submit_uc = st.form_submit_button("Add Use Case")
        
        if submit_uc:
            if uc_name:
                new_use_case = {
                    "name": uc_name,
                    "business_problem": business_problem,
                    "business_owner": business_owner,
                    "intended_users": intended_users,
                    "business_benefit": business_benefit,
                    "required_data": required_data,
                    "solution_type": solution_type,
                    "regulatory_sensitivity": regulatory_sensitivity,
                    "implementation_assumptions": implementation_assumptions,
                    # Step 28 scores saved here
                    "scores": {
                        "business_impact": business_impact,
                        "strategic_alignment": strategic_alignment,
                        "technical_feasibility": technical_feasibility,
                        "data_readiness": data_readiness_score,
                        "risk": risk_score
                    }
                }
                st.session_state.use_cases.append(new_use_case)
                st.success(f"Use case '{uc_name}' added and evaluated successfully!")
            else:
                st.error("Please provide a Use-case name.")

    # Display currently added use cases if any exist
    if st.session_state.use_cases:
        st.write("---")
        st.write("### Logged Use Cases")
        for idx, uc in enumerate(st.session_state.use_cases):
            with st.expander(f"{idx + 1}. {uc['name']} ({uc['solution_type']})"):
                st.write(f"**Business Owner/Function:** {uc['business_owner']}")
                st.write(f"**Business Problem:** {uc['business_problem']}")
                
                # Render the evaluation summary
                st.write("**Prioritization Metrics:**")
                sc = uc["scores"]
                st.text(f"  • Business Impact: {sc['business_impact']}/5 | Strategic Alignment: {sc['strategic_alignment']}/5")
                st.text(f"  • Technical Feasibility: {sc['technical_feasibility']}/5 | Data Readiness: {sc['data_readiness']}/5")
                st.text(f"  • Risk Profile: {sc['risk']}/5 (Note: 5 indicates high risk)")