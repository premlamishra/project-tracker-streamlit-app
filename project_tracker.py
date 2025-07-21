import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from openpyxl import load_workbook

#functions
def load_data():
    return pd.read_excel("projects.xlsx")

def save_data(df):
    df.to_excel("projects.xlsx", index=False)

def add_project(name, owner, status, start_date, end_date, deadline):
    df = load_data()
    today = datetime.today().strftime('%Y-%m-%d')
    new_row = {
        'Project Name': name,
        'Owner': owner,
        'Status': status,
        'Start Date': start_date,
        'End Date': end_date,
        'Deadline': deadline,
        'Last Updated': today
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    st.success("✅ Project added successfully!")

def update_status(project_name, new_status):
    df = load_data()
    today = datetime.today().strftime('%Y-%m-%d')
    mask = df['Project Name'] == project_name
    if mask.any():
        df.loc[mask, 'Status'] = new_status
        df.loc[mask, 'Last Updated'] = today
        save_data(df)
        st.success("✅ Status updated!")
    else:
        st.warning("❗Project not found.")

def delete_project(project_name):
    df = load_data()
    mask = df['Project Name'] == project_name
    if mask.any():
        df = df[~mask]
        save_data(df)
        st.success("🗑️ Project deleted successfully!")
    else:
        st.warning("❗Project not found.")

#streamlit app layout
st.set_page_config(page_title="Project Tracker", layout="wide")
st.title("Internal Project Tracker")

menu = ["📋 View Projects", "➕ Add Project", "📝 Update Status", "🗑️ Delete Project", "📈 Analytics"]
choice = st.sidebar.radio("Navigate", menu)

#add project
if choice == "➕ Add Project":
    st.subheader("Add New Project")
    name = st.text_input("Project Name")
    owner = st.text_input("Owner")
    status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    deadline = st.date_input("Deadline")
    
    if st.button("Add Project"):
        if name and owner:
            add_project(name, owner, status, start_date, end_date, deadline)
        else:
            st.error("Please fill all fields.")

#view project
elif choice == "📋 View Projects":
    st.subheader("All Projects")
    df = load_data()

    # Filters
    owner_filter = st.sidebar.selectbox("Filter by Owner", ["All"] + sorted(df['Owner'].dropna().unique().tolist()))
    status_filter = st.sidebar.selectbox("Filter by Status", ["All", "Not Started", "In Progress", "Completed"])
    
    if owner_filter != "All":
        df = df[df["Owner"] == owner_filter]
    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    # Deadline status
    df["Deadline"] = pd.to_datetime(df["Deadline"])
    today = pd.to_datetime("today")
    df["Days Left"] = (df["Deadline"] - today).dt.days

    def highlight_deadline(row):
        if row["Days Left"] < 0:
            return ['background-color: #4caf50'] * len(row)
        elif row["Days Left"] <= 3:
            return ['background-color: #fff3cd'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(df.style.apply(highlight_deadline, axis=1), use_container_width=True)

#update status
elif choice == "📝 Update Status":
    st.subheader("Update Project Status")
    df = load_data()
    project_names = df['Project Name'].tolist()
    
    selected_project = st.selectbox("Select Project", project_names)
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"])
    
    if st.button("Update"):
        update_status(selected_project, new_status)

#delete project
elif choice == "🗑️ Delete Project":
    st.subheader("Delete a Project")
    df = load_data()
    project_names = df['Project Name'].tolist()
    
    if project_names:
        selected_project = st.selectbox("Select Project to Delete", project_names)
        confirm = st.checkbox("Are you sure you want to delete this project?")
        
        if st.button("Delete") and confirm:
            delete_project(selected_project)
    else:
        st.info("No projects available to delete.")

#analytics
elif choice == "📈 Analytics":
    st.subheader("Project Status Analytics")
    df = load_data()

    status_counts = df["Status"].value_counts()
    st.write("### Status Count")
    st.bar_chart(status_counts)

    st.write("### Pie Chart of Status")
    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

    df["Deadline"] = pd.to_datetime(df["Deadline"])
    df["Week"] = df["Deadline"].dt.to_period("W").astype(str)
    weekly_due = df["Week"].value_counts().sort_index()

    st.write("### Projects Due per Week")
    fig2, ax2 = plt.subplots()
    ax2.plot(weekly_due.index, weekly_due.values, marker='o')
    ax2.set_title("Deadlines by Week")
    ax2.set_xlabel("Week")
    ax2.set_ylabel("Number of Projects")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.write("### 📅 Gantt Chart of Projects")
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])

    fig3 = px.timeline(
        df,
        x_start="Start Date",
        x_end="End Date",
        y="Project Name",
        color="Status",
        title="Project Timeline (Gantt Chart)"
    )
    fig3.update_yaxes(autorange="reversed")
    st.plotly_chart(fig3, use_container_width=True)

