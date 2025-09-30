import streamlit as st
from datetime import datetime


st.set_page_config(page_title="To-Do List App", page_icon="📝", layout="wide")


st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .title {
        font-size: 42px; 
        color: #4CAF50; 
        font-weight: bold;
        text-align: center;
    }
    .task-box {
        background: linear-gradient(90deg, #ffdde1, #ee9ca7);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        color: #2c2c2c;
        font-weight: 500;
    }
    .completed-task {
        text-decoration: line-through;
        color: grey;
    }
    .overdue {
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


if "tasks" not in st.session_state:
    st.session_state.tasks = []  
if "username" not in st.session_state:
    st.session_state.username = ""
if "deadline_date" not in st.session_state:
    st.session_state.deadline_date = datetime.now().date()
if "deadline_time" not in st.session_state:
    st.session_state.deadline_time = datetime.now().time()
if "task_input" not in st.session_state:
    st.session_state.task_input = ""

def add_task():
    task = st.session_state.task_input.strip()
    if task:
        deadline = datetime.combine(st.session_state.deadline_date, st.session_state.deadline_time)
        st.session_state.tasks.append({
            "task": task,
            "done": False,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": deadline.strftime("%Y-%m-%d %H:%M")
        })
        st.session_state.task_input = ""

if st.session_state.username == "":
    st.markdown("<div class='title'>📝 Advanced To-Do List</div>", unsafe_allow_html=True)
    st.subheader("👋 Welcome! Please enter your name to continue:")
    name_input = st.text_input("Your Name")
    if st.button("Start"):
        if name_input.strip() != "":
            st.session_state.username = name_input.strip().title()
            st.rerun()
        else:
            st.warning("⚠️ Please enter a valid name")
else:
    st.markdown(f"<div class='title'> Welcome, {st.session_state.username}! 🎉</div>", unsafe_allow_html=True)
    st.write("Manage your tasks with an attractive and colorful interface!")

    st.sidebar.header("➕ Add New Task")
    st.sidebar.text_input("Enter a task", key="task_input", on_change=add_task)
    st.session_state.deadline_date = st.sidebar.date_input("Deadline Date", value=st.session_state.deadline_date)
    st.session_state.deadline_time = st.sidebar.time_input("Deadline Time", value=st.session_state.deadline_time)

    if st.sidebar.button("Add Task"):
        add_task()
        st.sidebar.success("✅ Task added!")
        st.rerun()

    st.subheader("📋 Your Tasks")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks yet! Add tasks from the left panel.")
    else:
        for i, t in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([6, 1, 1])

            deadline_dt = datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M")
            overdue = (not t["done"]) and (deadline_dt < datetime.now())

            with col1:
                if t["done"]:
                    st.markdown(
                        f"<div class='task-box'><span class='completed-task'>{t['task']}</span><br>"
                        f"<small>Added: {t['time']} | Deadline: {t['deadline']}</small></div>",
                        unsafe_allow_html=True
                    )
                elif overdue:
                    st.markdown(
                        f"<div class='task-box'><span class='overdue'>{t['task']}</span><br>"
                        f"<small>Added: {t['time']} | Deadline: {t['deadline']} ⚠️ Overdue!</small></div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div class='task-box'>{t['task']}<br>"
                        f"<small>Added: {t['time']} | Deadline: {t['deadline']}</small></div>",
                        unsafe_allow_html=True
                    )

            with col2:
                if not t["done"]:
                    if st.button("✅", key=f"done{i}"):
                        st.session_state.tasks[i]["done"] = True
                        st.rerun()
            with col3:
                if st.button("🗑️", key=f"del{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

    st.sidebar.markdown("---")
    if st.sidebar.button("🧹 Clear All Tasks"):
        st.session_state.tasks.clear()
        st.sidebar.success("All tasks cleared!")
        st.rerun()
