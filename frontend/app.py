import streamlit as st
from components.sidebar import workspace_sidebar

# Must be called FIRST before any page logic
st.set_page_config(page_title="Productivity App", layout="wide")

# Load the sidebar (workspace selector + navigation)
workspace_sidebar()

st.title("📌 Productivity Dashboard")

# Retrieve selected workspace
workspace_id = st.session_state.get("workspace_id")

# If no workspace selected, stop page execution
if not workspace_id:
    st.info("👈 Please select a workspace from the left sidebar.")
    st.stop()

# Optional: Show current workspace
st.write(f"Current workspace ID: **{workspace_id}**")

st.success("Welcome to your Productivity App 🎉")
