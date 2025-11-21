import streamlit as st
from utils.api import get_notes, create_note

workspace_id = st.session_state.get("workspace_id")

if not workspace_id:
    st.warning("Please select a workspace from the sidebar.")
    st.stop()


st.title("Notes")

with st.form("note_form"):
    st.subheader("Create Note")
    title = st.text_input("Title")
    content = st.text_area("Content")
    tags = st.text_input("Tags")

    if st.form_submit_button("Add"):
        create_note({
            "title": title,
            "content": content,
            "tags": tags.split(",") if tags else [],
            "workspace_id": workspace_id
        })
        st.success("Note added!")

st.markdown("---")
st.subheader("Your Notes")

for n in get_notes(workspace_id):
    st.write(f"### {n['title']}")
    st.caption(", ".join(n.get("tags", [])))
    st.write(n.get("content", ""))
    st.write("---")
