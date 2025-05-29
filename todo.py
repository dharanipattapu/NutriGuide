import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os

TASK_FILE = "user_tasks.yaml"

# ───────────────────────────────────────────────────
# Load tasks for a specific user from the YAML file
# ───────────────────────────────────────────────────
def load_tasks(username):
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as file:
        data = yaml.load(file, Loader=SafeLoader) or {}
        return data.get(username, [])

# ───────────────────────────────────────────────────
# Save tasks for a specific user to the YAML file
# ───────────────────────────────────────────────────
def save_tasks(username, tasks):
    try:
        with open(TASK_FILE, "r") as file:
            data = yaml.load(file, Loader=SafeLoader) or {}
    except FileNotFoundError:
        data = {}

    data[username] = tasks
    with open(TASK_FILE, "w") as file:
        yaml.dump(data, file)

# ───────────────────────────────────────────────────
# Main To-Do Page logic for each authenticated user
# ───────────────────────────────────────────────────
def todo_page(username):
    st.title("📝 To-Do List")
    st.markdown(f"**Logged in as:** `{username}`")

    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks(username)

    # ─ Add new task
    new_task = st.text_input("Add a new task:")
    if st.button("➕ Add Task") and new_task:
        st.session_state.tasks.append({"task": new_task, "done": False})
        save_tasks(username, st.session_state.tasks)
        st.rerun()

    # ─ Show task list
    if st.session_state.tasks:
        st.subheader("📋 Your Tasks")

    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.7, 0.2, 0.1])
        with col1:
            st.session_state.tasks[i]["done"] = st.checkbox(
                label=task["task"],
                value=task["done"],
                key=f"{username}_checkbox_{i}"
            )
        with col2:
            st.write("✅" if task["done"] else "🕒")
        with col3:
            if st.button("❌", key=f"{username}_delete_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(username, st.session_state.tasks)
                st.rerun()

    # Save updates
    save_tasks(username, st.session_state.tasks)
