import streamlit as st
from utils.api import get_workspaces, create_workspace

def workspace_sidebar():
    st.sidebar.title("📁 Workspaces")

    workspaces = get_workspaces()

    # Transform list → dict
    workspace_names = {w["name"]: w["_id"] for w in workspaces} if workspaces else {}

    # Case 1: No workspace exists → force creation first
    if not workspace_names:
        st.sidebar.warning("No workspaces found. Create one below to continue.")

        with st.sidebar.form("create_first_workspace"):
            name = st.text_input("Workspace name")
            description = st.text_area("Description")
            color = st.color_picker("Color", "#4CAF50")

            if st.form_submit_button("Create Workspace"):
                create_workspace(name, description, color)
                st.sidebar.success("Workspace created!")
                st.rerun()

        return  # stop here: don't try to set workspace_id

    # Case 2: Workspaces exist → show selector
    selected = st.sidebar.selectbox(
        "Select workspace",
        list(workspace_names.keys()),
        key="ws_selector"
    )

    # Save the workspace ID safely
    if selected:
        st.session_state["workspace_id"] = workspace_names[selected]

    # Navigation section
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Navigation")
    st.sidebar.page_link("pages/Workspaces.py", label="Workspaces")
    st.sidebar.page_link("pages/Tasks.py", label="Tasks")
    st.sidebar.page_link("pages/Habits.py", label="Habits")
    st.sidebar.page_link("pages/Notes.py", label="Notes")
    st.sidebar.page_link("pages/Analytics.py", label="Analytics")
