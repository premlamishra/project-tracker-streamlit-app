import pandas as pd

data = {
    'Project Name': [],
    'Owner': [],
    'Status': [],
    'Deadline': [],
    'Last Updated': []
}
df = pd.DataFrame(data)
df.to_excel("projects.xlsx", index=False)
