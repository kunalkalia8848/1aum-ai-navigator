import streamlit as st

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
        "readiness_responses": [],
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
    
    # Step 20 Categories
    st.markdown("- **Strategy and Leadership**")
    st.markdown("- **Data Readiness**")
    st.markdown("- **Technology and Infrastructure**")
    st.markdown("- **Governance, Risk, and Security**")
    st.markdown("- **Talent and Operating Model**")
    st.markdown("- **Adoption and Change Management**")

elif section == "3. Use-Case Prioritization":
    st.title("Use-Case Prioritization")
    st.write("Prioritize and evaluate your AI initiatives.")

elif section == "4. Risk Register":
    st.title("Risk Register")
    st.write("Identify and analyze material AI risks.")

elif section == "5. Roadmap and Report":
    st.title("Roadmap and Report")
    st.write("Generate your practical 90-day execution plan.")