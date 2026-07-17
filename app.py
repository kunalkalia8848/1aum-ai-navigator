import streamlit as st

st.set_page_config(
    page_title="1AUM Navigator",
    page_icon="🧭",
    layout="wide",
)

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
