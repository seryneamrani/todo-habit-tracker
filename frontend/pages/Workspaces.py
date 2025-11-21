import streamlit as st
from utils.api import get_workspaces, create_workspace

workspace_id = st.session_state.get("workspace_id")


st.title("Manage Workspaces")


name = st.text_input("Workspace name")
description = st.text_area("Description")
color = st.color_picker("Color", "#4CAF50")

if st.button("Create Workspace"):
    res = create_workspace(name, description, color)
    st.success("Workspace created!")

st.markdown("---")

st.subheader("Existing Workspaces")
for w in get_workspaces():
    st.write(f"### {w['name']} – 🔵 {w.get('color')}")
    st.caption(w.get("description"))
    st.write("---")
