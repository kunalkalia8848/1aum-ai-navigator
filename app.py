import streamlit as st
import json
import os

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
        # Group questions by their category
        categories = {}
        for q in questions:
            cat = q["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q)
            
        # Display the categories and questions dynamically
        for cat, q_list in categories.items():
            with st.expander(cat, expanded=True):
                for q in q_list:
                    # Creating a unique key for each question using its ID
                    st.radio(
                        q["question"],
                        options=["1 - Initial / Ad-hoc", "2 - Repeatable", "3 - Defined", "4 - Managed", "5 - Optimized"],
                        key=f"q_{q['id']}"
                    )
    else:
        st.error("Could not load readiness questions from data folder.")

elif section == "3. Use-Case Prioritization":
    st.title("Use-Case Prioritization")
    st.write("Prioritize and evaluate your AI initiatives.")

elif section == "4. Risk Register":
    st.title("Risk Register")
    st.write("Identify and analyze material AI risks.")

elif section == "5. Roadmap and Report":
    st.title("Roadmap and Report")
    st.write("Generate your practical 90-day execution plan.")