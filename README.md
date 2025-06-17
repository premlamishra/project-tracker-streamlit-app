# Internal Project Tracker

This is a Streamlit web app to manage internal project statuses and deadlines. It allows individuals or small teams to track project progress, update information, and visualize status using charts, all stored in a local Excel file.

## Features
-  View and highlight projects with color-coded statuses
-  Add new projects with deadline and owner details
-  Update project status, owner, or deadline
-  Delete projects when completed or no longer needed
-  Dashboard with a pie chart of project statuses
-  Data saved to and loaded from `projects.xlsx` using Excel integration

## Tech Stack
- Python
- Streamlit
- Pandas
- OpenPyXL
- Matplotlib

## How to Run

1. Clone the repository
bash
git clone https://github.com/your-username/project-tracker-app.git
cd project-tracker-app

2. Install the required libraries
pip install streamlit pandas openpyxl matplotlib

3. Run the Streamlit app
bash
streamlit run project_tracker.py

4. Open in browser
It will automatically open in your browser at http://localhost:8501

## Files
project_tracker.py – Main Streamlit application
project.py - To create Excel file
projects.xlsx – Excel file to store and retrieve project data
README.md – Project documentation
