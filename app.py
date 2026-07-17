import streamlit as st

# 1. Page Configuration (This sets up the browser tab)
st.set_page_config(
    page_title="1AUM Navigator",
    page_icon="🧭",
    layout="wide",
)

# 2. Initialize Session State (This sets up the temporary data notebook)
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

# This runs the notebook setup right away
initialize_session_state()


# 3. UI Layout (This draws the text on the screen)
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