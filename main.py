import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Business Launch Timeline",
    page_icon="📅",
    layout="wide",
)

# ============================================================
# INITIAL DATA
# ============================================================

INITIAL_TASKS = [
    {
        "Task": "Finish VIP app",
        "Owner": "Cintia",
        "Start": date(2026, 9, 17),
        "End": date(2026, 9, 30),
        "Status": "In progress",
        "Category": "Technical",
        "Notes": "Hard deadline: end of September.",
    },
    {
        "Task": "Decide on business idea",
        "Owner": "Both",
        "Start": date(2026, 9, 17),
        "End": date(2026, 10, 1),
        "Status": "In progress",
        "Category": "Business",
        "Notes": "Select the idea to pursue and define ICP, problem and initial offer.",
    },
    {
        "Task": "Market validation",
        "Owner": "Both",
        "Start": date(2026, 9, 20),
        "End": date(2026, 10, 1),
        "Status": "Not started",
        "Category": "Business",
        "Notes": "Customer interviews, problem validation and willingness-to-pay.",
    },
    {
        "Task": "Define MVP + first sellable offer",
        "Owner": "Both",
        "Start": date(2026, 9, 25),
        "End": date(2026, 10, 5),
        "Status": "Not started",
        "Category": "Launch",
        "Notes": "Turn the validated idea into a narrow product that can actually be sold.",
    },
    {
        "Task": "Build business MVP",
        "Owner": "Both",
        "Start": date(2026, 10, 1),
        "End": date(2026, 11, 15),
        "Status": "Not started",
        "Category": "Launch",
        "Notes": "Build the smallest version capable of delivering the promised outcome.",
    },
    {
        "Task": "Start marketing + outreach",
        "Owner": "Both",
        "Start": date(2026, 10, 1),
        "End": date(2026, 12, 31),
        "Status": "Not started",
        "Category": "Launch",
        "Notes": "Start before the product is perfect. Generate leads and customer conversations.",
    },
    {
        "Task": "Get first paying customers",
        "Owner": "Both",
        "Start": date(2026, 11, 1),
        "End": date(2026, 12, 31),
        "Status": "Not started",
        "Category": "Launch",
        "Notes": "December target: actual revenue from the business.",
    },
    {
        "Task": "Graph DB",
        "Owner": "Cintia",
        "Start": date(2026, 9, 17),
        "End": date(2026, 12, 31),
        "Status": "In progress",
        "Category": "Technical",
        "Notes": "Build the graph database required for the RAG system.",
    },
    {
        "Task": "RAG artifacts",
        "Owner": "Cintia",
        "Start": date(2026, 9, 17),
        "End": date(2026, 12, 31),
        "Status": "In progress",
        "Category": "Technical",
        "Notes": "Finish the artifacts/data structures required by the RAG system.",
    },
    {
        "Task": "Ingestion pipeline",
        "Owner": "Pali",
        "Start": date(2026, 9, 17),
        "End": date(2026, 12, 31),
        "Status": "In progress",
        "Category": "Technical",
        "Notes": "Complete ingestion pipeline.",
    },
    {
        "Task": "Vector DB",
        "Owner": "Pali",
        "Start": date(2026, 9, 17),
        "End": date(2026, 12, 31),
        "Status": "In progress",
        "Category": "Technical",
        "Notes": "Complete vector database component.",
    },
    {
        "Task": "RAG system",
        "Owner": "Both",
        "Start": date(2027, 1, 1),
        "End": date(2027, 2, 28),
        "Status": "Not started",
        "Category": "Technical",
        "Notes": "Joint work. Break into specific tasks later.",
    },
    {
        "Task": "Business revenue validation",
        "Owner": "Both",
        "Start": date(2027, 1, 1),
        "End": date(2027, 2, 28),
        "Status": "Not started",
        "Category": "Business",
        "Notes": "Establish whether revenue is repeatable enough to support leaving Lenovo.",
    },
    {
        "Task": "Lenovo exit decision",
        "Owner": "Both",
        "Start": date(2027, 2, 1),
        "End": date(2027, 3, 15),
        "Status": "Not started",
        "Category": "Career",
        "Notes": "Target window around March, contingent on business/revenue situation.",
    },
]


# ============================================================
# STATE
# ============================================================

if "tasks" not in st.session_state:
    st.session_state.tasks = pd.DataFrame(INITIAL_TASKS)

if "editing_task" not in st.session_state:
    st.session_state.editing_task = None


# ============================================================
# HELPERS
# ============================================================

def save_tasks():
    """Save tasks locally."""
    st.session_state.tasks.to_csv("tasks.csv", index=False)


def load_tasks():
    """Load tasks if a local CSV exists."""
    try:
        df = pd.read_csv("tasks.csv")
        df["Start"] = pd.to_datetime(df["Start"]).dt.date
        df["End"] = pd.to_datetime(df["End"]).dt.date
        return df
    except FileNotFoundError:
        return pd.DataFrame(INITIAL_TASKS)


def status_icon(status):
    return {
        "Done": "●",
        "In progress": "◐",
        "At risk": "!",
        "Not started": "○",
    }.get(status, "○")


# ============================================================
# HEADER
# ============================================================

st.title("Business Launch Timeline")

st.caption(
    "September 2026 → March 2027 | "
    "Technical foundation + business launch + Lenovo exit target"
)

st.divider()


# ============================================================
# TOP METRICS
# ============================================================

tasks = st.session_state.tasks

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total tasks",
        len(tasks),
    )

with col2:
    st.metric(
        "Completed",
        len(tasks[tasks["Status"] == "Done"]),
    )

with col3:
    st.metric(
        "In progress",
        len(tasks[tasks["Status"] == "In progress"]),
    )

with col4:
    st.metric(
        "December launch",
        "TARGET",
    )


# ============================================================
# TABS
# ============================================================

tab_timeline, tab_tasks, tab_add = st.tabs(
    ["Timeline", "Edit tasks", "Add task"]
)


# ============================================================
# TIMELINE
# ============================================================

with tab_timeline:

    st.subheader("Master timeline")

    # Filter
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        owner_filter = st.multiselect(
            "Owner",
            options=sorted(tasks["Owner"].unique()),
            default=sorted(tasks["Owner"].unique()),
        )

    with filter_col2:
        category_filter = st.multiselect(
            "Category",
            options=sorted(tasks["Category"].unique()),
            default=sorted(tasks["Category"].unique()),
        )

    filtered = tasks[
        tasks["Owner"].isin(owner_filter)
        & tasks["Category"].isin(category_filter)
    ].copy()

    # --------------------------------------------------------
    # GANTT
    # --------------------------------------------------------

    if not filtered.empty:

        gantt = filtered[
            ["Task", "Start", "End", "Category", "Owner", "Status"]
        ].copy()

        gantt["Start"] = pd.to_datetime(gantt["Start"])
        gantt["End"] = pd.to_datetime(gantt["End"])

        gantt = gantt.set_index("Task")

        st.bar_chart(
            gantt,
            x="Start",
            y="End",
            horizontal=True,
        )

        st.caption(
            "Use the task table below for exact dates and editing. "
            "The timeline is the visual overview."
        )

    # --------------------------------------------------------
    # MONTHLY VIEW
    # --------------------------------------------------------

    st.subheader("Monthly execution plan")

    months = [
        ("September 2026", date(2026, 9, 1), date(2026, 9, 30)),
        ("October 2026", date(2026, 10, 1), date(2026, 10, 31)),
        ("November 2026", date(2026, 11, 1), date(2026, 11, 30)),
        ("December 2026", date(2026, 12, 1), date(2026, 12, 31)),
        ("January 2027", date(2027, 1, 1), date(2027, 1, 31)),
        ("February 2027", date(2027, 2, 1), date(2027, 2, 28)),
        ("March 2027", date(2027, 3, 1), date(2027, 3, 31)),
    ]

    for month_name, month_start, month_end in months:

        month_tasks = filtered[
            (filtered["Start"] <= month_end)
            & (filtered["End"] >= month_start)
        ].copy()

        if month_tasks.empty:
            continue

        with st.expander(
            f"{month_name}  ·  {len(month_tasks)} tasks",
            expanded=month_name in ["September 2026", "October 2026"],
        ):

            for _, task in month_tasks.sort_values("Start").iterrows():

                st.markdown(
                    f"""
                    **{status_icon(task['Status'])} {task['Task']}**

                    `{task['Owner']}` · `{task['Category']}` ·
                    `{task['Status']}`

                    {task['Start']} → {task['End']}

                    {task['Notes']}
                    """
                )

                st.divider()


# ============================================================
# EDIT TASKS
# ============================================================

with tab_tasks:

    st.subheader("Edit existing tasks")

    if tasks.empty:
        st.info("No tasks yet.")
    else:

        for index, task in tasks.iterrows():

            with st.expander(
                f"{status_icon(task['Status'])} {task['Task']} "
                f"— {task['Owner']}"
            ):

                col1, col2 = st.columns(2)

                with col1:
                    new_name = st.text_input(
                        "Task",
                        value=task["Task"],
                        key=f"name_{index}",
                    )

                    new_owner = st.selectbox(
                        "Owner",
                        ["Cintia", "Pali", "Both"],
                        index=["Cintia", "Pali", "Both"].index(task["Owner"]),
                        key=f"owner_{index}",
                    )

                    new_category = st.selectbox(
                        "Category",
                        ["Business", "Technical", "Launch", "Career"],
                        index=[
                            "Business",
                            "Technical",
                            "Launch",
                            "Career",
                        ].index(task["Category"]),
                        key=f"category_{index}",
                    )

                with col2:
                    new_start = st.date_input(
                        "Start",
                        value=task["Start"],
                        key=f"start_{index}",
                    )

                    new_end = st.date_input(
                        "End",
                        value=task["End"],
                        key=f"end_{index}",
                    )

                    new_status = st.selectbox(
                        "Status",
                        [
                            "Not started",
                            "In progress",
                            "Done",
                            "At risk",
                        ],
                        index=[
                            "Not started",
                            "In progress",
                            "Done",
                            "At risk",
                        ].index(task["Status"]),
                        key=f"status_{index}",
                    )

                new_notes = st.text_area(
                    "Notes",
                    value=task["Notes"],
                    key=f"notes_{index}",
                )

                save_col, delete_col = st.columns(2)

                with save_col:
                    if st.button(
                        "Save changes",
                        key=f"save_{index}",
                        type="primary",
                    ):

                        if new_end < new_start:
                            st.error("End date cannot be before start date.")
                        else:
                            tasks.loc[index, "Task"] = new_name
                            tasks.loc[index, "Owner"] = new_owner
                            tasks.loc[index, "Category"] = new_category
                            tasks.loc[index, "Start"] = new_start
                            tasks.loc[index, "End"] = new_end
                            tasks.loc[index, "Status"] = new_status
                            tasks.loc[index, "Notes"] = new_notes

                            st.session_state.tasks = tasks
                            save_tasks()

                            st.success("Task updated.")
                            st.rerun()

                with delete_col:
                    if st.button(
                        "Delete task",
                        key=f"delete_{index}",
                    ):
                        tasks = tasks.drop(index).reset_index(drop=True)
                        st.session_state.tasks = tasks
                        save_tasks()

                        st.success("Task deleted.")
                        st.rerun()


# ============================================================
# ADD TASK
# ============================================================

with tab_add:

    st.subheader("Add a task")

    with st.form("add_task_form"):

        task_name = st.text_input(
            "Task name",
            placeholder="e.g. Customer interviews",
        )

        col1, col2 = st.columns(2)

        with col1:
            owner = st.selectbox(
                "Owner",
                ["Cintia", "Pali", "Both"],
            )

            category = st.selectbox(
                "Category",
                ["Business", "Technical", "Launch", "Career"],
            )

            status = st.selectbox(
                "Status",
                [
                    "Not started",
                    "In progress",
                    "Done",
                    "At risk",
                ],
            )

        with col2:
            start = st.date_input(
                "Start",
                value=date.today(),
            )

            end = st.date_input(
                "End",
                value=date.today(),
            )

        notes = st.text_area(
            "Notes",
            placeholder="What does this task actually involve?",
        )

        submitted = st.form_submit_button(
            "Add task",
            type="primary",
        )

        if submitted:

            if not task_name.strip():
                st.error("Task name is required.")

            elif end < start:
                st.error("End date cannot be before start date.")

            else:

                new_task = {
                    "Task": task_name.strip(),
                    "Owner": owner,
                    "Start": start,
                    "End": end,
                    "Status": status,
                    "Category": category,
                    "Notes": notes,
                }

                st.session_state.tasks = pd.concat(
                    [
                        st.session_state.tasks,
                        pd.DataFrame([new_task]),
                    ],
                    ignore_index=True,
                )

                save_tasks()

                st.success("Task added.")
                st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Local persistence: tasks.csv. "
    "Cintia can edit dates, owners, status, categories and notes at any time."
)
