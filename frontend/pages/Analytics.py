import streamlit as st
from utils.api import get_analytics
import pandas as pd

workspace_id = st.session_state.get("workspace_id")

if not workspace_id:
    st.warning("Please select a workspace from the sidebar.")
    st.stop()

st.title("Analytics Dashboard")

data = get_analytics()

st.subheader("Tasks")
st.json(data["tasks"])

st.subheader("Habits")
st.json(data["habits"])

st.subheader("Notes")
st.json(data["notes"])

st.subheader("Workspaces Overview")
df = pd.DataFrame(data["workspaces"]["workspaces"])
st.dataframe(df)
