import streamlit as st
from utils.api import update_task

def kanban_board(tasks):
    statuses = {
        "to_do": "📝 To Do",
        "in_progress": "🚧 In Progress",
        "done": "✅ Done"
    }

    cols = st.columns(3)

    for i, (status, label) in enumerate(statuses.items()):
        with cols[i]:
            st.write(f"### {label}")
            for task in tasks:
                if task["status"] == status:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="padding:10px; border-radius:10px; border:1px solid #888;">
                                <b>{task['title']}</b><br>
                                <small>{task.get('description','')}</small><br>
                                <span style="color:gray">Priority: {task['priority']}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Move task button
                        if status != "done":
                            next_status = "in_progress" if status == "to_do" else "done"
                            if st.button(f"➡ Move to {statuses[next_status]}", key=f"mv-{task['_id']}"):
                                update_task(task["_id"], {"status": next_status})
                                st.rerun()
            st.write("---")
