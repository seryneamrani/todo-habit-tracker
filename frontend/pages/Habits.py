import streamlit as st
from utils.api import create_habit, get_habits, check_habit

workspace_id = st.session_state.get("workspace_id")

if not workspace_id:
    st.warning("Please select a workspace from the sidebar.")
    st.stop()


st.title("Habit Tracker")

with st.form("habit_form"):
    st.subheader("Add Habit")
    name = st.text_input("Habit name")
    description = st.text_area("Description")
    if st.form_submit_button("Add"):
        create_habit({
            "name": name,
            "description": description,
            "workspace_id": workspace_id
        })
        st.success("Habit added!")

st.markdown("---")
st.subheader("Your Habits")

habits = get_habits(workspace_id)

for h in habits:
    st.write(f"### {h['name']}")
    if st.button(f"Mark done – {h['_id']}"):
        check_habit(h["_id"])
        st.rerun()
    st.write("---")
