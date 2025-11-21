import streamlit as st
from utils.api import get_tasks, create_task, update_task
from components.kanban import kanban_board

workspace_id = st.session_state.get("workspace_id")

if not workspace_id:
    st.warning("Please select a workspace from the sidebar.")
    st.stop()

st.title("Tasks")

with st.form("create_task"):
    st.subheader("Add Task")
    title = st.text_input("Title")
    description = st.text_area("Description")
    priority = st.selectbox("Priority", ["low", "medium", "high"])
    status = "to_do"
    tags = st.text_input("Tags (comma sep)")
    deadline = st.date_input("Deadline")
    
    if st.form_submit_button("Add"):
        create_task({
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "tags": tags.split(",") if tags else [],
            "deadline": str(deadline),
            "workspace_id": workspace_id
        })
        st.success("Task added!")

st.markdown("---")
st.subheader("Kanban Board")

tasks = get_tasks(workspace_id)
kanban_board(tasks)


cols = st.columns(3)
statuses = ["to_do", "in_progress", "done"]
labels = ["📝 To Do", "🚧 In Progress", "✅ Done"]

for col, status, label in zip(cols, statuses, labels):
    with col:
        st.write(f"### {label}")
        for t in tasks:
            if t["status"] == status:
                st.write(f"**{t['title']}**")
                if st.button(f"Move to next – {t['_id']}", key=t['_id']):
                    new_status = "in_progress" if status == "to_do" else "done"
                    update_task(t["_id"], {"status": new_status})
                    st.rerun()



